"""Test loading packages from within a directory."""
import os
from pathlib import Path

import pytest

from dismantle.package import DirectoryPackageFormat, PackageFormat


def test_inherits() -> None:
    assert issubclass(DirectoryPackageFormat, PackageFormat) is True


def test_grasp_exists(datadir: Path) -> None:
    src = datadir / 'directory_src'
    assert DirectoryPackageFormat.grasps(src) is True


def test_grasp_non_existant(datadir: Path) -> None:
    src = datadir / 'directory_non_existant'
    assert DirectoryPackageFormat.grasps(src) is False


def test_grasp_not_supported(datadir: Path) -> None:
    src = datadir / 'package.zip'
    assert DirectoryPackageFormat.grasps(src) is False


def test_extract_not_supported(datadir: Path) -> None:
    src = datadir / 'package.zip'
    dest = datadir / f'{src}_output'
    message = 'formatter only supports directories'
    with pytest.raises(ValueError, match=message):
        DirectoryPackageFormat.extract(src, dest)


def test_extract_non_existant(datadir: Path) -> None:
    src = datadir / 'directory_non_existant'
    dest = datadir / f'{src}_output'
    message = 'formatter only supports directories'
    with pytest.raises(ValueError, match=message):
        DirectoryPackageFormat.extract(src, dest)


def test_extract_already_exists(datadir: Path) -> None:
    src = datadir / 'directory_src'
    dest = datadir / 'directory_exists'
    DirectoryPackageFormat.extract(src, dest)
    assert os.path.exists(dest) is True
    assert os.path.exists(dest / 'package.json') is True


def test_extract_create(datadir: Path) -> None:
    src = datadir / 'directory_src'
    dest = datadir / 'directory_created'
    DirectoryPackageFormat.extract(src, dest)
    assert os.path.exists(dest) is True
    assert os.path.exists(dest / 'package.json') is True
