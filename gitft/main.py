#!/usr/bin/env python3

from functools import reduce
import argparse
import copy
import os
import re
import subprocess


def ext_of(filename: str) -> str:
    return os.path.splitext(filename)[1]


def prepare_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("tree", nargs="?", default="HEAD")
    return parser


def parse_arguments():
    parser = prepare_argument_parser()
    return parser.parse_args()


def git_grep(tree: str):
    return subprocess.check_output(
        ["git", "grep", "-Ic", "", tree], encoding="utf-8"
    ).splitlines()


SPLIT_PATTERN = re.compile(r"^(?:[^:]+):(.+):([^:]+)$")


def stat_from(line):
    match = re.match(SPLIT_PATTERN, line)
    if match == None:
        raise RuntimeError("未知の文字列です。")
    filepath, line = match.group(1, 2)
    return {ext_of(filepath): {"file": 1, "line": int(line)}}


def merge_stat(stat1, stat2):
    result = copy.deepcopy(stat1)
    for key in list(stat2):
        if key in result:
            result[key]["file"] += stat2[key]["file"]
            result[key]["line"] += stat2[key]["line"]
        else:
            result[key] = stat2[key].copy()
    return result


def count_lines(tree):
    return reduce(merge_stat, map(stat_from, git_grep(tree)))


def print_stat(stat):
    for key in sorted(list(stat)):
        print(f"{key}:{stat[key]['file']}:{stat[key]['line']}")


def ft(tree):
    print_stat(count_lines(tree))


def main():
    arguments = parse_arguments()
    ft(arguments.tree)


main()
