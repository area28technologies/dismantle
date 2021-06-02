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
from json import JSONDecodeError
import pytest
from dismantle.index import IndexHandler, JsonFileIndexHandler


def test_notfound(datadir):
    with pytest.raises(FileNotFoundError):
        JsonFileIndexHandler(datadir.join('index_notfound.json'))


def test_blank(datadir):
    with pytest.raises(JSONDecodeError):
        JsonFileIndexHandler(datadir.join('index_blank.json'))


def test_empty(datadir):
    index = JsonFileIndexHandler(datadir.join('index_empty.json'))
    assert len(index) == 0


def test_broken(datadir):
    with pytest.raises(JSONDecodeError):
        JsonFileIndexHandler(datadir.join('index_broken.json'))


def test_populated(datadir):
    index = JsonFileIndexHandler(datadir.join('index_populated.json'))
    assert isinstance(index, IndexHandler) is True


def test_rfc8089(datadir):
    path = 'file://' + str(datadir.join('index_populated.json'))
    index = JsonFileIndexHandler(path)
    assert isinstance(index, IndexHandler) is True


def test_outdated(datadir):
    index = JsonFileIndexHandler(datadir.join('index_populated.json'))
    assert index.outdated is False


def test_update(datadir):
    index = JsonFileIndexHandler(datadir.join('index_populated.json'))
    assert index.update() is True


def test_length(datadir):
    index = JsonFileIndexHandler(datadir.join('index_populated.json'))
    assert len(index) == 6
    assert len(index.find('@scope-one/package-one')) == 1
    assert len(index.find('package-one')) == 3
    assert len(index.find('package-two')) == 2
    assert len(index.find('package-three')) == 1
    assert len(index.find('@scope-one')) == 3
    assert len(index.find('@scope-two')) == 2
    assert len(index.find('@scope-three')) == 1


def test_populated_package_exists(datadir):
    index = JsonFileIndexHandler(datadir.join('index_populated.json'))
    package = index["@scope-one/package-one"]
    assert package["name"] == "@scope-one/package-one"
    assert package["version"] == "0.1.0"
    assert package["path"] == "@scope-one/package-one"


def test_populated_package_nonexistant(datadir):
    index = JsonFileIndexHandler(datadir.join('index_populated.json'))
    with pytest.raises(KeyError):
        index["@scope-four/package-one"]
