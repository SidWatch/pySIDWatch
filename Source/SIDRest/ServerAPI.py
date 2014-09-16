__author__ = 'briannelson'
import requests

class SidWatchAPI:
    def __init__(self, config):
        """
        Constructor
        """
        self.Config = config

    def get_upload_credentials(self):
        username = self.Config.SidWatch.Username
        password = self.Config.SidWatch.Password

        url = self.Config.SidWatch.SidWatchServerUrl + "accesskey"

        custom_headers = {'sidwatch-emailaddress': username,
                          'sidwatch-password': password}
        response = requests.get(url, headers=custom_headers)
        access_key = response.json()

        if 'error' in access_key:
            return None
        else:
            ak = access_key['accesskey']
            sk = access_key['secretkey']
            bucket = access_key['bucketname']

            return {'AccessKey':ak, 'SecretKey':sk, 'Bucket':bucket }