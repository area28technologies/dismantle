"""Test packages using a zip file format."""
import os
from pathlib import Path

import pytest

from dismantle.package import PackageFormat, ZipPackageFormat


def test_inherits() -> None:
    assert issubclass(ZipPackageFormat, PackageFormat) is True


def test_grasp_exists(datadir: Path) -> None:
    src = datadir / 'package.zip'
    assert ZipPackageFormat.grasps(src) is True


def test_grasp_file_url(datadir: Path) -> None:
    src = f'file://{datadir.join("package.zip")}'
    assert ZipPackageFormat.grasps(src) is True


def test_grasp_not_supported(datadir: Path) -> None:
    src = datadir / 'directory_src'
    assert ZipPackageFormat.grasps(src) is False


def test_grasp_not_supported_format(datadir: Path) -> None:
    src = datadir / 'invalid.file'
    assert ZipPackageFormat.grasps(src) is False


def test_extract_not_supported(datadir: Path) -> None:
    src = datadir / 'directory_src'
    dest = datadir / f'{src}_output'
    message = 'formatter only supports zip files'
    with pytest.raises(ValueError, match=message):
        ZipPackageFormat.extract(src, dest)


def test_extract_not_supported_format(datadir: Path) -> None:
    src = datadir / 'invalid.file'
    dest = datadir / f'{src}_output'
    message = 'formatter only supports zip files'
    with pytest.raises(ValueError, match=message):
        ZipPackageFormat.extract(src, dest)


def test_extract_non_existant(datadir: Path) -> None:
    src = datadir / 'non_existant.zip'
    dest = datadir / f'{src}_output'
    message = 'invalid zip file'
    with pytest.raises(ValueError, match=message):
        ZipPackageFormat.extract(src, dest)


def test_extract_already_exists(datadir: Path) -> None:
    src = datadir / 'package.zip'
    dest = datadir / 'directory_exists'
    assert ZipPackageFormat.extract(src, dest) is None


def test_extract_create(datadir: Path) -> None:
    src = datadir / 'package.zip'
    dest = datadir / 'directory_created'
    ZipPackageFormat.extract(src, dest)
    assert os.path.exists(dest) is True
    assert os.path.exists(dest / 'package.json') is True
