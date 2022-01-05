import geopandas as gpd
import shapely.geometry

streets = gpd.read_file('data/GPS.nosync/Streets/Streets.shp')

street = streets.loc[0]
b = street['geometry'].boundary
data = [[street['OBJECTID'], street['OBJECTID'], street['OBJECTID'] * 10 + 1, street['OBJECTID'] * 10 + 2, street['Shape__Len'], b[0].x, b[0].y, b[1].x, b[1].y, street['geometry']]]
dict_points = {(b[0].x, b[0].y):street['OBJECTID'] * 10 + 1}
max_id = len(streets)
count = 0
for index, street in streets.iterrows():
  id_1 = 0
  id_2 = 0
  start = (0.0, 0.0)
  end = (0.0, 0.0)

  if (len(street['geometry'].boundary) == 2):
    boundary = street['geometry'].boundary
    id_1 = street['OBJECTID'] * 10 + 1
    id_2 = street['OBJECTID'] * 10 + 2
    start = (boundary[0].x, boundary[0].y)
    end = (boundary[1].x, boundary[1].y)
  else:
    continue
  if dict_points.get(start) == None:
    dict_points[start] = id_1
  else:
    id_1 = dict_points[start]

  if dict_points.get(end) == None:
    dict_points[end] = id_2
  else:
    id_2 = dict_points[end]
  data.append([street['OBJECTID'], street['OBJECTID'], id_1, id_2, street['Shape__Len'], boundary[0].x, boundary[0].y, boundary[1].x, boundary[1].y, street['geometry']])

df = gpd.GeoDataFrame(data, columns = ['_uid_', 'id', 'source', 'target', 'cost','x1','y1','x2','y2','geometry'])
df.to_file('data/GPS.nosync/street_nodes_dual.shp')