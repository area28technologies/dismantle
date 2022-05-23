"""Creates a solution to handle multiple package formats."""
from dismantle.package._formats import (
    DirectoryPackageFormat,
    PackageFormat,
    TarPackageFormat,
    TgzPackageFormat,
    ZipPackageFormat
)
from dismantle.package._handlers import (
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
