# coding: utf-8
from subprocess import run
from dependency.installer import Installer
from dependency.status import Status
from dependency.theme import Theme
from inquirer import Checkbox, prompt
import argparse
import getpass


class Main:
    """This is the Main class of Starter project
    """
    def __init__(self):
        self.__s = Status()
        self.__default = None
        self.__choices = None
        self.__package = 'packages.csv'

        self.__helper = "Script that helps you to install easily your " \
                        "favorite packages. It knows how to use apt, snap, " \
                        "deb, repo. apt - apt packages, snap - snap packages," \
                        "deb - deb file and it needs the file link," \
                        "repo - package name and repository name." \
                        "There are a few special like, bash(oh-my-bash)," \
                        " and sdkman."
        self.__package_help = ".csv file of the required packages. The file should" \
                              " look like this (every package in a new line): " \
                              "<manager>,<package>,<other>"
        self.__def_package_help = ".csv file of the selected by default packages. " \
                                  "Should look like this (every package in a new " \
                                  "line): <package_name>"

        self.__parser = argparse.ArgumentParser(description=self.__helper)
        self.__parser.add_argument('-p', '--packages', help=self.__package_help,
                                   required=False, default=self.__package)
        self.__parser.add_argument('-d', '--default', help=self.__def_package_help,
                                   required=False, default='')
        self.__argument = self.__parser.parse_args()

        if self.__argument.default != '':
            self.__default = self.__db_list(
                self.__file_reader(
                    self.__argument.default))

        self.__welcome = """Welcome to Starter!!!
        This project is made by Chris, to make program 
        installation easier when Ubuntu is freshly installed.
        """
        self.__helper = "▲ - Move up, ▼ - Move down, ▶ - Select item, " \
                        "◀ - Deselect item, \n SPACE - Select/Deselect item," \
                        " ENTER - Confirm, Ctrl + C - Cancel\n "

    @staticmethod
    def __file_reader(file):
        """Reads the file and creates list.

        :return: list of packages
        """
        packages = []
        with open(file, 'r') as f:
            for line in f:
                line = line.strip('\n').rsplit(',')
                packages.append(line)
        return packages

    def __select(self, chosen):
        """Select the chosen applications from the database.

        :param chosen: list of chosen application
        """
        file = self.__file_reader(self.__argument.packages)
        for request in chosen:
            for item in file:
                if request in item:
                    Installer().install(item)

    @staticmethod
    def __db_list(file):
        """Checks the packages file for Package names.

        :param file: List[List[str]] list of packages which contains its attrib
        :return: list of Package name
        """
        apps = []
        for item in file:
            if len(item) > 1:
                apps.append(item[1])
            else:
                apps.append(item[0])
        apps.sort()
        return apps

    def __checkbox(self):
        """Creates the checkbox which one to choose from.
        """
        question = [Checkbox(
            'applications',
            message="What programs do you want to install?",
            choices=self.__db_list(
                self.__file_reader(
                    self.__argument.packages)),
            default=self.__default
        )]
        chosen = prompt(question, theme=Theme())
        self.__select(chosen['applications'])

    def main(self):
        """Main function initializing application.
        """
        try:
            self.__choices = self.__db_list(
                self.__file_reader(
                    self.__argument.packages))
            run('clear')
            print(self.__welcome)
            print(self.__helper)
            getpass.getpass('Press {} to continue...'.format(
                self.__s.colored('Yellow', 'ENTER')))
            self.__checkbox()
        except FileNotFoundError:
            self.__parser.print_help()
        except TypeError:
            pass
        except KeyboardInterrupt:
            print('\b\b  ')
            print('\nCancelled by user\n')


if __name__ == "__main__":
    Main().main()
