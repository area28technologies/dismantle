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
from ._formats import (
    DirectoryPackageFormat,
    PackageFormat,
    TarPackageFormat,
    TgzPackageFormat,
    ZipPackageFormat
)
from ._handlers import (
    HttpPackageHandler,
    LocalPackageHandler,
    PackageHandler
)


__all__ = [
    'HttpPackageHandler',
    'PackageFormat',
    'PackageHandler',
    'DirectoryPackageFormat',
    'LocalPackageHandler',
    'ZipPackageFormat',
    'TarPackageFormat',
    'TgzPackageFormat'
]

# IDEAS: --- package ----------------------------
# IDEAS: Package handlers for multiple package types
# IDEAS: Update packages, show latest version, show current version
# IDEAS: Get package information (author, description, ...)
# IDEAS: Verify package hash
# IDEAS: Create a package
# IDEAS: Submit a package (needs a handler)

# load manifest handler
# load installed handler
