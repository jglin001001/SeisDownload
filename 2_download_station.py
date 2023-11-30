from obspy import UTCDateTime
from obspy.clients.fdsn import Client

# 创建 FDSN 客户端，这里使用 Download_seis
client = Client("IRIS")

# 下载指定区域内的地震台站
min_latitude = 16
max_latitude = 17
min_longitude = 149
max_longitude = 150
sta_start_time = UTCDateTime('2012-1-30')
sta_end_time = UTCDateTime('2012-3-31')

inventory = client.get_stations(minlatitude=min_latitude, maxlatitude=max_latitude,
                                minlongitude=min_longitude, maxlongitude=max_longitude,
                                starttime=sta_start_time, endtime=sta_end_time)
print(inventory)

with open('station_info.txt', 'w') as file:
    for network in inventory:
        for station in network:
            file.write(f"{network.code}, {station.code}, {station.latitude}, {station.longitude}, {station.elevation}\n")