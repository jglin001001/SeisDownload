from obspy import UTCDateTime
from obspy.clients.fdsn import Client

# 创建 FDSN 客户端，这里使用 Download_seis
client = Client("IRIS")

# 定义查询参数
start_time = UTCDateTime("2012-01-30")
end_time = UTCDateTime("2012-03-31")
min_magnitude = 7.0
## 下载指定区域
min_latitude = None # 指定区域纬度
max_latitude = None
min_longitude = None # 指定区域经度
max_longitude = None
## 下载指定位置一定震中距的地震数据
sta_latitude = None # 位置纬度
sta_longitude = None # 位置经度
min_radius = None # 最小震中距
max_radius = None # 最大震中距

# 获取地震目录
catalog = client.get_events(starttime=start_time, endtime=end_time, minmagnitude=min_magnitude,
                            minlatitude=min_latitude, maxlatitude=max_latitude,minlongitude=min_longitude, maxlongitude=max_longitude,
                            latitude=sta_latitude, longitude=sta_longitude, minradius=min_radius, maxradius= max_radius)

# 输出地震目录
print(catalog)
# 准备保存到文本文件的字符串
catalog_txt = ""
event_number = 1
for event in catalog:
    origin = event.origins[0]
    magnitude = event.magnitudes[0]
    event_info = f"{event_number}, Time | {origin.time}, Location | ({origin.latitude}/{origin.longitude}), Depth | {origin.depth} m, Magnitude | {magnitude.mag}\n"
    event_number += 1
    catalog_txt += event_info

# 保存到文本文件
with open("earthquake_catalog.txt", "w") as file:
    file.write(catalog_txt)
