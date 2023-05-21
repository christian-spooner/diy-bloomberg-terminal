import diy_bbt.providers.settings as settings
from diy_bbt.controllers.base import Base


# Controller class for 'settings' section
class Settings(Base):
    def __init__(self):
        super().__init__()
        self.controllers.update(
            {
                "keys": settings.keys,
                "k": settings.keys,
            }
        )

    def get_source(self):
        return settings

    def execute(self, cmd):
        if len(cmd) == 1:
            return self.name()
        elif cmd[1] in self.controllers:
            func = self.controllers[cmd[1]]
            return func()
        return self.unknown(cmd)
