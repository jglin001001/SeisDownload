import obspy

st = obspy.read('Seis_mseed_download_station/1_XF_B01.mseed')

#  复制原始stream后对其进行带通滤波
st_filt = st.copy()
tr = st_filt.filter('bandpass',freqmin=0.03,freqmax=2,corners=4,zerophase=True)
tr.plot(equal_scale=False)
