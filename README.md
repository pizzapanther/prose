# Prose

An unpoetic version of [Poetry](https://python-poetry.org/).

While the Poetry package is elegant and reduces a Python developers burden, every day usage has some small annoyances. Some of these things could be fixed but have been considered out of scope and unpoetic.

Prose is made to be the everyday version of Poetry and little bit more trashy. But the trashiness serves those well in the dirty jobs of life. Prose is a wrapper around Poetry so all commands and APIs should function the same with the addition of more features.

## Installation

```
pip install trashy-poetry
```

## Usage

Substitute all `poetry` commands for `prose`.

See [Poetry Docs](https://python-poetry.org/docs/). All commands and APIs function the same except for the additional features documented.

For Example:

```
poetry init -> prose init

poetry shell -> prose shell
```

## Features

### Task Runner

Prose includes [Poe the Poet](https://github.com/nat-n/poethepoet) by default. Poe the Poet lets you create shortcuts to common tasks such as shell scripts and Python functions. The usage and API functions the same as documented except for the addition of the `poe` shortcut.

`prose run poe [options] task [task_args]`

can also be run as

`prose poe [options] task [task_args]`

### Hardcoded Environmental Variables

Inject environmental variables into the `run` and `shell` commands by hard coding them into you `pyproject.toml` file.

**Example:**

```
[tool.prose.env]
TEST_ENV = "hello world"
TEST_PATH = "${PATH}:/narf"
```

Any variables set in the `tool.prose.env` section of your toml file will be injected into the environment for you.

### Load DotEnv Files

### Default DotEnv Files

Prose loads `.env` files if it finds it in the current working directory. See [python-dotenv](https://pypi.org/project/python-dotenv/) for usage documentation.

## Custom DotEnv Files
Prose allows you to add custom `.env` files with a command line switch for the `poe`, `run`, and `shell` commands.

```
OPTIONS
  -e (--env)             Dotenv file to load (multiple values allowed)
```

**Examples:**

```
prose shell -e path/custom.env
prose run -e path/custom.env printenv NARF
prose poe -e path/custom.env mycommand
```

*Note: When using the `run` and `poe` commands, the `-e` and `--env` options must be used before your command arguments*
