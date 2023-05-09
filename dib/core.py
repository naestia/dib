# -*- coding: utf-8 -*-

# python std lib
import logging
import os
import sys
from pathlib import Path
from subprocess import run

# dib imports
from dib.constants import *

# 3rd party imports
import curses
import pyperclip
from curses import wrapper


log = logging.getLogger(__name__)


class DIB():
    def __init__(self, current_dir=None):
        if not current_dir:
            self.current_dir = Path.cwd()
        else:
            self.current_dir = Path(current_dir)

        self.file_type = "d"
        self.ignore_directory = [
            ".git/",
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

    def _search_file_system(self, string_list):
        path_dict = {}
        for string in string_list:
            self.path_list = []

            if len(string) > 1:
                if self.file_type == "d":
                    for path in self.current_dir.rglob(f"*{string}*/**"):
                        ignored_path = False
                        for item in self.ignore_directory:
                            if item in str(path):
                                ignored_path = True

                        if path.is_dir() and not ignored_path:
                            path_str = str(path)
                            relative_path = path_str.replace(str(self.current_dir), "")

                            if path_str != str(self.current_dir):

                                if string in relative_path:

                                    if relative_path and relative_path not in self.path_list:
                                        self.path_list.append(str(path))
                elif self.file_type == "f":
                    for path in self.current_dir.glob(f"**/*{string}*"):
                        ignored_path = False
                        for item in self.ignore_directory:
                            if item in str(path):
                                ignored_path = True

                        if path.is_file() and not ignored_path:
                            path_str = str(path)
                            relative_path = path_str.replace(str(self.current_dir), "")

                            if path_str != str(self.current_dir):

                                if string in relative_path:

                                    if relative_path and relative_path not in self.path_list:
                                        self.path_list.append(str(path))

                path_dict[string] = list(sorted(self.path_list))

        return dict(sorted(path_dict.items()))

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

                        if all_match:
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

                    if self.file_type == "d":
                        self.starting_index = item.find(i)
                    else:
                        self.starting_index = item.rfind(i)
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
        self.new_list = []
        self.string_to_match = ""
        self.bad_match = False
        self.index_to_match = -1
        self.match_list = []
        self.chosen_path = ""
        self.current_word = ""
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_RED, self.screen.getbkgd())
        while True:
            # Record every keystroke the user does
            key = self.screen.getch()
            self.height, self.width = self.screen.getmaxyx()
            self.pad = curses.newpad((self.height - 2), self.width)
            self.debug_pad = curses.newpad(1, self.width)
            self.string_list = []
            self.path_list = []
            self.path_dict = {}

            if not self.string_to_match:
                self.index_to_match = -1

            if key != "KEY" and key not in IGNORE_KEYS:
                self.string_to_match += chr(key)
                self.current_word += chr(key)
                self.string_list = self.string_to_match.split(" ")
                for item in self.string_list:
                    if not item:
                        self.string_list.remove(item)

                self._update()

            if key == 127 or key == 263:
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
            elif key == 258:
                if self.index_to_match < len(self.match_list) - 1:
                    self.index_to_match += 1
                self._update_match_text()
            elif key == 259:
                if self.index_to_match > 0:
                    self.index_to_match -= 1
                self._update_match_text()
            elif key == 10:
                if self.index_to_match >= 0:
                    if self.chosen_path:
                        return self.chosen_path.replace(" ", "\ ")
                elif self.current_word == "quit()":
                    sys.exit()

            self.screen.addstr(0, 0, self.string_to_match)
            self.debug_pad.clear()
            self.debug_pad.addstr(f"String to match: {self.string_to_match}")
            self.debug_pad.refresh(0, 0, (self.height - 1), 0, self.height, self.width)

    def ls(self, flags=None):
        path = self.run()
        return os.system(f"ls {flags} {path}")

    def cd(self):
        path = self.run()
        dib_folder = Path.home() / ".dib"
        script = "run_cd.sh"
        os.chdir(dib_folder)
        run(["sh", script, path])

    def find(self, flag):
        self.file_type = flag
        path = self.run()
        print(f"\tFound: {path}")
        answer = input("Would you like to copy path to clipboard? [Y/n] >> ").upper()
        if answer == "Y":
            pyperclip.copy(str(path))
        else:
            return 0
