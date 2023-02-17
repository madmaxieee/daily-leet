# `daily-leet`

**Usage**:

```console
$ daily-leet [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `daily`: Fetch today's daily challenge and create...
* `new`: Fetch data from a problem's description...

## `daily-leet daily`

Fetch today's daily challenge and create files for it, then open the problem page in browser and open the main file in editor

**Usage**:

```console
$ daily-leet daily [OPTIONS] LANGUAGE:{python|python3|py|cpp|c++|go|golang|rust}
```

**Arguments**:

* `LANGUAGE:{python|python3|py|cpp|c++|go|golang|rust}`: The language you want to use  [required]

**Options**:

* `--help`: Show this message and exit.

## `daily-leet new`

Fetch data from a problem's description page and create files for it, then open the problem page in browser and open the main file in editor

**Usage**:

```console
$ daily-leet new [OPTIONS] LANGUAGE:{python|python3|py|cpp|c++|go|golang|rust}
```

**Arguments**:

* `LANGUAGE:{python|python3|py|cpp|c++|go|golang|rust}`: The language you want to use  [required]

**Options**:

* `-u, --url TEXT`: The url to fetch data from, usually a problem's description page. e.g. https://leetcode.com/problems/two-sum/. You need to provide either url or problem title.
* `-t, --title TEXT`: The title of the problem, separated by '-' or ' '. e.g. two-sum. You need to provide either url or problem title.
* `--help`: Show this message and exit.
