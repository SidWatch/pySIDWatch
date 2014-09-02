__author__ = 'briannelson'

from SID.Utilities import ConfigUtility
from SIDClient.Controllers import SendToSidWatchServerController

config = ConfigUtility.load('/FileSync/Source/Other/SidWatch/pySidWatch/Source/Config/sidwatch.cfg')

controller = SendToSidWatchServerController(config)

controller.start()

