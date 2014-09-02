__author__ = 'briannelson'

from SID.Utilities import ConfigUtility
from SIDClient.Controllers import SidDataController

config = ConfigUtility.load('/FileSync/Source/Other/SidWatch/pySidWatch/Source/Config/sidwatch.cfg')

controller = SidDataController(config)

controller.start()
