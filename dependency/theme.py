from inquirer.themes import Default
from blessings import Terminal


class Theme(Default):
    """Determines the cli theme.
    """
    __term = Terminal()

    def __init__(self):
        super().__init__()
        self.Question.mark_color = self.__term.red
        self.Question.brackets_color = self.__term.red
        self.Question.default_color = self.__term.normal
        self.Checkbox.selection_color = self.__term.green
        self.Checkbox.selection_icon = '≫'
        self.Checkbox.selected_icon = ' ⬢'
        self.Checkbox.selected_color = self.__term.yellow + self.__term.bold
        self.Checkbox.unselected_color = self.__term.norlam
        self.Checkbox.unselected_icon = '⬡'
