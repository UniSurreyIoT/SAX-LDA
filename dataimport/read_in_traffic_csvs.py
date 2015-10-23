__author__ = 'citypulse-dp'
from dataimport.dataPandas import Stream

#give filepath with all traffic csv files
def read_in_streams(filepath):
    traffic_streams = {}
    for file_name in os.listdir(filepath):
        if file_name.endswith('.csv'):
                traffic_streams[sensor_id] = Stream(lda_config.data_path, file_name)
    return traffic_stream