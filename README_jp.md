# TAGS
TAが生徒を割いてする際に用いるコマンド. 

## Installation
Github経由でpip installを行う.
```bash
pip install git+https://github.com/Qip21n0/TAGS.git
```

## Description
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
compile  download  help  test  unzip

Undocumented commands:
======================
EOF  cd  ls
```

## Notes
TAGSで採点するには、[Google Chrome](https://www.google.com/intl/ja/chrome/)が既にインストール済みでなければなりません. 

---
### **Windows**の方

[WSL](https://docs.microsoft.com/ja-jp/windows/wsl/install)上でTAGSを使うことをお勧めします.

- Windows10ユーザは[VcXsrv](https://sourceforge.net/projects/vcxsrv/)を用いて利用してください. 
- Windows11ユーザは[WSLg](https://github.com/microsoft/wslg)を用いることもできます.

#### Link
- [Can't use X-Server in WSL 2 - GitHub Issues #4106](https://github.com/microsoft/WSL/issues/4106)
- [【WSL2】VcXsrvでUbuntu GUIアプリケーションを実行する【Xサーバー】](https://tamnology.com/wsl2-vcxsrv/)

---
### MacOSやLinuxの方
特になし.