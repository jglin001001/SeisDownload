from obspy import UTCDateTime, Stream, read, read_inventory, taup
from obspy.clients.fdsn import Client
from obspy.geodetics import locations2degrees
import matplotlib.pyplot as plt
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
    event_depth_str = parts[3].split('|')[1].split('m')[0].strip()
    event_depth = float(event_depth_str)/1000
    event_mag = parts[4].split('|')[1].strip()
    return int(number), UTCDateTime(time_str), float(lat), float(lon), float(event_depth), float(event_mag)

def parse_station_line(line):
    parts = line.split(',')
    network_str = parts[0]
    station_str = parts[1].strip()
    station_lat = parts[2].strip()
    station_lon = parts[3].strip()
    station_depth_str = parts[4].split('-')[1].strip()
    station_depth = float(station_depth_str)/1000
    return str(network_str), str(station_str), float(station_lat),float(station_lon),float(station_depth)

def calculate_arrival_times(event_lat, event_lon, event_depth, station_lat, station_lon, station_depth):
    distance = locations2degrees(event_lat,event_lon,station_lat,station_lon)
    model = taup.TauPyModel('ak135')
    arrivals = model.get_travel_times(source_depth_in_km=event_depth, distance_in_degree=distance,
                                      phase_list=['P','S'], receiver_depth_in_km=station_depth)
    p_arrival, s_arrival = None, None
    for arrival in arrivals:
        if arrival.name == 'P':
            p_arrival = arrival.time
        if arrival.name == 'S':
            s_arrival = arrival.time
    return p_arrival, s_arrival

def download_and_process_data(event_line, station_lines):
    event_number, event_time, event_lat, event_lon, event_depth, event_mag = parse_event_line(event_line)
    client = Client("IRIS")

    for station_line in station_lines:
        network, station, station_lat, station_lon, station_depth = parse_station_line(station_line)
        print(network,station)
        location = "--"
        channels = ['HH*', 'EL*', 'BH*', 'HDH', 'EDH']
        start_time = event_time
        end_time = event_time + 30 * 60
        combined_stream = Stream()
        for channel in channels:
            try:
                st = client.get_waveforms(network, station, location, channel, start_time, end_time, attach_response=True)
                print(st)
                if st:
                    resp_file_path = f'./RESP/{network}.{station}.{channel}.xml'
                    inventory = read_inventory(resp_file_path)
                    pre_filt = (0.005, 0.006, 30.0, 35.0)
                    st.remove_response(inventory=inventory, output='DISP', pre_filt=pre_filt)
                    start_time_str = st[0].stats.starttime.strftime("%Y%m%d_%H%M%S")
                    st = st.resample(sampling_rate=5.0)
                    st = st.detrend("demean")
                    st = st.detrend("linear")
                    st = st.taper(max_percentage=0.05, type="hann")
                    st = st.filter('bandpass', freqmin=0.05, freqmax=2, corners=4, zerophase=True)
                    combined_stream += st
            except Exception:
                pass

        if combined_stream:
            mseed_file_path = os.path.join(mseed_folder_name, f'{network}.{station}_{start_time_str}.mseed')
            combined_stream.write(mseed_file_path, format="MSEED")
            photo_file_path = os.path.join(photo_folder_name, f'{network}.{station}_{start_time_str}.png')
            plot_waveforms_with_markers(combined_stream, station_lat, station_lon, station_depth, event_time, event_lat, event_lon, event_depth, event_mag, photo_file_path)

def plot_waveforms_with_markers(stream, station_lat, station_lon,station_depth, event_time, event_lat, event_lon, event_depth, event_mag, outfile):
    station_lat = station_lat
    station_lon = station_lon
    station_depth = station_depth  # 假设台站深度为0，或者使用相应的真实值
    epicentral_distance = locations2degrees(event_lat, event_lon, station_lat, station_lon)
    annotation_text = (f"Station: {stream[0].stats.station}, "
                       f"Event: {event_time},"
                       f"Distance: {epicentral_distance:.2f} degrees, "
                       f"Magnitude: {event_mag}, "
                       f"Filter Band: 0.05-2 Hz")
    p_arrival, s_arrival = calculate_arrival_times(event_lat, event_lon, event_depth, station_lat, station_lon,
                                                   station_depth)

    # 计算相对于事件时间的P波和S波到达时间
    if p_arrival is not None:
        p_time = event_time + p_arrival
    else:
        p_time = None
    if s_arrival is not None:
        s_time = event_time + s_arrival
    else:
        s_time = None

    # 绘图
    fig, axes = plt.subplots(nrows=len(stream), ncols=1, figsize=(12, 2 * len(stream)), sharex=True)
    plt.suptitle(annotation_text, fontsize=12, y = 0.95)
    if len(stream) == 1:
        axes = [axes]
    for i, tr in enumerate(stream):
        relative_times = tr.times(type='relative', reftime=event_time)
        axes[i].plot(relative_times, tr.data, color='black', label=tr.stats.channel)
        if p_time:
            axes[i].axvline((p_time - event_time), color='green', linestyle='-', label='P wave')
        if s_time:
            axes[i].axvline((s_time - event_time), color='red', linestyle='--', label='S wave')
        axes[i].legend(loc='upper left')

    for ax in axes:
        handles, labels = ax.get_legend_handles_labels()
        # 仅保留第一个图例项（假设这是通道名）
        if handles:
            ax.legend(handles=[handles[0]], labels=[labels[0]], loc='upper left')
    # 在整个图表的右上方添加P波和S波的统一图例
    fig.legend(handles=[plt.Line2D([], [], color='green', linestyle='-', label='P wave'),
                        plt.Line2D([], [], color='red', linestyle='--', label='S wave')],
               loc='upper right')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(outfile)
    plt.close(fig)

# 读取地震目录文件和台站文件
with open("earthquake_catalog.txt", "r") as file:
    event_lines = file.readlines()

with open("station_info.txt", "r") as file:
    station_lines = file.readlines()

# 创建波形图文件夹,使用自己命名的文件夹
photo_folder_name = 'Seis_wave_download_station'
os.makedirs(photo_folder_name, exist_ok=True)
# 创建mseed文件夹，使用自己命名的文件夹
mseed_folder_name = 'Seis_mseed_download_station'
os.makedirs(mseed_folder_name, exist_ok=True)
# 仪器响应
resp_folder_name = './RESP'
os.makedirs(resp_folder_name, exist_ok=True)

# 遍历每个地震事件并处理
for event_line in event_lines:
    download_and_process_data(event_line, station_lines)
