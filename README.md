```
     _                                     _   _ _
 ___(_)___  ___ _ __  ___  ___       _   _| |_(_) |___
/ __| / __|/ _ \ '_ \/ __|/ _ \_____| | | | __| | / __|
\__ \ \__ \  __/ | | \__ \  __/_____| |_| | |_| | \__ \
|___/_|___/\___|_| |_|___/\___|      \__,_|\__|_|_|___/

```

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![mypy: checked](https://img.shields.io/badge/mypy-checked-green)](http://mypy-lang.org)

`sisense-utils` is a collection of utilities I create when working with [Sisense](https://www.sisense.com/).

- `get_folder_components()` is useful to figure out the folder components of a Sisense dashboard. It depends on `GET /dashboards` and `GET /navver` endpoints.
