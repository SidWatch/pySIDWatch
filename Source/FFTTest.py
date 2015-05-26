__author__ = 'briannelson'

from SID.Utilities import FileUtility
from SID.Utilities import FrequencyUtility

data = FileUtility.read_audio('./20141014_150150_042628.txt')

Pxx, frequencies = FrequencyUtility.process_psd(data)

FileUtility.dump_psd('./psd.txt', frequencies, Pxx)