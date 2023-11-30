# SeisDownload
Creator: Jungle LIN, Yuechu WU

Email: jglin001001@foxmail.com

中文：地震事件数据下载
1. download_event.  从iris上下载指定时间及最低震级的地震目录。当然，你也可以下载指定区域或者指定位置一定震中距的地震数据，该目录将保存为txt格式文件（示例中台站信息保存为‘earthquake_catalog.txt’），该文件包含事件序号、时间、位置信息、深度及震级。
   
2. download_station.  从iris上下载指定区域内所有台站信息。台站信息将保存为txt文件（示例中台站信息保存为‘station_info.txt’），该文件包含台网、台站、台站位置坐标及深度。
   
3. download_seis.  根据上述的文件，从iris上下载txt文件内台站信息的所有通道的地震信号。该文件运行过程中可能会产生警告，但并不影响程序使用，所下载的地震数据将去除仪器响应，分别以图片形式、mseed格式保存在你所指定的文件夹中（示例中，去除仪器响应后的mseed文件保存在‘Seis_mseed_download_station’，波形图片文件保存在‘Seis_wave_download_station’）。另外，你可以从iris中指定采样率下载数据，取消注释tr.resample即可。
   
4. filter_seis.  将已经去除仪器响应后的文件进行滤波。

In English: Download earthquake event data
1. download_event. Download the earthquake directory with the specified time and minimum magnitude from Iris. Of course, you can also download earthquake data from a specified area or location with a certain epicenter distance. The directory will be saved as a txt format file (in the example, station information will be saved as 'earthquake_catalog.txt'), which includes event sequence number, time, location information, depth, and magnitude.
   
2. download_station. Download all station information within the specified area from Iris. The station information will be saved as a txt file (in the example, the station information will be saved as 'station_info.txt'), which includes the station network, station location coordinates, and depth.

3. download_seis. According to the above file, download the seismic signals for all channels of station information in the txt file from Iris. The file may generate warnings during operation, but it does not affect program usage. The downloaded seismic data will remove the instrument response and be saved in the folder you specified in image format and mseed format (for example, the mseed file after removing the instrument response is saved in 'Seis_mseed_download_station', and the waveform image file is saved in 'Seis_wave_download_station'). Additionally, you can download data at a specified sampling rate from Iris and uncomment tr.resample.
   
4. filter_seis. Filter the file that has already removed the instrument response.
