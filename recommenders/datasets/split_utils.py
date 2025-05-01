from contextlib import contextmanager
from tempfile import TemporaryDirectory
import zipfile

@contextmanager
def download_path(path=None):
    if not path:
        tmp_dir = TemporaryDirectory()
        try:
            yield tmp_dir.name
        finally:
            tmp_dir.cleanup()
    else:
        path = os.path.realpath(path)
        yield path

def unzip_file(zip_src, dst_dir, clean_zip_file=False):
    fz = zipfile.ZipFile(zip_src, "r")
    for file in fz.namelist():
        fz.extract(file, dst_dir)
    if clean_zip_file:
        os.remove(zip_src)