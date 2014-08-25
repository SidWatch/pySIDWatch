__author__ = 'briannelson'

from SID.Utilities import ConfigUtility
from SID.Controllers import SendToSidWatchServerController

config = ConfigUtility.load('/FileSync/Projects/Projects/RadioAstronomy/Source/SidWatch/Config/sidwatch.cfg')

controller = SendToSidWatchServerController(config)

controller.start()

