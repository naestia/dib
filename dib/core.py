# -*- coding: utf-8 -*-

# python std lib
import logging
import os
import re
import sys
from pathlib import Path
from subprocess import PIPE, Popen

# subgit imports
from dib.constants import *

# 3rd party imports
import curses
from curses import wrapper
from packaging import version
from packaging.specifiers import SpecifierSet


log = logging.getLogger(__name__)


class DIB():
    def __init__(self):
        self.working_dir = Path().cwd()

    def run_c(self):
        wrapper(self.main)

    def main(self, stdscr):
        stdscr.clear
        stdscr.refresh()
        stdscr.addstr(str(self.working_dir))
        stdscr.getch()

    def ls(self, flags=None):
        print("This will be a version of the classic ls command")
    
    def cd(self):
        print("This will be a version of the classic cd command")

    def find(self):
        print("This will be a version of the classic find command")
