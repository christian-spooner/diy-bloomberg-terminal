import diy_bbt.providers.home as home
from diy_bbt.controllers.base import Base


# Controller class for 'home' section
class Home(Base):
    def __init__(self):
        super().__init__()

    def get_source(self):
        return home
