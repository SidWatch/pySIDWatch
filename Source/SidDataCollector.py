__author__ = 'briannelson'

from SID.Utilities import ConfigUtility
from SID.Utilities import HDF5Utility
from SID.Utilities import DateUtility
from SID.Utilities import FrequencyUtility

from Audio.Utilities import Utilities as AudioUtilities
import datetime as dt
import os
import time as threadtime


config = ConfigUtility.load('/FileSync/Projects/Projects/RadioAstronomy/Source/SidWatch/Config/sidwatch.cfg')

done = False

now = dt.datetime.utcnow()
current_date = now.date()
next_date_time = DateUtility.get_next_run_time(now)

sample_count = 0

print(current_date)

data_file = None
filename_prefix = None
filename_temp = None
filename_final = None

raw_data_group = None
stations_group = None
frequency_spectrum_data_group = None

while not done:
    current_time = dt.datetime.utcnow()

    if current_time > next_date_time:
        if sample_count == 0:
            filename_prefix = config.SidWatch.DataFolder + \
                              "{0}_{1}".format(config.Site.Name, current_time.strftime("%Y%m%d_%H%M"))
            filename_temp = filename_prefix + ".tmp"
            filename_final = filename_prefix + ".h5"

            result = HDF5Utility.open_file(filename_temp, config)

            data_file = result["File"]
            raw_data_group = result["RawDataGroup"]
            stations_group = result["StationsGroup"]
            frequency_spectrum_data_group = result["FrequencySpectrumDataGroup"]

            print("Opened new file")

        result = AudioUtilities.get_second_of_audio(config.Audio)

        time = result["Time"]
        data = result["Data"]

        #store the raw data
        dataset_name = time.strftime("%Y%m%d_%H%M%S_%f")
        if raw_data_group is not None:
            HDF5Utility.add_raw_data_set(raw_data_group, dataset_name, time, config.Audio.NumberFormat, data)

        #process the data for power spectral density
        Pxx, frequencies = FrequencyUtility.process_psd(data, config.SidWatch.NFFT, config.Audio.SamplingRate)

        #store the frequency spectrum
        if frequency_spectrum_data_group is not None:
            HDF5Utility.add_frequency_spectrum(frequency_spectrum_data_group, dataset_name, time, frequencies, Pxx)

        if stations_group is not None:
            #Store the values for each monitored station
            for station in config.Stations:
                signal_strength = Pxx[station.MonitoredBin]
                HDF5Utility.add_signal_strength(station, stations_group, dataset_name, time, signal_strength)


        #determine the next date time to monitor
        next_date_time = DateUtility.get_next_run_time(current_time)
        sample_count += 1
        print("{0} - Read data".format(dataset_name))

        #Determine if it is time for a new file
        if sample_count >= config.SidWatch.ReadingPerFile:
            raw_data_group = None
            processed_data_group = None
            station_group = None
            HDF5Utility.close_file(data_file)
            os.rename(filename_temp, filename_final)

            sample_count = 0
            print("closed file")

    threadtime.sleep(.05)


pass