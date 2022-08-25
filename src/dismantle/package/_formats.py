import abc
import shutil
import tarfile
import zipfile
from pathlib import Path
from typing import Union

from dismantle.utils import _parse_filepath


class PackageFormat(metaclass=abc.ABCMeta):
    """Base class for packet formats."""

    @staticmethod
    @abc.abstractmethod
    def grasps(path: Union[str, Path]) -> bool:
        """Check if format can be processed."""
        ...

    @staticmethod
    @abc.abstractmethod
    def extract(src: Union[str, Path], dest: Union[str, Path]) -> bool:
        """Extract a package to the cache location."""
        ...


class DirectoryPackageFormat(PackageFormat):
    """A package format using a directory to hold files."""

    @staticmethod
    def grasps(path: Union[str, Path]) -> bool:
        """Check if dir on the local filesystem has been provided."""
        path = _parse_filepath(path)
        try:
            return Path(str(path)).is_dir()
        except OSError:
            return False

    @staticmethod
    def extract(src: Union[str, Path], dest: Union[str, Path]) -> None:
        """Use the formatter to process any movement related actions."""
        src = _parse_filepath(src)
        dest = _parse_filepath(dest)
        if not DirectoryPackageFormat.grasps(src):
            message = 'formatter only supports directories'
            raise ValueError(message)
        if dest != src:
            shutil.rmtree(dest, ignore_errors=True)
            shutil.copytree(
                src,
                dest,
                ignore=shutil.ignore_patterns('.git', '__pycache__')
            )


class ZipPackageFormat(PackageFormat):
    """A package format compressed as a zip file."""

    @staticmethod
    def grasps(path: Union[str, Path]) -> bool:
        """Check if dir on the local filesystem has been provided."""
        path = _parse_filepath(path)
        zip_path = Path(path)
        return zip_path.suffix == '.zip'

    @staticmethod
    def extract(src: Union[str, Path], dest: Union[str, Path]) -> None:
        """Extract the zipfile to the cache location."""
        src = _parse_filepath(src)
        dest = _parse_filepath(dest)
        src = Path(src)
        dest_path = Path(dest)

        if not ZipPackageFormat.grasps(src):
            message = 'formatter only supports zip files'
            raise ValueError(message)
        if not src.is_file() or not zipfile.is_zipfile(src):
            message = 'invalid zip file'
            raise ValueError(message)
        with zipfile.ZipFile(src, 'r') as zip_ref:
            zip_ref.extractall(dest_path)


class TarPackageFormat(PackageFormat):
    """A package format using a compressed tar file."""

    @staticmethod
    def grasps(path: Union[str, Path]) -> bool:
        """Check if dir on the local filesystem has been provided."""
        path = _parse_filepath(path)
        tar_path = Path(path)
        suffixes = ''.join(tar_path.suffixes)
        return suffixes == '.tar'

    @staticmethod
    def extract(src: Union[str, Path], dest: Union[str, Path]) -> None:
        """Extract the tarfile to the cache location."""
        src = _parse_filepath(src)
        dest = _parse_filepath(dest)
        src_path = Path(src)
        dest_path = Path(dest)

        if not TarPackageFormat.grasps(src_path):
            message = 'formatter only supports tar files'
            raise ValueError(message)
        if not src_path.is_file() or not tarfile.is_tarfile(src_path):
            message = 'invalid tar file'
            raise ValueError(message)
        with tarfile.open(src_path, 'r') as tar_ref:
            tar_ref.extractall(dest_path)


class TgzPackageFormat(PackageFormat):
    """A package format using a tgz file compression."""

    @staticmethod
    def grasps(path: Union[str, Path]) -> bool:
        """Check if dir on the local filesystem has been provided."""
        path = _parse_filepath(path)
        src_path = Path(path)
        suffixes = ''.join(src_path.suffixes)
        return suffixes in {'.tgz', '.tar.gz'}

    @staticmethod
    def extract(src: Union[str, Path], dest: Union[str, Path]) -> None:
        """Extract the tarfile to the cache location."""
        src = _parse_filepath(src)
        dest = _parse_filepath(dest)
        src_path = Path(src)
        dest_path = Path(dest)

        if not TgzPackageFormat.grasps(src_path):
            message = 'formatter only supports tar.gz files'
            raise ValueError(message)
        if not src_path.is_file() or not tarfile.is_tarfile(src_path):
            message = 'invalid tgz file'
            raise ValueError(message)
        with tarfile.open(src_path, 'r') as tgz_ref:
            tgz_ref.extractall(dest_path)
