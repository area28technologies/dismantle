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
from hashlib import md5
from json import JSONDecodeError
from shutil import copy2
import pytest
from pytest_httpserver import HTTPServer
from pytest_httpserver.httpserver import HandlerType
from requests import ConnectionError
from dismantle.index import IndexHandler, JsonUrlIndexHandler


def test_invalid_server(httpserver: HTTPServer, tmpdir):
    with pytest.raises(ConnectionError):
        JsonUrlIndexHandler('http://invalid.server/notfound.json', tmpdir)
    httpserver.check_assertions()


def test_notfound(httpserver: HTTPServer, tmpdir):
    httpserver.no_handler_status_code = 404
    params = {"uri": "/invalid.json", 'handler_type': HandlerType.ONESHOT}
    httpserver.expect_request(**params).respond_with_data("")
    with pytest.raises(FileNotFoundError):
        JsonUrlIndexHandler(httpserver.url_for('notfound.json'), tmpdir)


def test_blank(httpserver: HTTPServer, tmpdir):
    params = {"uri": "/blank.json", 'handler_type': HandlerType.ONESHOT}
    httpserver.expect_request(**params).respond_with_data("")
    with pytest.raises(JSONDecodeError):
        JsonUrlIndexHandler(httpserver.url_for('blank.json'), tmpdir)
    httpserver.check_assertions()


def test_empty(httpserver: HTTPServer, datadir):
    with open(datadir.join('index_empty.json')) as json_file:
        data = json_file.read()
    params = {"uri": "/empty.json", 'handler_type': HandlerType.ONESHOT}
    httpserver.expect_request(**params).respond_with_data(data)
    index = JsonUrlIndexHandler(httpserver.url_for('empty.json'), datadir)
    httpserver.check_assertions()
    assert len(index) == 0


def test_broken(httpserver: HTTPServer, datadir):
    with open(datadir.join('index_broken.json')) as json_file:
        data = json_file.read()
    params = {"uri": "/broken.json", 'handler_type': HandlerType.ONESHOT}
    httpserver.expect_request(**params).respond_with_data(data)
    with pytest.raises(JSONDecodeError):
        JsonUrlIndexHandler(httpserver.url_for('broken.json'), datadir)
    httpserver.check_assertions()


def test_populated(httpserver: HTTPServer, datadir):
    with open(datadir.join('index_populated.json')) as json_file:
        data = json_file.read()
    params = {"uri": "/populated.json", 'handler_type': HandlerType.ONESHOT}
    httpserver.expect_request(**params).respond_with_data(data)
    index = JsonUrlIndexHandler(httpserver.url_for('populated.json'), datadir)
    assert isinstance(index, IndexHandler) is True
    httpserver.check_assertions()


def test_latest(httpserver: HTTPServer, datadir):
    copy2(datadir.join('index_populated.json'), datadir.join('index.json'))
    file_digest = md5()  # noqa: S303
    with open(datadir.join('index_populated.json'), "rb") as cached_index:
        for block in iter(lambda: cached_index.read(65536), b""):
            file_digest.update(block)
    digest = file_digest.hexdigest()
    headers = {"If-None-Match": digest}
    params = {
        "uri": "/latest.json",
        "headers": headers,
        'handler_type': HandlerType.ONESHOT
    }
    httpserver.expect_request(**params).respond_with_data("", status=304)
    index = JsonUrlIndexHandler(httpserver.url_for('latest.json'), datadir)
    assert isinstance(index, IndexHandler) is True
    assert index._updated is False


def test_current(httpserver: HTTPServer, datadir):
    copy2(datadir.join('index_populated.json'), datadir.join('index.json'))
    file_digest = md5()  # noqa: S303
    with open(datadir.join('index_populated.json'), "rb") as cached_index:
        for block in iter(lambda: cached_index.read(65536), b""):
            file_digest.update(block)
    digest = file_digest.hexdigest()
    headers = {"If-None-Match": digest}
    params = {
        "uri": "/current.json",
        "headers": headers,
        'handler_type': HandlerType.PERMANENT
    }
    httpserver.expect_request(**params).respond_with_data("", status=304)
    index = JsonUrlIndexHandler(httpserver.url_for('current.json'), datadir)
    assert isinstance(index, IndexHandler) is True
    assert index.outdated is False


def test_outdated(httpserver: HTTPServer, datadir):
    copy2(datadir.join('index_empty.json'), datadir.join('index.json'))
    file_digest = md5()  # noqa: S303
    with open(datadir.join('index_empty.json'), "rb") as cached_index:
        for block in iter(lambda: cached_index.read(65536), b""):
            file_digest.update(block)
    digest = file_digest.hexdigest()
    headers = {"If-None-Match": digest}
    params = {
        "uri": "/outdated.json",
        "headers": headers,
        "method": "GET",
        'handler_type': HandlerType.ONESHOT
    }
    httpserver.expect_request(**params).respond_with_data("", status=304)
    index = JsonUrlIndexHandler(httpserver.url_for('outdated.json'), datadir)
    assert isinstance(index, IndexHandler) is True
    assert index._updated is False
    params['method'] = 'HEAD'
    with open(datadir.join('index_populated.json')) as json_file:
        data = json_file.read()
    httpserver.expect_request(**params).respond_with_data(data, status=200)
    assert index.outdated is True


def test_create(httpserver: HTTPServer, datadir):
    with open(datadir.join('index_populated.json')) as json_file:
        data = json_file.read()
    httpserver.expect_request(
        "/create.json"
    ).respond_with_data(data, status=200)
    index = JsonUrlIndexHandler(httpserver.url_for('create.json'), datadir)
    assert isinstance(index, IndexHandler) is True
    assert index._updated is True


def test_update(httpserver: HTTPServer, datadir):
    with open(datadir.join('index_populated.json')) as json_file:
        data = json_file.read()
    httpserver.expect_request(
        "/update.json"
    ).respond_with_data(data, status=200)
    index = JsonUrlIndexHandler(httpserver.url_for('update.json'), datadir)
    assert isinstance(index, IndexHandler) is True
    assert index._updated is True


def test_populated_index_length(httpserver: HTTPServer, datadir):
    with open(datadir.join('index_populated.json')) as json_file:
        data = json_file.read()
    httpserver.expect_request("/populated.json").respond_with_data(data)
    index = JsonUrlIndexHandler(httpserver.url_for('populated.json'), datadir)
    httpserver.check_assertions()
    assert len(index) == 6
    assert len(index.find('@scope-one/package-one')) == 1
    assert len(index.find('package-one')) == 3
    assert len(index.find('package-two')) == 2
    assert len(index.find('package-three')) == 1
    assert len(index.find('@scope-one')) == 3
    assert len(index.find('@scope-two')) == 2
    assert len(index.find('@scope-three')) == 1


def test_populated_pkg_exists(httpserver: HTTPServer, datadir):
    with open(datadir.join('index_populated.json')) as json_file:
        data = json_file.read()
    params = {"uri": "/exists.json", 'handler_type': HandlerType.ONESHOT}
    httpserver.expect_request(**params).respond_with_data(data)
    index = JsonUrlIndexHandler(httpserver.url_for('exists.json'), datadir)
    httpserver.check_assertions()
    package = index["@scope-one/package-one"]
    assert package["name"] == "@scope-one/package-one"
    assert package["version"] == "0.1.0"
    assert package["path"] == "@scope-one/package-one"


def test_populated_pkg_nonexistant(httpserver: HTTPServer, datadir):
    with open(datadir.join('index_populated.json')) as json_file:
        data = json_file.read()
    params = {"uri": "/nonexist.json", 'handler_type': HandlerType.ONESHOT}
    httpserver.expect_request(**params).respond_with_data(data)
    index = JsonUrlIndexHandler(httpserver.url_for('nonexist.json'), datadir)
    with pytest.raises(KeyError):
        index["@scope-four/package-one"]
    httpserver.check_assertions()
