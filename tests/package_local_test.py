# Copyright 2021 Gary Stidston-Broadbent
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
import os
from pathlib import Path
import pytest
from dismantle.package import (
    LocalPackageHandler,
    PackageHandler,
    DirectoryPackageFormat,
    TarPackageFormat,
    TgzPackageFormat,
    ZipPackageFormat
)


def test_inherits() -> None:
    assert issubclass(LocalPackageHandler, PackageHandler) is True


def test_grasp_exists(datadir: Path) -> None:
    src = datadir.join('package.zip')
    assert LocalPackageHandler.grasps(src) is True


def test_grasp_non_existant(datadir: Path) -> None:
    src = datadir.join('non_existant.zip')
    assert LocalPackageHandler.grasps(src) is False


def test_grasp_not_supported(datadir: Path) -> None:
    src = datadir.join('directory_src')
    assert LocalPackageHandler.grasps(src) is False


def test_grasp_not_http_url(datadir: Path) -> None:
    src = 'https://google.com/package.zip'
    assert LocalPackageHandler.grasps(src) is False


def test_grasp_file_url(datadir: Path) -> None:
    src = f'file://{datadir.join("package.zip")}'
    assert LocalPackageHandler.grasps(src) is True


def test_grasp_not_supported_format(datadir: Path) -> None:
    src = datadir.join('invalid.file')
    assert LocalPackageHandler.grasps(src) is False


def test_src_notfound(datadir: Path) -> None:
    name = 'package/not-found'
    src = datadir.join(name)
    message = 'unable to process source format'
    with pytest.raises(FileNotFoundError, match=message):
        LocalPackageHandler(name, src)


def test_subclass_correct(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join(name)
    package = LocalPackageHandler(name, src)
    assert isinstance(package, PackageHandler) is True


def test_install_no_destination(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join(name)
    package = LocalPackageHandler(name, src)
    assert package.installed is False
    assert package.install(version='0.0.1') is True
    assert package.installed is True


def test_install_directory_exists(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join(name)
    dest = datadir.join('directory_exists')
    message = 'destination already exists'
    package = LocalPackageHandler(name, src)
    assert package.installed is False
    with pytest.raises(FileExistsError, match=message):
        package.install(dest, '0.0.1')
    assert package.installed is False


def test_install_directory_create(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join(name)
    dest = datadir.join('package-nonexistant')
    package = LocalPackageHandler(name, src)
    assert package.installed is False
    package.install(dest, '0.0.1')
    assert package.installed is True
    assert os.path.exists(src)


def test_meta_value_nonexistant(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join(name)
    package = LocalPackageHandler(name, src)
    message = 'nonexistant is an invalid attribute'
    assert package.install(src, '0.0.1') is True
    with pytest.raises(AttributeError, match=message):
        assert package.nonexistant


def test_name(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join(name)
    package = LocalPackageHandler(name, src)
    assert package.install(src, '0.0.1') is True
    assert package.name == name
    assert package.name != '@scope-two/package-one'


def test_name_invalid(datadir: Path) -> None:
    name = '@scope-one/package-two'
    wrong_name = '@scope-one/package-one'
    src = datadir.join(wrong_name)
    message = 'meta name does not match provided package name'
    package = LocalPackageHandler(name, src)
    with pytest.raises(ValueError, match=message):
        package.install(src, '0.0.1')


def test_name_missing(datadir: Path) -> None:
    name = '@scope-one/package-three'
    src = datadir.join(name)
    message = 'meta file missing name value'
    package = LocalPackageHandler(name, src)
    with pytest.raises(ValueError, match=message):
        package.install(src, '0.0.1')


def test_version(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join(name)
    package = LocalPackageHandler(name, src)
    assert package.install(src, '0.0.1') is True
    assert package.version == '0.0.1'
    assert package.version != '1.0.1'


def test_version_missing(datadir: Path) -> None:
    name = '@scope-one/package-four'
    src = datadir.join(name)
    message = 'meta file missing version value'
    package = LocalPackageHandler(name, src)
    with pytest.raises(ValueError, match=message):
        package.install(src, '0.0.1')


def test_verification_none(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join(name)
    package = LocalPackageHandler(name, src)
    assert package.verify() is True


def test_verification_value(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join(name)
    message = 'the local package handler does not support verification'
    package = LocalPackageHandler(name, src)
    with pytest.raises(ValueError, match=message):
        package.verify('a0aea27ca371ef0e715c594300e22ef9')


def test_uninstall(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join(name)
    dest = datadir.join('test_uninstall')
    package = LocalPackageHandler(name, src)
    assert package.installed is False
    package.install(dest, version='0.0.1')
    assert package.installed is True
    assert os.path.exists(src)
    assert package.uninstall() is True
    assert os.path.exists(src) is True
    assert package.installed is False


def test_uninstall_with_dest(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join(name)
    dest = datadir.join('package-nonexistant')
    package = LocalPackageHandler(name, src)
    assert package.installed is False
    package.install(dest, '0.0.1')
    assert package.installed is True
    assert os.path.exists(src) is True
    assert os.path.exists(dest)
    assert package.uninstall() is True
    assert os.path.exists(src) is True
    assert os.path.exists(dest) is False
    assert package.installed is False


def test_directory_format(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join(name)
    dest = datadir.join('package-nonexistant')
    package = LocalPackageHandler(name, src)
    assert package.installed is False
    package.install(dest, '0.0.1')
    assert package.installed is True
    assert os.path.exists(src) is True
    assert os.path.exists(dest)
    assert package.uninstall() is True
    assert os.path.exists(src) is True
    assert os.path.exists(dest) is False
    assert package.installed is False


def test_zip_format(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join('package.zip')
    dest = datadir.join('package-nonexistant')
    package = LocalPackageHandler(name, src, [ZipPackageFormat])
    assert package.installed is False
    package.install(dest, '0.0.1')
    assert package.installed is True
    assert os.path.exists(src) is True
    assert os.path.exists(dest) is True
    assert os.path.exists(dest / 'package.json') is True
    assert package.uninstall() is True
    assert os.path.exists(src) is True
    assert os.path.exists(dest) is False
    assert package.installed is False


def test_tar_format(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join('package.tar')
    dest = datadir.join('package-nonexistant')
    package = LocalPackageHandler(name, src, [TarPackageFormat])
    assert package.installed is False
    package.install(dest, '0.0.1')
    assert package.installed is True
    assert os.path.exists(src) is True
    assert os.path.exists(dest) is True
    assert os.path.exists(dest / 'package.json') is True
    assert package.uninstall() is True
    assert os.path.exists(src) is True
    assert os.path.exists(dest) is False
    assert package.installed is False


def test_tgz_format(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join('package.tgz')
    dest = datadir.join('package-nonexistant')
    package = LocalPackageHandler(name, src, [TgzPackageFormat])
    assert package.installed is False
    package.install(dest, '0.0.1')
    assert package.installed is True
    assert os.path.exists(src) is True
    assert os.path.exists(dest) is True
    assert os.path.exists(dest / 'package.json') is True
    assert package.uninstall() is True
    assert os.path.exists(src) is True
    assert os.path.exists(dest) is False
    assert package.installed is False


def test_multi_format(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join('package.tgz')
    dest = datadir.join('package-nonexistant')
    formats = [
        DirectoryPackageFormat,
        TgzPackageFormat,
        ZipPackageFormat,
        TarPackageFormat
    ]
    package = LocalPackageHandler(name, src, formats)
    assert package.installed is False
    package.install(dest, '0.0.1')
    assert package.installed is True
    assert os.path.exists(src) is True
    assert os.path.exists(dest) is True
    assert os.path.exists(dest / 'package.json') is True
    assert package.uninstall() is True
    assert os.path.exists(src) is True
    assert os.path.exists(dest) is False
    assert package.installed is False


def test_no_format(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join('package.zip')
    message = 'unable to process source format'
    with pytest.raises(FileNotFoundError, match=message):
        LocalPackageHandler(name, src, [])


def test_missing_format(datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = datadir.join('package.zip')
    message = 'unable to process source format'
    with pytest.raises(FileNotFoundError, match=message):
        LocalPackageHandler(name, src, [TarPackageFormat])
