__author__ = 'briannelson'

from SID.Utilities import ConfigUtility
from SIDClient.Controllers import SendToSidWatchServerController

config = ConfigUtility.load('./Config/sidwatch.cfg')

controller = SendToSidWatchServerController(config)

controller.start()

