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

    _name = "default"
    _category = "default"

    def __init__(self):
        self._active = False

    def activeate(self):
        self._active = True

    def deactivate(self):
        self._active = False

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @property
    def active(self):
        return self._active
