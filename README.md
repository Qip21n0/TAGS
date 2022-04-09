# TAGS
Commands used by the TA for grading students (TAGS).

Japanese translation is [here](https://github.com/Qip21n0/TAGS/blob/main/README_jp.md)

## Demo
![demo](https://github.com/Qip21n0/TAGS/blob/main/gif/demo.gif)

## Installation
pip install via Github
```bash
pip install git+https://github.com/Qip21n0/TAGS.git
```

## Description
TAGS can be used as a command.
```
$ tags test --help
Welcome to TAGS system!!! (2022/04/03 08:39:08)

Usage: main.py test [OPTIONS]

Options:
  -m, --modified  Add this option if you want to modify test.txt or
                  answer.txt.
  --help          Show this message and exit.
```

TAGS can also be used in [REPL(Read–eval–print loop)](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop).
```
$ tags
Welcome to TAGS system!!! (2022/04/03 08:36:32)
Type "help" for more information.
Press [Ctl + C] or [Ctl + D] to exit this mode.
======================== 
TAGS>> help

Documented commands (type help <topic>):
========================================
compile  download  help  show  test  unzip

Undocumented commands:
======================
EOF  cd  ls
```

## Notes
If you want to grade with TAGS, you must already have [Google Chrome](https://www.google.com/intl/en/chrome/) installed. 

---
### For **Windows**

- Command prompt
  1. Install `python` and `gcc` and `git`
  2. Install `pyreadline` with pip
  3. Add the paths for gcc and Python Scripts to the environment variable PATH.

- WSL
  1. If `WSLg` is not available, please use `X Server`.
  2. Install `python` and `pip` and `git` and `python3-tk`
  3. Install `python-xlib` with pip

---
### For MacOS & Linux
None.