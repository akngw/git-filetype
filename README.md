# git-ft

git-ftというGitのサブコマンドです。拡張子ごとの行数・ファイル数が取得できます。

## インストール

```
pip install git+https://github.com/akngw/gitft
```

## 使い方

```
usage: git-ft [-h] [-c] [-I] [-i] [tree]

positional arguments:
  tree

optional arguments:
  -h, --help         show this help message and exit
  -c, --count        show the numbers of files and lines
  -I                 ignore binary files
  -i, --ignore-case  ignore case the extensions
```

## 使用例

```
$ git ft -c
:2:150
.cfg:1:11
.md:1:1
.py:1:104
.toml:1:3
$
```

treeを省略するとHEADです。
