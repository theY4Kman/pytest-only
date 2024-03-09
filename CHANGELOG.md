# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [Unreleased]
### Fixed
 - Resolve brittle handling of class- and module-level assignments in flake8 plugin


## [2.1.0] — 2024-03-08
### Added
 - Add [flake8](https://github.com/PyCQA/flake8) plugin to detect `only` marks before they get committed (see [GH#11](https://github.com/theY4Kman/pytest-only/issues/11))


## [2.0.0] — 2022-06-14
### Added
 - Added [pylint](https://pylint.pycqa.org) plugin to detect `only` marks before they get committed (thank you, [@nikolaik](https://github.com/nikolaik) — [GH#10](https://github.com/theY4Kman/pytest-only/pull/10))

### Changed
 - Remove support for Python 2.7


## [1.2.2] — 2020-01-18
### Fixed
 - Register the `only` mark to avoid warning messages emitted since 4.5.0 (thank you, [@nicoddemus](https://github.com/nicoddemus) – [GH#8](https://github.com/theY4Kman/pytest-only/pull/8))


## [1.2.1] — 2019-01-09
### Fixed
 - Fix get_marker usage for compatibility with pytest 4.1.0 (see https://github.com/pytest-dev/pytest/issues/4546)


## [1.2.0] — 2018-12-23
### Added
 - Add `--no-only` and `--only` cmd-line options to disable and enable plugin functionality


## [1.1.0] — 2017-03-28
### Fixed
 - Call `pytest_deselected` with deselected tests
