from dependency.status import Status
from subprocess import run, Popen, PIPE


class Installer:
    """Installer class which chooses of the package manager
    """
    __s = Status()

    def __apt(self, pkg):
        """Installs the required package with apt package manager

        :param pkg: str package name
        """
        self.__s.status(pkg, 'install')
        run(['sudo', 'apt', 'install', pkg])

    def __snap(self, pkg, oth=None):
        """Installs the required package with snap manager.

        :param pkg: str package name
        :param oth: str OPTIONAL classic
        """
        if oth == 'classic':
            self.__s.status(pkg, 'install')
            run(['sudo', 'snap', 'install', pkg, '--' + oth])
        else:
            self.__s.status(pkg, 'install')
            run(['sudo', 'snap', 'install', pkg])

    def __deb(self, oth):
        """Checks if gDebi is installed, and installs
        the required package with gDebi manager

        :param oth: str .deb package link
        """
        installer = Popen('dpkg -l gdebi', shell=True, stdout=PIPE)
        installer.wait()
        if installer.returncode == 1:
            self.__s.status('gdebi', 'install')
            self.install('gdebi')

        pkgName = oth.rsplit('/', 1)[-1]
        self.__s.status(pkgName, 'install')
        run(['wget', oth])
        run(['sudo', 'gdebi', pkgName, '-n'])
        run(['rm', '-rf', pkgName])

    def __repo(self, pkg, oth):
        """Adds the required repository and installs the package.

        :param pkg: str package name
        :param oth: str repository
        """
        name = oth.rsplit(':', 1)[-1]
        self.__s.status(name, 'add')
        run(['sudo', 'add-apt-repository', '-y', oth])
        self.update()
        self.install(['apt', pkg])

    def update(self):
        """Method that updates the system.
        """
        self.__s.status('system', 'update')
        run(['sudo', 'apt', 'update', '-y'])

    def install(self, packages):
        """Calls the required package manager method.

        :param packages: list package properties
        """
        mgr = packages[0].lower()
        pkg = packages[1].lower() if len(packages) >= 2 else None
        oth = packages[2] if len(packages) == 3 else None
        if mgr == 'apt':
            self.__apt(pkg)
        elif mgr == 'snap':
            self.__snap(pkg, oth)
        elif mgr == 'deb':
            self.__deb(oth)
        elif mgr == 'repo':
            self.__repo(pkg, oth)
