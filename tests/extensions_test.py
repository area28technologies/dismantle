import sys
from pathlib import Path
from dismantle.extension import Extensions
from dismantle.index import JsonFileIndexHandler
from dismantle.package import LocalPackageHandler


def test_success(datadir: Path) -> None:
    from tests.ColorExtension import ColorExtension
    from tests.GreetingExtension import GreetingExtension
    ext_types = [ColorExtension, GreetingExtension]
    index_src = datadir.join('index.json')
    index = JsonFileIndexHandler(index_src)
    packages = {}
    for pkg_meta in index:
        meta = index[pkg_meta]
        path = datadir.join(meta['path'])
        package = LocalPackageHandler(meta['name'], path)
        package._meta = {**package._meta, **meta}
        package.install()
        packages[package.name] = package
    extensions = Extensions(ext_types, packages, 'd_')
    assert extensions.types == ['color', 'greeting']
    assert list(extensions.category('color').keys()) == [
        '@scope-one/package-one.extension.green.GreenColorExtension',
        '@scope-one/package-two.extension.red.RedColorExtension',
        '@scope-one/package-three.extension.blue.BlueColorExtension',
    ]
    assert list(extensions.extensions.keys()) == ['color', 'greeting']
    assert list(extensions.imports.keys()) == [
        '@scope-one/package-one.extension.hello',
        '@scope-one/package-one.extension.green',
        '@scope-one/package-two.extension.afternoon',
        '@scope-one/package-two.extension.red',
        '@scope-one/package-three.extension.goodbye',
        '@scope-one/package-three.extension.blue'
    ]


def test_in_sys_modules(datadir: Path) -> None:
    from tests.ColorExtension import ColorExtension
    ext_types = [ColorExtension]
    index_src = datadir.join('index_in_sys_modules.json')
    index = JsonFileIndexHandler(index_src)
    packages = {}
    for pkg_meta in index:
        meta = index[pkg_meta]
        path = datadir.join(meta['path'])
        package = LocalPackageHandler(meta['name'], path)
        package._meta = {**package._meta, **meta}
        package.install()
        packages[package.name] = package
    extensions = Extensions(ext_types, packages, 'd_')
    assert extensions.types == ['color']
    assert list(extensions.category('color').keys()) == [
        '@scope-five/package-one.extension.carbon.CarbonColorExtension'
    ]
    assert list(extensions.extensions.keys()) == ['color']
    assert list(extensions.imports.keys()) == [
        '@scope-five/package-one.extension.carbon'
    ]
    assert '@scope-five/package-one.extension.carbon' in sys.modules
