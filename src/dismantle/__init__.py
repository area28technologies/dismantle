#      888 ,e,                                     d8   888
#  e88 888  "   dP"Y 888 888 8e   ,"Y88b 888 8e   d88   888  ,e e,
# d888 888 888 C88b  888 888 88b "8" 888 888 88b d88888 888 d88 88b
# Y888 888 888  Y88D 888 888 888 ,ee 888 888 888  888   888 888   ,
#  "88 888 888 d,dP  888 888 888 "88 888 888 888  888   888  "YeeP"
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
"""Dismantle is a Python package / plugin / extension manager."""
import logging
from dismantle.__version__ import __version__  # noqa: F401


logging.getLogger(__name__).addHandler(logging.NullHandler())
