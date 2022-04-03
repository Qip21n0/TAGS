# TAGS
Commands used by the TA for grading students (TAGS).

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

TAGS can also be used in [REPL(Read–eval–print loop)](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop)
```
$ tags
Welcome to TAGS system!!! (2022/04/03 08:36:32)
Type "help" for more information.
Press [Ctl + C] or [Ctl + D] to exit this mode.
======================== 
TAGS>> help

Documented commands (type help <topic>):
========================================
compile  download  help  test  unzip

Undocumented commands:
======================
EOF  cd  ls
```