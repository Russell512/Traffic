import os
from generateSumocfg import generate_sumocfg

# SIM_NAME: 車流檔案共用前綴
# SIM_TIME: 模擬時間
SIM_NAME = 'rs'
SIM_TIME = 500

# SRC: '.add.xml', '.net.xml', '.rou.xml'資料來源路徑
# HIS: 優化過程生成檔案路徑
# OPT: 優化結果路徑
SRC_PATH = 'source\\'
HIS_PATH = 'history\\'
OPT_PATH = 'optimal\\'

# 生成資料夾
if not os.path.isdir(HIS_PATH):
    os.mkdir(HIS_PATH)
if not os.path.isdir(OPT_PATH):
    os.mkdir(OPT_PATH)

# 在SRC生成'.sumocfg'檔案
generate_sumocfg(SRC_PATH, SIM_NAME, SIM_TIME)

NET_XML = SIM_NAME + '.net.xml'
ROU_XML = SIM_NAME + '.rou.xml'
ADD_XML = SIM_NAME + '.add.xml'
SUMOCFG = SIM_NAME + '.sumocfg'

# 複製'.net.xml'和'.rou.xml'至HIS和OPT資料夾(不會做修改)
import shutil
shutil.copyfile(SRC_PATH + NET_XML, HIS_PATH + NET_XML)
shutil.copyfile(SRC_PATH + ROU_XML, HIS_PATH + ROU_XML)
shutil.copyfile(SRC_PATH + NET_XML, OPT_PATH + NET_XML)
shutil.copyfile(SRC_PATH + ROU_XML, OPT_PATH + ROU_XML)

# 從'.rou.xml'獲取車輛總數
# 從'.add.xml'獲取需優化秒數的數量
import xml.etree.ElementTree as ET

rou_xml = ET.parse(SRC_PATH + ROU_XML)
routes = rou_xml.getroot()
VEHICLES = len(routes.findall('vehicle'))

add_xml = ET.parse(SRC_PATH + ADD_XML)
additional = add_xml.getroot()
PHASE = 0
for phase in additional.iter('phase'):
    if(phase.get('state').find('y') == -1):
        PHASE += 1