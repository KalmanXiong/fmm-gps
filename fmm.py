from fmm import Network,NetworkGraph,FastMapMatch,FastMapMatchConfig,UBODT
from fmm import UBODTGenAlgorithm
import pyarrow
import pyarrow.parquet as pq
import os

def getPoints(file_path):
    if os.path.isfile(file_path):
        text_file = open(file_path, "r")
        wkt = text_file.read()
        text_file.close()
    return wkt

def save_results(file_base_name, cpath, opath, indices, m_wkt, e_wkt):
  text_file = open(file_base_name + '-cpath.txt', "w")
  text_file.write(cpath)
  text_file.close()
  text_file = open(file_base_name + '-opath.txt', "w")
  text_file.write(opath)
  text_file.close()
  text_file = open(file_base_name + '-indices.txt', "w")
  text_file.write(indices)
  text_file.close()
  text_file = open(file_base_name + '-m_wkt.txt', "w")
  text_file.write(m_wkt)
  text_file.close()
  text_file = open(file_base_name + '-e_wkt.txt', "w")
  text_file.write(e_wkt)
  text_file.close()

def get_sub_result(input_path, output_path, index):
  input_source = input_path + str(index) + '-points.txt'
  out_dir = output_path + 'sub-result-' + str(index)
  if (os.path.isfile(input_source)) & (not os.path.isdir(out_dir)):
    wkt = getPoints(input_source)
    result = model.match_wkt(wkt,fmm_config)
    if len(list(result.cpath)) > 0:
      #dir = output_path + 'sub-result-' + str(index)
      os.mkdir(out_dir)
      output_base = out_dir + '/' + str(index)
      save_results(output_base,str(list(result.cpath)), str(list(result.opath)),str(list(result.indices)),result.mgeom.export_wkt(),result.pgeom.export_wkt())
      print('index %d sucess!' % index)
    else:
      print('index %d failed!' % index)



  #network = Network("data/edges.shp")
network = Network('data/GPS.nosync/street_nodes_dual.shp')
print "Nodes {} edges {}".format(network.get_node_count(),network.get_edge_count())
print(network)
graph = NetworkGraph(network)

ubodt_gen = UBODTGenAlgorithm(network,graph)

status = ubodt_gen.generate_ubodt("data/GPS.nosync/street_dual_ubodt_new.txt", 4, binary=False, use_omp=True)
print status

ubodt = UBODT.read_ubodt_csv("data/GPS.nosync/street_dual_ubodt_new.txt")
model = FastMapMatch(network,graph,ubodt)

k = 64
radius = 10
gps_error = 50
fmm_config = FastMapMatchConfig(k,radius,gps_error)

for index in range(5,999):
  get_sub_result('data/GPS.nosync/points/', 'data/GPS.nosync/output/', index)