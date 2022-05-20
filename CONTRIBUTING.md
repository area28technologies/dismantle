# Contributing to Dismantle

## New Release

- update version number in pyproject.toml and src/dismantle/__version__.py
- git commit -m "release: cut release 0.0.0"
- git tag -s v0.0.0 -m "release: cut release 0.0.0"
- git push
- git push --tags
- poetry build
- poetry publish

# Code flow

1. scheme selector is called with a URI to decide which scheme processor to use and it returns a Scheme Processor (eg. http(s), file, ftp)
2. scheme processor checks the source uri to get the

3. index scheme selector is called with a URI
4. index scheme selector chooses which Scheme to use (eg. http(s), file, ftp)
5. selected scheme handler

6. Scheme check if an installed version exists
    a) if one does not exist, Scheme checks if a cached version exists
      1. if cached does not exist, fetch from the url
      2.
   1. if one exists, check the hash
      1. if valid,
5.
