#!/usr/bin/env python3

from copy import deepcopy
from functools import partial, reduce
import argparse
import os
import re
import subprocess


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("tree", nargs="?", default="HEAD")
    parser.add_argument(
        "-c",
        "--count",
        action="store_const",
        dest="print_stat1",
        const=print_stat1_with_count,
        default=print_stat1_without_count,
        help="show the numbers of files and lines",
    )
    parser.add_argument(
        "-I", action="store_true", dest="ignore_binary", help="ignore binary files"
    )
    parser.add_argument(
        "-i",
        "--ignore-case",
        action="store_const",
        dest="ext_convert",
        const=lambda x: x.upper(),
        default=lambda x: x,
        help="ignore case the extensions",
    )
    return parser


def parse_arguments():
    return argument_parser().parse_args()


def git_grep(env):
    tree = env.tree
    option = "-Ic" if env.ignore_binary else "-c"
    return subprocess.check_output(
        ["git", "grep", option, "", tree], encoding="utf-8"
    ).splitlines()


SPLIT_PATTERN = re.compile(r"^(?:[^:]+):(.+):([^:]+)$")


def ext_of(env, filename):
    return env.ext_convert(os.path.splitext(filename)[1])


def stat_of(env, line):
    _ext_of = partial(ext_of, env)
    match = re.match(SPLIT_PATTERN, line)
    if match == None:
        raise RuntimeError("未知の文字列です。")
    filepath, line = match.group(1, 2)
    return {_ext_of(filepath): {"file": 1, "line": int(line)}}


def merge_stats(stat1, stat2):
    result = deepcopy(stat1)
    for ext in list(stat2):
        if ext in result:
            result[ext]["file"] += stat2[ext]["file"]
            result[ext]["line"] += stat2[ext]["line"]
        else:
            result[ext] = stat2[ext].copy()
    return result


def count_lines(env):
    _stat_of = partial(stat_of, env)
    return reduce(merge_stats, map(_stat_of, git_grep(env)))


def print_stat1_with_count(ext, stat1):
    print(f"{ext}:{stat1['file']}:{stat1['line']}")


def print_stat1_without_count(ext, stat1):
    print(f"{ext}")


def print_stat(env, stat):
    for ext in sorted(list(stat)):
        env.print_stat1(ext, stat[ext])


def ft(env):
    print_stat(env, count_lines(env))


def main():
    ft(parse_arguments())


if __name__ == "__main__":
    main()
