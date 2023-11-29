import obspy

st = obspy.read('1_XF_B01.mseed')
st.plot()