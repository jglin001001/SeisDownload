# SeisDownload（实现波形展示显示P/S到时）
Creator: Jungle LIN, Yuechu WU

Email: jglin001001@foxmail.com

中文：地震事件数据下载
1. download_event.  从iris上下载指定时间及最低震级的地震目录。当然，你也可以下载指定区域或者指定位置一定震中距的地震数据，该目录将保存为txt格式文件（示例中台站信息保存为‘earthquake_catalog.txt’），该文件包含事件序号、时间、位置信息、深度及震级。
   
2. download_station.  从iris上下载指定区域内所有台站信息。台站信息将保存为txt文件（示例中台站信息保存为‘station_info.txt’），该文件包含台网、台站、台站位置坐标及深度。

3. resp. 从iris下载地震台站的仪器响应文件（之前尝试边下载地震数据边下载仪器响应文件用于去除仪器响应，发现有时会出现下载错误，可能是网络连接问题）

4. download_seis.  根据上述的文件，从iris上下载txt文件内台站信息的所有通道的地震信号。该文件运行过程中可能会产生警告，但并不影响程序使用，所下载的地震数据将去除仪器响应，分别以图片形式、mseed格式保存在你所指定的文件夹中（示例中，去除仪器响应后的mseed文件保存在‘Seis_mseed_download_station’，波形图片文件保存在‘Seis_wave_download_station’）。另外，你可以从iris中指定采样率下载数据，取消注释tr.resample即可。另外，还提供了去均值、去线性趋势、波行尖灭以及滤波的操作，取消注释相关行即可。

5. sac.  将上述的mseed格式文件转换为sac格式文件，命名方式为：{network}.{station}.{channel}.{quality}.{start_time.year}.{start_time.julday}.{start_time.hour}{start_time.minute}{start_time.second}.SAC
   
6. 在sac头段中添加lat、lon。

7. 测试是否添加成功lat、lon。

In English: Download earthquake event data
1. download_event. Download the earthquake directory with the specified time and lowest magnitude from iris. Of course, you can also download seismic data of a specified area or a certain epicentral distance at a specified location. The directory will be saved as a txt format file (in the example, the station information is saved as 'earthquake_catalog.txt'). The file contains event number, time, and location. Information, depth and magnitude.
   
2. download_station. Download all station information in the specified area from iris. The station information will be saved as a txt file (in the example, the station information is saved as ‘station_info.txt’). The file contains the station network, station, station location coordinates and depth.

3. resp. Download the instrument response file of the seismic station from iris (I previously tried to download the instrument response file while downloading seismic data to remove the instrument response, and found that sometimes download errors would occur, which may be a network connection problem)

4. download_seis. According to the above file, download the seismic signals of all channels of the station information in the txt file from iris. Warnings may be generated during the running of this file, but it does not affect the use of the program. The downloaded seismic data will have the instrument response removed and will be saved in the folder you specify in image form and mseed format (in the example, the instrument response will be removed The final mseed file is saved in 'Seis_mseed_download_station', and the waveform image file is saved in 'Seis_wave_download_station'). In addition, you can download data from iris by specifying the sampling rate and uncommenting tr.resample. In addition, it also provides the operations of removing the mean, removing the linear trend, wave line pinching and filtering. Just uncomment the relevant lines.

5. sac. Convert the above mseed format file to sac format file. The naming method is: {network}.{station}.{channel}.{quality}.{start_time.year}.{start_time.julday}.{start_time .hour}{start_time.minute}{start_time.second}.SAC
   
6. Add lat and lon to the sac header.

7. Test whether lat and lon are added successfully.
