#!/usr/bin/env python
import argparse
from fileHandler import init_files
import sys
from main import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="treeNote")
    parser.add_argument("-i", "--init", default=False, action="store_true")
    args = parser.parse_args()
    if args.init:
        init_files()
    main()
