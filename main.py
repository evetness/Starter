# coding: utf-8
from subprocess import run
from dependency.installer import Installer
from dependency.status import Status
import sys
import cutie
import argparse


class Main:
    """This is the Main class of Starter project
    """

    def __init__(self):
        self._stat = Status()
        self._default_file = None
        self._package_file = 'packages.csv'

        self._HELPER = "Script that helps you to install easily your " \
                       "preferred packages. It uses apt, snap, " \
                       "deb, repo. apt - apt packages, snap - snap packages, " \
                       "deb - deb file and it needs the file link, " \
                       "repo - package name and repository name."
        self._PACKAGE_HELP = ".csv file of the required packages. The file should" \
                             " look like this (every package in a new line): " \
                             "<manager>,<package_name>,<other>"
        self._DEFAULT_HELP = ".csv file of the selected packages by default. " \
                             "Should look like this (every package in a new " \
                             "line): <package_name>"

        self._parser = argparse.ArgumentParser(description=self._HELPER)
        self._parser.add_argument('-p', '--packages',
                                  help=self._PACKAGE_HELP,
                                  required=False,
                                  default=self._package_file)
        self._parser.add_argument('-d', '--default',
                                  help=self._DEFAULT_HELP,
                                  required=False,
                                  default='')
        self._arguments = self._parser.parse_args()

        try:
            if self._arguments.default != '':
                self._default_file = list(range(len(self._file_reader(
                    self._arguments.default))))

            self._package_file = self._file_reader(self._arguments.packages)
        except FileNotFoundError:
            print(self._stat.colored('Red', '\nFile not found!!!\n'))
            sys.exit(1)

        self._WELCOME = """Welcome to Starter!!!
        This project is made by Chris, to make program 
        installation easier when Ubuntu is freshly installed.
        """
        self._GUIDE = "▲ - Move up, ▼ - Move down, Select - Select/Deselect item,\n" \
                      "ENTER - Confirm, Ctrl + C - Cancel\n"

    @staticmethod
    def _file_reader(file):
        """Reads the file and creates list.

        :return: list of packages
        """
        packages = []
        with open(file, 'r') as f:
            for line in f:
                line = line.strip('\n').rsplit(',')
                packages.append(line)
        return packages

    def _select(self, chosen):
        """Select the chosen applications from the database.

        :param chosen: list of chosen application
        """
        for request in chosen:
            for item in self._package_file:
                if request in item:
                    Installer().install(item)

    @staticmethod
    def _names(file):
        """Checks the packages file for Package names.

        :param file: List[List[str]] list of packages which contains its attrib
        :return: list of Package name
        """
        apps = []
        for item in file:
            if len(item) > 1:
                apps.append(item[1])
        apps.sort()
        return apps

    def _prompt_app_list(self):
        """Creates the checkbox which one to choose from.
        """
        print("Choose which applications to install:")
        package_names = self._names(self._package_file)
        selection = cutie.select_multiple(package_names,
                                          ticked_indices=self._default_file,
                                          deselected_unticked_prefix=' ⬡ ',
                                          deselected_ticked_prefix=self._stat.colored('Green', ' ⬢ '),
                                          selected_unticked_prefix=self._stat.colored('Yellow', ' ⬡ '),
                                          selected_ticked_prefix=self._stat.colored('Yellow', ' ⬢ '),
                                          hide_confirm=True)
        chosen = []
        for i in selection:
            chosen.append(package_names[i])
        self._select(chosen)

    def main(self):
        """Main function initializing application.
        """
        run('clear')
        print(self._WELCOME)
        print(self._GUIDE)
        if cutie.prompt_yes_or_no("Do you want to {}?".format(self._stat.colored('Yellow', 'continue')),
                                  selected_prefix=self._stat.colored('Yellow', ' ▶ '),
                                  deselected_prefix=' ▷ '):
            self._prompt_app_list()


if __name__ == "__main__":
    Main().main()
