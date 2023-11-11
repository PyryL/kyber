# Usage guide

## Installation

Make sure that you have [Poetry](https://python-poetry.org/) installed. After cloning the repository to your computer move to its root directory and run

```
poetry install
```

## Usage

Currently `kyber` provides three main functions that can be used directly from Python code. A sample usage is included in  `main.py`.

At the moment there is no GUI or CLI available.

### Tests

Unit tests can be run with

```
poetry run invoke test
```

### Coverage

Coverage report can be created with

```
poetry run invoke coverage-report
```

after which the report will appear at `htmlcov/index.html`.

### Lint

Run static style cheking with

```
poetry run invoke lint
```
