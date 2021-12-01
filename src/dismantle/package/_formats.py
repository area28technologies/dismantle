import abc
import shutil
import tarfile
import zipfile
from pathlib import Path
from typing import Union


class PackageFormat(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def grasps(path: any) -> bool:
        """Return a boolean value describing whether the Format can be
        processed.
        """
        ...

    @staticmethod
    @abc.abstractmethod
    def verify(signature: str) -> bool:
        """Verify a packages hash with the provided signature."""
        ...

    @staticmethod
    @abc.abstractmethod
    def extract(src: any, dest: str) -> bool:
        """Verify a packages hash with the provided signature."""
        ...


class DirectoryPackageFormat(PackageFormat):

    @staticmethod
    def grasps(path: any) -> bool:
        """Check if a directory on the local filesystem has been provided."""
        path = str(path)[7:] if str(path)[:7] == 'file://' else path
        try:
            return Path(str(path)).is_dir()
        except OSError:
            return False

    @staticmethod
    def extract(src: any, dest: str) -> bool:
        """Use the formatter to process any movement related actions."""
        src = str(src)[7:] if str(src)[:7] == 'file://' else src
        dest = str(dest)[7:] if str(dest)[:7] == 'file://' else dest
        if not DirectoryPackageFormat.grasps(src):
            message = 'formatter only supports directories'
            raise ValueError(message)
        if dest != src:
            try:
                shutil.copytree(src, dest)
            except FileExistsError:
                raise FileExistsError('destination already exists')


class ZipPackageFormat(PackageFormat):

    @staticmethod
    def grasps(path: any) -> bool:
        """Check if a directory on the local filesystem has been provided."""
        path = str(path)[7:] if str(path)[:7] == 'file://' else path
        zip_path = Path(path)
        if zip_path.suffix != '.zip':
            return False
        return True

    @staticmethod
    def extract(src: Union[str, Path], dest: str):
        """Extract the zipfile to the cache location."""
        src = str(src)[7:] if str(src)[:7] == 'file://' else src
        dest = str(dest)[7:] if str(dest)[:7] == 'file://' else dest
        src = Path(src)
        if not ZipPackageFormat.grasps(src):
            message = 'formatter only supports zip files'
            raise ValueError(message)
        if not src.is_file() or not zipfile.is_zipfile(src):
            message = 'invalid zip file'
            raise ValueError(message)
        dest_path = Path(dest)
        with zipfile.ZipFile(src, 'r') as zip_ref:
            zip_ref.extractall(dest_path)


class TarPackageFormat(PackageFormat):

    @staticmethod
    def grasps(path: any) -> bool:
        """Check if a directory on the local filesystem has been provided."""
        path = str(path)[7:] if str(path)[:7] == 'file://' else path
        tar_path = Path(path)
        suffixes = ''.join(tar_path.suffixes)
        if suffixes != '.tar':
            return False
        return True

    @staticmethod
    def extract(src: str, dest: str):
        """Extract the tarfile to the cache location."""
        src = str(src)[7:] if str(src)[:7] == 'file://' else src
        dest = str(dest)[7:] if str(dest)[:7] == 'file://' else dest
        src = Path(src)
        if not TarPackageFormat.grasps(src):
            message = 'formatter only supports tar files'
            raise ValueError(message)
        if not src.is_file() or not tarfile.is_tarfile(src):
            message = 'invalid tar file'
            raise ValueError(message)
        dest_path = Path(dest)
        with tarfile.open(src, 'r') as tar_ref:
            tar_ref.extractall(dest_path)


class TgzPackageFormat(PackageFormat):

    @staticmethod
    def grasps(path: any) -> bool:
        """Check if a directory on the local filesystem has been provided."""
        path = str(path)[7:] if str(path)[:7] == 'file://' else path
        tgz = Path(path)
        suffixes = ''.join(tgz.suffixes)
        if suffixes not in ['.tgz', '.tar.gz']:
            return False
        return True

    @staticmethod
    def extract(src: str, dest: str):
        """Extract the tarfile to the cache location."""
        src = str(src)[7:] if str(src)[:7] == 'file://' else src
        dest = str(dest)[7:] if str(dest)[:7] == 'file://' else dest
        src = Path(src)
        if not TgzPackageFormat.grasps(src):
            message = 'formatter only supports tar.gz files'
            raise ValueError(message)
        if not src.is_file() or not tarfile.is_tarfile(src):
            message = 'invalid tgz file'
            raise ValueError(message)
        dest_path = Path(dest)
        with tarfile.open(src, 'r') as tgz_ref:
            tgz_ref.extractall(dest_path)
