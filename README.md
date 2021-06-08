# Dismantle

**Dismantle** Python package / plugin / extension manager.

```python
"""Simple plugin example"""
from dismantle import plugin


class Chat():
    @plugin.register('chat.message')
    def show(self, message):
        print(message)


@plugin.plugin('chat.message', order=-1)
def make_uppercase(message):
    return message.upper()

```

```python
"""Full example using all aspects."""
from pathlib import Path
from dismantle.extension import Extensions, IExtension
from dismantle.index import JsonFileIndexHandler
from dismantle.package import LocalPackageHandler


class ColorExtension(IExtension):
    _category = 'color'

    def color(self) -> None:
        ...


class GreenColorExtension(ColorExtension):
    _name = 'green'

    def color(self) -> None:
        print(f'color is {self._name}')


packages = {}
index = JsonFileIndexHandler('index.json')
for pkg_meta in index:
    meta = index[pkg_meta]
    path = datadir.join(meta['path'])
    package = LocalPackageHandler(meta['name'], path)
    package._meta = {**package._meta, **meta}
    package.install()
    packages[package.name] = package
extensions = Extensions([ColorExtension], packages, 'ext_')
assert extensions.types == ['color']
assert list(extensions.category('color').keys()) == [
    '@scope-one/package-one.extension.green.GreenColorExtension',
    '@scope-one/package-two.extension.red.RedColorExtension',
    '@scope-one/package-three.extension.blue.BlueColorExtension',
]
assert list(extensions.extensions.keys()) == ['color']
assert list(extensions.imports.keys()) == [
    '@scope-one/package-one.extension.green',
    '@scope-one/package-two.extension.red',
    '@scope-one/package-three.extension.blue'
]
```

Dismantle allows you to provide the ability to create a plugin/extension/module for an application.
It does this by checking a package index and using that index to manage package versions. Packages
then contain plugins (using decorators) and extensions (using a custom module loader) to add the
additional functionality to the application.

## Installing Dismantle and Supported Versions

Dismantle is available on PyPI:

```console
$ python -m pip install dismantle
```

Dismantle officially supports Python 3.7+.

## Supported Features & Best–Practices

Dismantle is ready for the demands of providing flexibility within applications allowing developers
to build rich ecosystems around core applications.

### Index Management

- easy to create custom index handlers providing additional ways to define package indexes
- local index file support using json
- url based index file support using json
- etag based caching for url based index

### Packaging

- easy to create custom package handlers providing additional ways to define package sources
- easy to create custom package formats compression types and structures
- support for zip, tar.gz, tgz, and local directories as package formats
- support for local and url based (http/https) package handlers
- hash validation for packages with the ability to verify package integrity

### Extensions

- Categorized extension groups to filter extension types (eg. loggers, parsers, ...)
- Support for __init__ or .py based module loading.
- Extension activation and deactivation management.
- Module name collision avoidance
- Hierarchical module naming

### Plugins

- Decorator based plugins with pre and post value modification
- Multiple plugins per function with ability to set execution order
- Activation management
