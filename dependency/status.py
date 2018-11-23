class Status:
    """This class is responsible for the status indicator.
    """
    _colors = {
        'Yellow': '\x1b[0;93m',
        'Green': '\x1b[0;92m',
        'Red': '\x1b[0;91m',
        'None': '\x1b[0m'
    }
    """Defined colors.
    """

    def colored(self, color, string):
        """Colorize string.

        :param color: str color name
        :param string: str required string
        :return: str colored string
        """
        return self._colors[color] + string + self._colors['None']

    @staticmethod
    def _lines(string):
        """Creates a long line of dashes.
        Calculates line length from string.

        :param string: str given string
        :return: str dashes
        """
        dashes = 77 - len(string)
        dashes = '-' * dashes
        return dashes

    def status(self, string, stat):
        """Informs the user from the install status.

        :param string: str package name
        :param stat: str status
        """
        if stat == 'update' or stat == 'upgrade':
            stat = self.colored(
                'Green', stat[:1].upper() + stat[1:-1:] + 'ing'
            )
        elif stat == 'install' or stat == 'add':
            stat = self.colored(
                'Yellow', stat[:1].upper() + stat[1:] + 'ing'
            )
        elif stat == 'done':
            stat = self.colored('Green', 'Done')

        res = "{0} {1} {2} {3}".format(
                                    self.colored('Yellow', '[>---'),
                                    stat,
                                    self.colored('Green', string),
                                    self.colored('Yellow', '{0}---<]'.format(
                                        self._lines(stat + string)))
                                       )
        print(res)
