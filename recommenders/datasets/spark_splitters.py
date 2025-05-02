
import numpy as np

try:
    from pyspark.sql import functions as F, Window
    from pyspark.storagelevel import StorageLevel
except ImportError:
    pass  # skip this import if we are in pure python environment

from recommenders.utils.constants import (
    DEFAULT_ITEM_COL,
    DEFAULT_USER_COL,
    DEFAULT_TIMESTAMP_COL,
)
from recommenders.datasets.split_utils import (
    process_split_ratio,
    min_rating_filter_spark,
)

# random
def spark_random_split(data, ratio=0.75, seed=42):
    multi_split, ratio = process_split_ratio(ratio)

    if multi_split:
        return data.randomSplit(ratio, seed=seed)
    else:
        return data.randomSplit([ratio, 1 - ratio], seed=seed)

# Helper function to perform stratified splits.
def _do_stratification_spark(
    data,
    ratio=0.75,
    min_rating=1,
    filter_by="user",
    is_partitioned=True,
    is_random=True,
    seed=42,
    col_user=DEFAULT_USER_COL,
    col_item=DEFAULT_ITEM_COL,
    col_timestamp=DEFAULT_TIMESTAMP_COL,
):
    # A few preliminary checks.
    if filter_by not in ["user", "item"]:
        raise ValueError("filter_by should be either 'user' or 'item'.")

    if min_rating < 1:
        raise ValueError("min_rating should be integer and larger than or equal to 1.")

    if col_user not in data.columns:
        raise ValueError("Schema of data not valid. Missing User Col")

    if col_item not in data.columns:
        raise ValueError("Schema of data not valid. Missing Item Col")

    if not is_random:
        if col_timestamp not in data.columns:
            raise ValueError("Schema of data not valid. Missing Timestamp Col")

    if min_rating > 1:
        data = min_rating_filter_spark(
            data=data,
            min_rating=min_rating,
            filter_by=filter_by,
            col_user=col_user,
            col_item=col_item,
        )

    split_by = col_user if filter_by == "user" else col_item
    partition_by = split_by if is_partitioned else []

    col_random = "_random"
    if is_random:
        data = data.withColumn(col_random, F.rand(seed=seed))
        order_by = F.col(col_random)
    else:
        order_by = F.col(col_timestamp)

    window_count = Window.partitionBy(partition_by)
    window_spec = Window.partitionBy(partition_by).orderBy(order_by)

    data = (
        data.withColumn("_count", F.count(split_by).over(window_count))
        .withColumn("_rank", F.row_number().over(window_spec) / F.col("_count"))
        .drop("_count", col_random)
    )
    # Persist to avoid duplicate rows in splits caused by lazy evaluation
    data.persist(StorageLevel.MEMORY_AND_DISK_2).count()

    multi_split, ratio = process_split_ratio(ratio)
    ratio = ratio if multi_split else [ratio, 1 - ratio]

    splits = []
    prev_split = None
    for split in np.cumsum(ratio):
        condition = F.col("_rank") <= split
        if prev_split is not None:
            condition &= F.col("_rank") > prev_split
        splits.append(data.filter(condition).drop("_rank"))
        prev_split = split

    return splits

# Spark chronological splitter.
def spark_chrono_split(
    data,
    ratio=0.75,
    min_rating=1,
    filter_by="user",
    col_user=DEFAULT_USER_COL,
    col_item=DEFAULT_ITEM_COL,
    col_timestamp=DEFAULT_TIMESTAMP_COL,
    no_partition=False,
):
    return _do_stratification_spark(
        data=data,
        ratio=ratio,
        min_rating=min_rating,
        filter_by=filter_by,
        is_random=False,
        col_user=col_user,
        col_item=col_item,
        col_timestamp=col_timestamp,
    )

# user/item distributed in similar way
def spark_stratified_split(
    data,
    ratio=0.75,
    min_rating=1,
    filter_by="user",
    col_user=DEFAULT_USER_COL,
    col_item=DEFAULT_ITEM_COL,
    seed=42,
):
    return _do_stratification_spark(
        data=data,
        ratio=ratio,
        min_rating=min_rating,
        filter_by=filter_by,
        seed=seed,
        col_user=col_user,
        col_item=col_item,
    )

# Spark timestamp based splitter.
def spark_timestamp_split(
    data,
    ratio=0.75,
    col_user=DEFAULT_USER_COL,
    col_item=DEFAULT_ITEM_COL,
    col_timestamp=DEFAULT_TIMESTAMP_COL,
):
    return _do_stratification_spark(
        data=data,
        ratio=ratio,
        is_random=False,
        is_partitioned=False,
        col_user=col_user,
        col_item=col_item,
        col_timestamp=col_timestamp,
    )