import os
from pathlib import Path
import pytest
from pytest_httpserver import HTTPServer
from pytest_httpserver.httpserver import HandlerType
from requests import ConnectionError
from dismantle.package import (
    DirectoryPackageFormat,
    HttpPackageHandler,
    PackageHandler,
    TarPackageFormat,
    TgzPackageFormat,
    ZipPackageFormat
)


def test_inherits() -> None:
    assert issubclass(HttpPackageHandler, PackageHandler) is True


def test_grasp_http_support() -> None:
    src = 'http://google.com/package.zip'
    assert HttpPackageHandler.grasps(src) is True


def test_grasp_https_support() -> None:
    src = 'https://google.com/package.zip'
    assert HttpPackageHandler.grasps(src) is True


def test_grasp_invalid_ftp() -> None:
    src = 'ftp://google.com/package.zip'
    assert HttpPackageHandler.grasps(src) is False


def test_grasp_invalid_file(datadir: Path) -> None:
    src = datadir.join('package.zip')
    assert HttpPackageHandler.grasps(src) is False


def test_grasp_invalid_path(datadir: Path) -> None:
    src = datadir.join('@scope-one/package-one')
    assert HttpPackageHandler.grasps(src) is False


def test_invalid_server(httpserver: HTTPServer) -> None:
    name = '@scope-one/package-one'
    src = 'http://invalid.server.com/notfound.zip'
    package = HttpPackageHandler(name, src)
    with pytest.raises(ConnectionError):
        package.install(src, '0.0.1')
    httpserver.check_assertions()


def test_notfound(httpserver: HTTPServer, datadir) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('notfound.zip')
    dest = datadir.join('package-nonexistant')
    httpserver.no_handler_status_code = 404
    params = {"uri": "/invalid.zip", 'handler_type': HandlerType.ONESHOT}
    httpserver.expect_request(**params).respond_with_data("")
    package = HttpPackageHandler(name, src)
    with pytest.raises(FileNotFoundError):
        package.install(dest)


def test_install_dir_exists(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/package.zip')
    dest = 'directory_exists'
    message = 'destination already exists'
    with open(datadir.join('package.zip'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.zip").respond_with_data(data)
    package = HttpPackageHandler(name, src)
    assert package.installed is False
    with pytest.raises(FileExistsError, match=message):
        package.install(datadir.join(dest), '0.0.1')
    assert package.installed is False


def test_install_create(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/package.zip')
    dest = datadir.join('package-create')
    with open(datadir.join('package.zip'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.zip").respond_with_data(data)
    package = HttpPackageHandler(name, src)
    assert package.installed is False
    package.install(dest, '0.0.1')
    assert package.installed is True
    assert os.path.exists(package._cache)


def test_meta_value_nonexistant(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/package.zip')
    dest = datadir.join('package-create')
    message = 'nonexistant is an invalid attribute'
    with open(datadir.join('package.zip'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.zip").respond_with_data(data)
    package = HttpPackageHandler(name, src)
    assert package.installed is False
    assert package.install(dest, '0.0.1') is True
    with pytest.raises(AttributeError, match=message):
        assert package.nonexistant


def test_name(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/package.zip')
    dest = datadir.join('package-create')
    with open(datadir.join('package.zip'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.zip").respond_with_data(data)
    package = HttpPackageHandler(name, src)
    assert package.installed is False
    assert package.install(dest, '0.0.1') is True
    assert package.name == name
    assert package.name != '@scope-two/package-one'


def test_name_invalid(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-two'
    src = httpserver.url_for('/package.zip')
    dest = datadir.join('package-create')
    message = 'meta name does not match provided package name'
    with open(datadir.join('package.zip'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.zip").respond_with_data(data)
    package = HttpPackageHandler(name, src)
    assert package.installed is False
    with pytest.raises(ValueError, match=message):
        package.install(dest, '0.0.1')
    assert package.installed is False


def test_name_missing(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/missing_name.zip')
    dest = datadir.join('package-create')
    message = 'meta file missing name value'
    with open(datadir.join('missing_name.zip'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/missing_name.zip").respond_with_data(data)
    package = HttpPackageHandler(name, src)
    with pytest.raises(ValueError, match=message):
        package.install(dest, '0.0.1')


def test_version(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/package.zip')
    dest = datadir.join('package-version')
    with open(datadir.join('package.zip'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.zip").respond_with_data(data)
    package = HttpPackageHandler(name, src)
    assert package.install(dest, '0.0.1') is True
    assert package.version == '0.0.1'
    assert package.version != '1.0.1'


def test_version_missing(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/missing_version.zip')
    dest = datadir.join('package-create')
    message = 'meta file missing version value'
    with open(datadir.join('missing_version.zip'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/missing_version.zip").respond_with_data(data)
    package = HttpPackageHandler(name, src)
    with pytest.raises(ValueError, match=message):
        package.install(dest, '0.0.1')


def test_verification_none(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/package.zip')
    with open(datadir.join('package.zip'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.zip").respond_with_data(data)
    package = HttpPackageHandler(name, src)
    assert package.verify() is True


def test_verification_value(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/package.zip')
    message = 'the http package handler does not support verification'
    with open(datadir.join('package.zip'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.zip").respond_with_data(data)
    package = HttpPackageHandler(name, src)
    with pytest.raises(ValueError, match=message):
        package.verify('a0aea27ca371ef0e715c594300e22ef9')


def test_uninstall(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/package.zip')
    dest = datadir.join('package-uninstall')
    with open(datadir.join('package.zip'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.zip").respond_with_data(data)
    package = HttpPackageHandler(name, src)
    assert package.installed is False
    package.install(dest, version='0.0.1')
    assert package.installed is True
    assert package.uninstall() is True
    assert os.path.exists(dest) is False
    assert package.installed is False


def test_zip_format(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/package.zip')
    dest = datadir.join('package-zip')
    with open(datadir.join('package.zip'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.zip").respond_with_data(data)
    package = HttpPackageHandler(name, src, [ZipPackageFormat])
    assert package.installed is False
    package.install(dest, '0.0.1')
    assert package.installed is True
    assert os.path.exists(dest) is True
    assert os.path.exists(dest / 'package.json') is True
    assert package.uninstall() is True
    assert os.path.exists(dest) is False
    assert package.installed is False


def test_tar_format(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/package.tar')
    dest = datadir.join('package-tar')
    with open(datadir.join('package.tar'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.tar").respond_with_data(data)
    package = HttpPackageHandler(name, src, [TarPackageFormat])
    assert package.installed is False
    package.install(dest, '0.0.1')
    assert package.installed is True
    assert os.path.exists(dest) is True
    assert os.path.exists(dest / 'package.json') is True
    assert package.uninstall() is True
    assert os.path.exists(dest) is False
    assert package.installed is False


def test_tgz_format(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/package.tgz')
    dest = datadir.join('package-tgz')
    with open(datadir.join('package.tgz'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.tgz").respond_with_data(data)
    package = HttpPackageHandler(name, src, [TgzPackageFormat])
    assert package.installed is False
    package.install(dest, '0.0.1')
    assert package.installed is True
    assert os.path.exists(dest) is True
    assert os.path.exists(dest / 'package.json') is True
    assert package.uninstall() is True
    assert os.path.exists(dest) is False
    assert package.installed is False


def test_multi_format(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/package.tgz')
    dest = datadir.join('package-tgz')
    formats = [
        DirectoryPackageFormat,
        TgzPackageFormat,
        ZipPackageFormat,
        TarPackageFormat
    ]
    with open(datadir.join('package.tgz'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.tgz").respond_with_data(data)
    package = HttpPackageHandler(name, src, formats)
    assert package.installed is False
    package.install(dest, '0.0.1')
    assert package.installed is True
    assert os.path.exists(dest) is True
    assert os.path.exists(dest / 'package.json') is True
    assert package.uninstall() is True
    assert os.path.exists(dest) is False
    assert package.installed is False


def test_no_format(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/package.zip')
    with open(datadir.join('package.zip'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.zip").respond_with_data(data)
    message = 'a valid source is required'
    with pytest.raises(FileNotFoundError, match=message):
        HttpPackageHandler(name, src, [])


def test_missing_format(httpserver: HTTPServer, datadir: Path) -> None:
    name = '@scope-one/package-one'
    src = httpserver.url_for('/package.zip')
    with open(datadir.join('package.zip'), 'rb') as pkg_file:
        data = pkg_file.read()
    httpserver.expect_request("/package.zip").respond_with_data(data)
    message = 'a valid source is required'
    with pytest.raises(FileNotFoundError, match=message):
        HttpPackageHandler(name, src, [TarPackageFormat])
