from obspy import UTCDateTime, Stream
from obspy.clients.fdsn import Client
import os

def parse_event_line(line):
    """从文本行解析地震事件信息"""
    parts = line.split(',')
    # 事件编号
    number = parts[0]
    # 时间信息
    time_str = parts[1].split('|')[1].strip()
    # 位置信息
    # 移除 "Location:" 和两端的空格，然后移除括号
    location_part = parts[2].split('|')[1].strip().strip('()')
    location_parts = location_part.split('/')
    if len(location_parts) != 2:
        raise ValueError(f"Invalid location format in line: {line}")
    lat = location_parts[0].strip()
    lon = location_parts[1].strip()

    return int(number), UTCDateTime(time_str), float(lat), float(lon)

def parse_station_line(line):
    parts = line.split(',')
    network_str = parts[0]
    station_str =parts[1]

    return str(network_str), str(station_str)

# 读取地震目录文件
with open("earthquake_catalog.txt", "r") as file:
    lines = file.readlines()

# 读取地震台站文件
with open("station_info.txt", "r") as file:
    station_lines = file.readlines()

# 创建 FDSN 客户端，这里使用 Download_seis
client = Client("IRIS")
# 创建波形图文件夹,使用自己命名的文件夹
photo_folder_name = 'Seis_wave_download_station'
os.makedirs(photo_folder_name, exist_ok=True)
# 创建mseed文件夹，使用自己命名的文件夹
mseed_folder_name = 'Seis_mseed_download_station'
os.makedirs(mseed_folder_name, exist_ok=True)

# 为每个地震事件下载波形数据
for line in lines:
    event_number, event_time, lat, lon = parse_event_line(line)
    print(event_number, event_time, lat, lon)

    for station_line in station_lines:
        network_num, station_num = parse_station_line(station_line)
        print(network_num, station_num)

        # 定义下载参数
        network = network_num  # 替换为目标网络代码
        station = station_num  # 替换为目标台站代码
        location = "--"  # 位置代码，通常是两个连字符
        channels = ['HH*','EL*','BH*']  # 通道代码，例如 "BHZ" 或 "HHZ"
        hydrophone_channels = ['HDH','EDH']
        start_time = event_time - 10 *60  # 事件前10分钟
        end_time = event_time + 60 * 60  # 事件后60分钟
        channel_stream = Stream()
        for channel in hydrophone_channels:
            try:
                hyd_st = client.get_waveforms(network, station, location, channel, start_time, end_time, attach_response=True)
                if hyd_st:
                    channel_stream += hyd_st
            except Exception :
                pass
        for channel in channels:
            try:
                st = client.get_waveforms(network, station, location, channel, start_time, end_time, attach_response=True)
                if st:
                    channel_stream = channel_stream + st
            except Exception :
                pass

        if channel_stream:
            pre_filt = (0.005, 0.006, 30.0, 35.0)  # 定义一个滤波带以防止在反卷积过程中放大噪声
            tr = channel_stream.remove_response(output='DISP', pre_filt=pre_filt) # 去除仪器响应

            # 可选的,可降采样下载相关数据,降采样时取消注释下面这行即可
            # tr = tr.resample(sampling_rate=5.0)
            print(tr)

            photo_file_path = os.path.join(photo_folder_name, f'{event_number}_{network}_{station}.png')
            tr.plot(outfile = photo_file_path,equal_scale=False,format='png')
            mseed_file_path = os.path.join(mseed_folder_name, f'{event_number}_{network}_{station}.mseed')
            tr.write(mseed_file_path, format="MSEED")
