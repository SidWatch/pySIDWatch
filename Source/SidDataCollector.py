__author__ = 'briannelson'

from SID.Utilities import ConfigUtility
from SID.Controllers import SidDataController

config = ConfigUtility.load('/FileSync/Projects/Projects/RadioAstronomy/Source/SidWatch/Config/sidwatch.cfg')

controller = SidDataController(config)

controller.start()
