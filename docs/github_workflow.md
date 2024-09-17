# GitHub Workflow for a Python package

## On pull-request
- Run lint
- Run tests with coverage on the main platform & version (e.g., Ubuntu latest + Python 3.12)
- Publish the coverage report to [Codecov]

## On push to `main` branch
- Run lint
- Run tests with coverage on all supported platforms & versions ((Ubuntu latest, macOS) * (Python 3.11, Python 3.12))
- Publish the coverage report to [Codecov]

## On push to semver tag
- _(if branch main contains the tag)_ Create GitHub Release (TBD)
- Build Python package
- Build documentation & publish to GitHub Pages. _(TBD: how to maintain multiple versions of
  documentation, e.g., tagged releases + HEAD)_
- Publish package to TestPyPi
- _(if tag is strictly MAJOR.MINOR.PATCH, i.e., not rc or dev build)_ Publish package to PyPi

[Codecov]: https://codecov.io
