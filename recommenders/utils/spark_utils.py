import os
from pyspark.sql import SparkSession

MMLSPARK_PACKAGE = "com.microsoft.azure:synapseml_2.12:0.9.5"
MMLSPARK_REPO = "https://mmlspark.azureedge.net/maven"

def start_or_get_spark(
    app_name="Sample",
    url="local[*]",
    memory="10g",
    config=None,
    packages=None,
    jars=None,
    repositories=None,
):
    """Start Spark if not started

    Args:
        app_name (str): set name of the application
        url (str): URL for spark master
        memory (str): size of memory for spark driver. This will be ignored if spark.driver.memory is set in config.
        config (dict): dictionary of configuration options
        packages (list): list of packages to install
        jars (list): list of jar files to add
        repositories (list): list of maven repositories

    Returns:
        object: Spark context.
    """

    builder = SparkSession.builder.appName(app_name)

    if url:
        builder = builder.master(url)

    builder = builder.config("spark.driver.memory", memory)
    builder = builder.config("spark.driver.extraJavaOptions", "-Xss4m")

    if config:
        for k, v in config.items():
            builder = builder.config(k, v)

    if packages:
        builder = builder.config("spark.jars.packages", ",".join(packages))

    if jars:
        builder = builder.config("spark.jars", ",".join(jars))

    if repositories:
        builder = builder.config("spark.jars.repositories", ",".join(repositories))

    return builder.getOrCreate()

    # submit_args = ""
    # if packages is not None:
    #     submit_args = "--packages {} ".format(",".join(packages))
    # if jars is not None:
    #     submit_args += "--jars {} ".format(",".join(jars))
    # if repositories is not None:
    #     submit_args += "--repositories {}".format(",".join(repositories))
    # if submit_args:
    #     os.environ["PYSPARK_SUBMIT_ARGS"] = "{} pyspark-shell".format(submit_args)

    # spark_opts = [
    #     'SparkSession.builder.appName("{}")'.format(app_name),
    #     'master("{}")'.format(url),
    # ]

    # if config is not None:
    #     for key, raw_value in config.items():
    #         value = (
    #             '"{}"'.format(raw_value) if isinstance(raw_value, str) else raw_value
    #         )
    #         spark_opts.append('config("{key}", {value})'.format(key=key, value=value))

    # if config is None or "spark.driver.memory" not in config:
    #     spark_opts.append('config("spark.driver.memory", "{}")'.format(memory))

    # # Set larger stack size
    # spark_opts.append('config("spark.executor.extraJavaOptions", "-Xss4m")')
    # spark_opts.append('config("spark.driver.extraJavaOptions", "-Xss4m")')

    # spark_opts.append("getOrCreate()")
    # return eval(".".join(spark_opts))