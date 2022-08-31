# Changelog
All notable changes to this project will be documented in this file.

## [1.x.x] - 2022-xx-xx

## [1.1.1] - 2022-08-31
### Fixed
- Relaxed jinja2 dependency

## Fixed
- Fixed import of version in documentation

## [1.1.0] - 2022-08-17
### Added
- Added location check to inform about degraded performance from outside US

## [1.0.0] - 2022-08-17
### Added
- Major first release
### Changed
- Updated README.md
- `.create` renamed `.run`
- Updated endpoint names
- Updated endpoint routes
- Fixed imports in `__init__` to surpress warnings
- Moved `version` from `config.py` to `__init__`
- Moved `log_level` from `config.py` to `__init__`
- Moved from `grequests` to `requests` for sync calls to avoid gevent warnings
- Moved import of `grequests` to runtime to avoid gevent warnings
### Removed
- `Bearer` prefix for Token authorization

## [0.0.7] - 2022-06-06
### Fixed for
- Dependencies security issues

## [0.0.6] - 2022-05-31
### Fixed for
- Error at package import

## [0.0.5] - 2022-05-26
### Changed
- This changelog

### Fixed for
- Documentation

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

- __Added__ for new features.
- __Changed__ for changes in existing functionality.
- __Deprecated__ for soon-to-be removed features. 
- __Removed__ for now removed features.
- __Fixed for__ any bug fixes.
- __Security__ in case of vulnerabilities.