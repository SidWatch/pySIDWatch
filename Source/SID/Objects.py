__author__ = 'briannelson'
import pyaudio
import numpy as np

class Site:

    def __init__(self, values_dictionary):
        """
        Constructor
        """
        self.MonitorId = values_dictionary["MonitorId"]
        self.Name = values_dictionary["Name"]
        self.Latitude = values_dictionary["Latitude"]
        self.Longitude = values_dictionary["Longitude"]
        self.UtcOffset = values_dictionary["UtcOffset"]
        self.Timezone = values_dictionary["Timezone"]

        pass


class Station:

    def __init__(self, values_dictionary):
        """
        Constructor
        """
        self.CallSign = values_dictionary["CallSign"]
        self.Color = values_dictionary["Color"]
        self.Frequency = values_dictionary["Frequency"]


class Logging:
    def __init__(self, values_dictionary):
        """
        Constructor
        """

        self.FilenameFormat = values_dictionary["FilenameFormat"]
        self.Folder = values_dictionary["Folder"]
        self.TraceLevel = values_dictionary["TraceLevel"]


class Config:
    def __init__(self, values_dictionary):
        """
        Constructor
        """

        self.Site = Site(values_dictionary["Site"])
        self.Audio = Audio(values_dictionary["Audio"])
        self.Logging = Logging(values_dictionary["Logging"])
        self.SidWatch = SidWatch(values_dictionary["SidWatch"])

        self.Stations = []
        stations = values_dictionary["Station"]
        for station_dictionary in stations:
            station = Station(station_dictionary)
            station.MonitoredBin = int(((int(station.Frequency) * self.SidWatch.NFFT) / self.Audio.SamplingRate))
            self.Stations.append(station)

        pass


class Audio:
    def __init__(self, values_dictionary):
        """
        Constructor
        """

        self.SamplingRate = values_dictionary["SamplingRate"]
        self.SamplingFormat = values_dictionary["SamplingFormat"]

        if self.SamplingFormat == 16:
            self.AudioFormat = pyaudio.paInt16
            self.NumberFormat = np.int16
            self.SampleBytes = 2
        elif self.SamplingFormat == 24:
            self.AudioFormat = pyaudio.paInt24
            self.NumberFormat = np.int32
            self.SampleBytes = 3
        else:
            self.AudioFormat = pyaudio.paFloat32
            self.NumberFormat = np.float32
            self.SampleBytes = 4


class SidWatch:
    def __init__(self, values_dictionary):
        """
        Constructor
        :param values_dictionary:
        :return:
        """

        self.AutoUpload = values_dictionary["AutoUpload"]
        self.DeleteAfterUpload = values_dictionary["DeleteAfterUpload"]
        self.DataFolder = values_dictionary["DataFolder"]
        self.ReadingPerFile = values_dictionary["ReadingPerFile"]
        self.NFFT = values_dictionary["NFFT"]
        self.SaveRawData = values_dictionary["SaveRawData"]
        self.SaveFrequencies = values_dictionary["SaveFrequencies"]
        self.SaveStationData = values_dictionary["SaveStationData"]

        self.Username = values_dictionary["Username"]
        self.Password = values_dictionary["Password"]
        self.SidWatchServerUrl = values_dictionary["SidWatchServerUrl"]

        if (self.NFFT is None) or (self.NFFT == 0) :
            self.NFFT = 1024