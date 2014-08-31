__author__ = 'briannelson'
import urllib3


class SidWatchAPI:
    def __init__(self, config):
        """
        Constructor
        """
        self.Config = config

    def get_upload_credentials(self):
        username = self.Config.SidWatch.Username
        password = self.Config.SidWatch.Password

        url = self.Config.SidWatch.SidWatchServerUrl + "uploadaccess"

        http = urllib3.PoolManager()

        headers = { 'sidwatch-emailaddress':'brian@treegecko.com', 'sidwatch-password':'tester' }
        response = http.request('GET', url, headers)

        print(response.data)

        pass