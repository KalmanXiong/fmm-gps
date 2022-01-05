import geopandas as gpd
import pyarrow
import pandas as pd
import os

def write_file(filename, info):
  text_file = open(filename, "w")
  text_file.write(info)
  text_file.close()

target_2631 = pd.read_parquet('data/GPS.nosync/filter/Sonoma_2631_new', engine='pyarrow')

start_index = 199567
start_id = target_2631.loc[start_index]['caid']
print("start index: %d, caid: %s" %(0, start_id))
end = 400000
count = 999
is_first = True
res = 'LINESTRING('
for index in range(start_index, end):
  data_id = target_2631.loc[index]['caid']
  single_data = target_2631.loc[index]
  is_data_valid = (single_data['latitude'] < 38.85) & (single_data['latitude'] > 38.099) & (single_data['longitude'] < -122.35) & (single_data['longitude'] > -123.55)
  if data_id != start_id:
    res+=')'
    if (index - start_index) > 49:
      write_file('data/GPS.nosync/points/' + str(count) +'-points.txt', res)
    is_first = True
    res = 'LINESTRING('
    count+=1
    start_index = index
    start_id = data_id
  lat = float(single_data['latitude'])
  lon = float(single_data['longitude'])
  if is_data_valid:
    if is_first:
      is_first = False
      res+= (str(lon) + ' ' + str(lat))
    else:
      res+= (',' + str(lon) + ' ' + str(lat))