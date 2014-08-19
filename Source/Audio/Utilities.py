__author__ = 'briannelson'
import numpy as np
import pyaudio
import datetime


class Utilities:
    def __init__(self):
        """
        Constructor
        """

    @staticmethod
    def get_second_of_audio(audio):
        CHUNK = 1000

        audio_device = pyaudio.PyAudio()
        CHUNKS_PER_SECOND = int(audio.SamplingRate / CHUNK)

        audio_output = np.zeros(audio.SamplingRate, audio.NumberFormat)

        try:
            audio_device = pyaudio.PyAudio()

            stream = audio_device.open(format=audio.AudioFormat,
                                       channels=1,
                                       rate=audio.SamplingRate,
                                       input=True,
                                       frames_per_buffer=CHUNK)

            time = datetime.datetime.utcnow()

            current_sample_position = 0

             #Read a second worth of data
            for i in range(0, CHUNKS_PER_SECOND):
                try:

                    data = stream.read(CHUNK)
                    result = Utilities.array_from_bytes(data, audio.SampleBytes, audio.AudioFormat)

                    channel1 = result['Channel1']
                    for j in range(0, CHUNK):
                        audio_output[current_sample_position] = channel1[j]
                        current_sample_position += 1
                except:
                    current_sample_position += CHUNK
        finally:
            #close the audio stream
            stream.stop_stream()
            stream.close()
            audio_device.terminate()

        return { "Time": time, "Data": audio_output}

    @staticmethod
    def array_from_bytes(data, sample_width, data_type):
        data_length = len(data)
        remainder = data_length % sample_width

        if remainder == 0:
            reading_count = data_length // sample_width

            channel1 = np.zeros(reading_count, dtype=data_type)

            current_position = 0

            for x in range(0, reading_count):
                byte_array = bytearray(sample_width)
                bytearray.zfill(byte_array, sample_width)

                for y in range(0, sample_width):
                    byte_array[y] = data[current_position]
                    current_position += 1

                if data_type == np.int16 or data_type == np.int32:
                    channel1[x] = int.from_bytes(byte_array, byteorder='little', signed=True)
                else:
                    channel1[x] = float.from_bytes(byte_array, byteorder='little', signed=True)


            return {'Channel1': channel1 }
        else:
            return None


    @staticmethod
    def deinterleave(data, sample_width, data_type):
        channel_count = 2
        data_length = len(data)
        remainder = data_length % (sample_width * channel_count)

        if remainder == 0:
            reading_count = data_length // (sample_width * channel_count)

            channel1 = np.zeros(reading_count, dtype=data_type)
            channel2 = np.zeros(reading_count, dtype=data_type)
            current_position = 0

            for x in range(0, reading_count):
                byte_array = bytearray(sample_width)
                bytearray.zfill(byte_array, sample_width)

                for y in range(0, sample_width):
                    byte_array[y] = data[current_position]
                    current_position += 1

                if data_type == np.int16 or data_type == np.int32:
                    channel1[x] = int.from_bytes(byte_array, byteorder='little', signed=True)
                else:
                    channel1[x] = float.from_bytes(byte_array, byteorder='little', signed=True)

                bytearray.zfill(byte_array, sample_width)
                for y in range(0, sample_width):
                    byte_array[y] = data[current_position]
                    current_position += 1

                if data_type == np.int16 or data_type == np.int32:
                    channel2[x] = int.from_bytes(byte_array, byteorder='little', signed=True)
                else:
                    channel2[x] = float.from_bytes(byte_array, byteorder='little', signed=True)

            return {'Channel1': channel1, 'Channel2': channel2}
        else:
            return None

