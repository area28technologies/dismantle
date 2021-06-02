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
"""Dismantle package manager system with support for extensions and plugins."""

# IDEAS: --- extension --------------------------
# IDEAS: Class Hook to provide extensions (add new abilities such as log types)
# IDEAS: activate, deactivate, active

__all__ = [
    'IExtension',
    'Extensions'
]

from .iextension import IExtension
from .extensions import Extensions  # noqa: I001 (needs to be after iextension)
