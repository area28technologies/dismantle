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
class IExtension:
    """Extension interface to recognise what needs to be processed."""

    _name: str = "default"
    _category: str = "default"

    def __init__(self) -> None:
        self._active: bool = False

    def activeate(self) -> bool:
        self._active = True
        return self._active

    def deactivate(self) -> bool:
        self._active = False
        return not self._active

    @property
    def name(self) -> str:
        return self._name

    @property
    def category(self) -> str:
        return self._category

    @property
    def active(self) -> bool:
        return self._active
