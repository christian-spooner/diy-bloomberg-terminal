from abc import ABC, abstractmethod


class Base(ABC):
    """
    Parent class for all controller classes.
    """

    def __init__(self):
        self.controllers = {
            "clear": self.clear,
            "cl": self.clear,
            "back": self.back,
            "b": self.back,
            "help": self.help,
            "h": self.help,
            "name": self.name,
        }

    @abstractmethod
    def get_source(self):
        pass

    def execute(self, cmd):
        if cmd[0] in self.controllers:
            func = self.controllers[cmd[0]]
            return func()
        return self.unknown(cmd)

    # Command functions
    def back(self):
        return "BACK"

    def clear(self):
        return "CLEAR"

    def help(self):
        return self.get_source().help()

    def name(self):
        return f"/{self.get_source().string()}"

    def unknown(self, cmd):
        text = " ".join(cmd)
        return f"command not found: {text}"
