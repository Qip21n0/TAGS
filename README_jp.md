# TAGS
TAが生徒を採点する際に用いるコマンド. 

## デモ
![demo](https://github.com/Qip21n0/TAGS/blob/main/gif/demo.gif)

## インストール
インストールをする前に[注意](https://github.com/Qip21n0/TAGS/blob/main/README_jp.md#%E6%B3%A8%E6%84%8F)を確認してください.

Github経由でpip installを行う.
```bash
pip install git+https://github.com/Qip21n0/TAGS.git
```

## 説明
TAGSはコマンドとして使えます. 
```
$ tags test --help
Welcome to TAGS system!!! (2022/04/03 08:39:08)

Usage: main.py test [OPTIONS]

Options:
  -m, --modified  Add this option if you want to modify test.txt or
                  answer.txt.
  --help          Show this message and exit.
```

また、TAGSは[REPL(Read–eval–print loop)](https://ja.wikipedia.org/wiki/REPL)モードでも使うことができます.
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

## 注意
TAGSで採点するには、[Google Chrome](https://www.google.com/intl/ja/chrome/)が既にインストール済みでなければなりません. 

---
### **Windows**の方

- コマンドプロンプト
  1. `python`と`gcc`, `git`をインストール
  2. pipを用いて`pyreadline`をインストール
  3. 環境変数PATHにgccとPythonのScriptsのものを加える

- WSL
  1. `WSLg`が利用できないなら、`X server`を入れてください
  2. `python`と`pip`, `git`, `python3-tk`をインストール
  3. pipを用いて`python-xlib`をインストール

---
### MacOSやLinuxの方
特になし.