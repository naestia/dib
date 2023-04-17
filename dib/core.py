# -*- coding: utf-8 -*-

# python std lib
import logging
import os
import sys
from multiprocessing import Pool
from pathlib import Path

# subgit imports
from dib.constants import *

# 3rd party imports
import curses
from curses import wrapper

import time


log = logging.getLogger(__name__)


class DIB():
    def __init__(self):
        self.working_dir = Path.cwd()
        self.ignore_directory = [
            ".git",
            ".tox",
            "__pycache__",
            ".idea",
            ".virtualenvs",
            ".local",
            ".oh-my-zsh",
            ".cache"
        ]

    def run(self):
        return wrapper(self.main)
    
    def _create_iterable_path_search(self, path):
        for item in self.ignore_directory:
            if item not in str(path):
                return path

    def _search_file_system(self, string_list):
        for string in string_list:
            self.path_list = []
            for path in self.iter_list:
                ignored_path = False
                for item in self.ignore_directory:
                    if item in str(path):
                        ignored_path = True

                if path.is_dir() and not ignored_path:
                    path_str = str(path)
                    relative_path = path_str.replace(str(self.working_dir), "")

                    if path_str != str(self.working_dir):

                        if string in relative_path:

                            if relative_path and relative_path not in self.path_list:
                                self.path_list.append(relative_path)

            self.path_dict[string] = self.path_list

        return self.path_dict

    def _get_match(self):
        self.match_list = []
        self.bad_match = False
        self.path_dict = self._search_file_system(self.string_list)

        for string in self.string_list:

            if len(string) > 1:

                for match in self.path_dict.get(string):
                    all_match = True
                    for i in self.string_list:
                        if i not in match:
                            all_match = False

                    if match not in self.match_list:
                        if len(self.match_list) == self.height - 4:
                            break
                        elif all_match:
                            self.match_list.append(match)

                if not self.bad_match:
                    self._update_match_text()

                self._refresh_pad()

    def _update_match_text(self):
        for index, item in enumerate(self.match_list):
            if self.index_to_match == index:
                self.pad.attron(curses.color_pair(1))
                self.pad.addstr(index, 0, item + (" " * (self.width - len(item))))
                self.chosen_path = item
                self.pad.attroff(curses.color_pair(1))
                self._refresh_pad()
            else:
                self.pad.addstr(index, 0, item)
                for i in self.string_list:
                    if len(i) > 1:
                        if len(self.current_word) > 1:
                            self.starting_index = item.find(i[0])
                        self.pad.attron(curses.color_pair(2))
                        self.pad.addstr(index, self.starting_index, i)
                        self.pad.attroff(curses.color_pair(2))

                self._refresh_pad()

    def _update(self):
        self._get_match()
        self._update_match_text()

    def _refresh_pad(self):
        self.pad.refresh(0, 0, 2, 0, (self.height - 2), self.width)

    def main(self, stdscr):
        self.screen = stdscr
        self.string_to_match = ""
        self.bad_match = False
        self.index_to_match = -1
        self.match_list = []
        self.chosen_path = ""
        self.current_word = ""
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_RED, self.screen.getbkgd())

        

        while True:
            key = self.screen.getkey()
            self.height, self.width = self.screen.getmaxyx()
            self.pad = curses.newpad((self.height - 2), self.width)
            self.debug_pad = curses.newpad(1, self.width)
            self.string_list = []
            self.path_list = []
            self.path_dict = {}

            if not self.string_to_match:
                self.index_to_match = -1

            if key[:3] != "KEY" and key not in IGNORE_KEYS:
                self.string_to_match += key
                self.current_word += key
                self.string_list = self.string_to_match.split(" ")
                for item in self.string_list:
                    if not item:
                        self.string_list.remove(item)

                self._update()

            if key == "KEY_BACKSPACE":

                self.string_to_match = self.string_to_match[:-1]
                if self.string_to_match:
                    if self.string_to_match[-1] != " " and self.string_to_match.rfind(" ") != -1:
                        self.current_word = self.string_to_match[self.string_to_match.rfind(" "):]
                    else:
                        self.current_word = self.string_to_match[:]
                else:
                    self.current_word = ""

                self.string_list = self.string_to_match.split(" ")
                for item in self.string_list:
                    if not item:
                        self.string_list.remove(item)

                self.screen.clear()
                self.screen.refresh()
                self._update()

            elif key == " ":
                self.current_word = ""
                self.index_to_match = -1
                # TODO: self.starting_index = 0

            elif key == "KEY_DOWN":
                if self.index_to_match < len(self.match_list) - 1:
                    self.index_to_match += 1
                self._update_match_text()

            elif key == "KEY_UP":
                if self.index_to_match > 0:
                    self.index_to_match -= 1
                self._update_match_text()

            elif key == "\n":
                if self.index_to_match >= 0:
                    if self.chosen_path:
                        return self.chosen_path

                elif self.current_word == "quit()":
                    sys.exit()

            self.debug_pad.clear()
            self.debug_pad.addstr(f"String to match: {self.string_to_match} | Current word: {self.current_word}")
            self.debug_pad.refresh(0, 0, (self.height - 1), 0, self.height, self.width)

            self.screen.addstr(0, 0, self.string_to_match)

    def ls(self, flags=None):

        with Pool(8) as pool:
             self.iter_list = pool.map(self._create_iterable_path_search, Path(self.working_dir).glob("**/*"))

        print(len(self.iter_list))
        path = self.run()
        os.system(f"ls {flags} .{path}")
