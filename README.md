# SeisDownload
Creator: Jungle LIN, Yuechu WU

Email: jglin001001@foxmail.com

地震事件数据下载
1. download_event.  从iris上下载指定时间及最低震级的地震目录。当然，你也可以下载指定区域或者指定位置一定震中距的地震数据，该目录将保存为txt格式文件（示例中台站信息保存为‘earthquake_catalog.txt’），该文件包含事件序号、时间、位置信息、深度及震级。
   
2. download_station.  从iris上下载指定区域内所有台站信息。台站信息将保存为txt文件（示例中台站信息保存为‘station_info.txt’），该文件包含台网、台站、台站位置坐标及深度。
   
3. download_seis.  根据上述的文件，从iris上下载txt文件内台站信息的所有通道的地震信号。该文件运行过程中可能会产生警告，但并不影响程序使用，所下载的地震数据将去除仪器响应，分别以图片形式、mseed格式保存在你所指定的文件夹中（示例中，去除仪器响应后的mseed文件保存在‘Seis_mseed_download_station’，波形图片文件保存在‘Seis_wave_download_station’）。另外，你可以从iris中指定采样率下载数据，取消注释tr.resample即可。
   
4. filter_seis.  将已经去除仪器响应后的文件进行滤波。
