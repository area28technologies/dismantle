import os
from pathlib import Path
import pytest
from dismantle.package import PackageFormat, TarPackageFormat


def test_inherits() -> None:
    assert issubclass(TarPackageFormat, PackageFormat) is True


def test_grasp_exists(datadir: Path) -> None:
    src = datadir.join('package.tar')
    assert TarPackageFormat.grasps(src) is True


def test_grasp_file_url(datadir: Path) -> None:
    src = f'file://{datadir.join("package.tar")}'
    assert TarPackageFormat.grasps(src) is True


def test_grasp_not_supported(datadir: Path) -> None:
    src = datadir.join('directory_src')
    assert TarPackageFormat.grasps(src) is False


def test_grasp_not_supported_format(datadir: Path) -> None:
    src = datadir.join('invalid.file')
    assert TarPackageFormat.grasps(src) is False


def test_extract_not_supported(datadir: Path) -> None:
    src = datadir.join('directory_src')
    dest = datadir.join(f'{src}_output')
    message = 'formatter only supports tar files'
    with pytest.raises(ValueError, match=message):
        TarPackageFormat.extract(src, dest)


def test_extract_not_supported_format(datadir: Path) -> None:
    src = datadir.join('invalid.file')
    dest = datadir.join(f'{src}_output')
    message = 'formatter only supports tar files'
    with pytest.raises(ValueError, match=message):
        TarPackageFormat.extract(src, dest)


def test_extract_non_existant(datadir: Path) -> None:
    src = datadir.join('non_existant.tar')
    dest = datadir.join(f'{src}_output')
    message = 'invalid tar file'
    with pytest.raises(ValueError, match=message):
        TarPackageFormat.extract(src, dest)


def test_extract_already_exists(datadir: Path) -> None:
    src = datadir.join('package.tar')
    dest = datadir.join('directory_exists')
    message = 'destination already exists'
    with pytest.raises(FileExistsError, match=message):
        TarPackageFormat.extract(src, dest)


def test_extract_create(datadir: Path) -> None:
    src = datadir.join('package.tar')
    dest = datadir.join('directory_created')
    TarPackageFormat.extract(src, dest)
    assert os.path.exists(dest) is True
    assert os.path.exists(dest / 'package.json') is True
