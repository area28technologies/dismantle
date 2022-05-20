"""Configure Sphinx to use pyproject.toml file.

Waiting for https://github.com/sphinx-doc/sphinx/issues/9506 to move all
configuration into pyproject.toml. Until then, use the sphinx_pyproject
module.
"""
from sphinx_pyproject import SphinxConfig

config = SphinxConfig("../../pyproject.toml", globalns=globals())

project = config["project"]
author = config["author"]
release = version = config.version
documentation_summary = config.description
github_url = (
    f"https://github.com/{config['github_username']}"
    f"/{config['github_repository']}"
)
