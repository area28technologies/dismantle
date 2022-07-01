# Dismantle

**Dismantle** is a module created for Python programs to provide the ability to provide additional functionality using packages listed within local or remote indices and installed during runtime.

Dismantle does this by checking a package index and using that index to manage package versions. Packages then contain plugins (using decorators) and extensions (using a custom module loader) to add the additional functionality to the application.

## Installing Dismantle

Dismantle is available on PyPI:

```console
$ python -m pip install dismantle
```

NOTE: *Dismantle officially supports Python from 3.7 up

## Supported Features & Best–Practices

Dismantle provides the flexibility within applications allowing developers to build rich ecosystems around core applications. It does this by providing the following:

### Index Management

Index files are used to provide list of available packages and provide information on packages and
the versions of said packages available.

- support for multiple index files that cascade
- easy to create custom index handlers providing additional ways to define package indices
- local index file support using json built in
- url based index file support using json built in
- etag based caching for url based index

### Packaging

Packages listed in index files provide the ability to bundle features and act as a transport
mechanism for additional functionality while providing security.

- easy to create custom package handlers providing additional ways to define package sources
- easy to create custom package formats compression types and structures
- support for zip, tar.gz, tgz, and local directories as package formats built in
- support for local and url based (http/https) package handlers built in
- hash validation for packages with the ability to verify package integrity

### Extensions

Extensions contained within packages provide a way to dynamically load modules at runtime for
Python modules as needed.  Packages can replace or extend application functionality at runtime by
replacing or adding modules in Pythons global modules manager.

- Categorized extension groups to filter extension types (eg. loggers, parsers, ...)
- Support for __init__ or .py based module loading.
- Extension activation and deactivation management.
- Module name collision avoidance
- Hierarchical module naming

### Plugins

Plugins contained within packages provide a way to intercept function parameters and return values
in order to manipulate data on the fly.  Plugins can be used for data validation, manipilation, or
to provide additional logging or auditing functionality.

- Decorator based plugins with pre and post value interceptions and/or modification
- Multiple plugins per function with ability to set execution order
- Activation management

## Example implementations

### Plugin

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

### Extension

```python
"""Full example using all aspects."""
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
    package = LocalPackageHandler(meta['name'], 'foo/path')
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
