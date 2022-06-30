"""Test packages conpressed as tgz files."""
import os
from pathlib import Path

import pytest

from dismantle.package import PackageFormat, TgzPackageFormat


def test_inherits() -> None:
    assert issubclass(TgzPackageFormat, PackageFormat) is True


def test_grasp_exists(datadir: Path) -> None:
    src = datadir / 'package.tar.gz'
    assert TgzPackageFormat.grasps(src) is True


def test_grasp_file_url(datadir: Path) -> None:
    src = f'file://{datadir.join("package.tgz")}'
    assert TgzPackageFormat.grasps(src) is True


def test_grasp_exists_tgz(datadir: Path) -> None:
    src = datadir / 'package.tgz'
    assert TgzPackageFormat.grasps(src) is True


def test_grasp_not_supported(datadir: Path) -> None:
    src = datadir / 'directory_src'
    assert TgzPackageFormat.grasps(src) is False


def test_grasp_not_supported_format(datadir: Path) -> None:
    src = datadir / 'invalid.file'
    assert TgzPackageFormat.grasps(src) is False


def test_extract_not_supported(datadir: Path) -> None:
    src = datadir / 'directory_src'
    dest = datadir / f'{src}_output'
    message = 'formatter only supports tar.gz files'
    with pytest.raises(ValueError, match=message):
        TgzPackageFormat.extract(src, dest)


def test_extract_not_supported_format(datadir: Path) -> None:
    src = datadir / 'invalid.file'
    dest = datadir / f'{src}_output'
    message = 'formatter only supports tar.gz files'
    with pytest.raises(ValueError, match=message):
        TgzPackageFormat.extract(src, dest)


def test_extract_non_existant(datadir: Path) -> None:
    src = datadir / 'non_existant.tar.gz'
    dest = datadir / f'{src}_output'
    message = 'invalid tgz file'
    with pytest.raises(ValueError, match=message):
        TgzPackageFormat.extract(src, dest)


def test_extract_non_existant_tgz(datadir: Path) -> None:
    src = datadir / 'non_existant.tgz'
    dest = datadir / f'{src}_output'
    message = 'invalid tgz file'
    with pytest.raises(ValueError, match=message):
        TgzPackageFormat.extract(src, dest)


def test_extract_already_exists(datadir: Path) -> None:
    src = datadir / 'package.tar.gz'
    dest = datadir / 'directory_exists'
    assert TgzPackageFormat.extract(src, dest) is None


def test_extract_already_exists_tgz(datadir: Path) -> None:
    src = datadir / 'package.tgz'
    dest = datadir / 'directory_exists'
    assert TgzPackageFormat.extract(src, dest) is None


def test_extract_create(datadir: Path) -> None:
    src = datadir / 'package.tar.gz'
    dest = datadir / 'directory_created'
    TgzPackageFormat.extract(src, dest)
    assert os.path.exists(dest) is True
    assert os.path.exists(dest / 'package.json') is True


def test_extract_create_tgz(datadir: Path) -> None:
    src = datadir / 'package.tar.gz'
    dest = datadir / 'directory_created'
    TgzPackageFormat.extract(src, dest)
    assert os.path.exists(dest) is True
    assert os.path.exists(dest / 'package.json') is True
