import os

NET_XML = 'hamasing.net.xml'
ROU_XML = 'hamasing.rou.xml'
ADD_XML = 'hamasing.add.xml'
SUMOCFG = 'hamasing.sumocfg'

SRC_PATH = 'source\\'
HIS_PATH = 'history\\'
if not os.path.isdir(HIS_PATH):
    os.mkdir(HIS_PATH)

import shutil
shutil.copyfile(SRC_PATH + NET_XML, HIS_PATH + NET_XML)
shutil.copyfile(SRC_PATH + ROU_XML, HIS_PATH + ROU_XML)

NET_XML = SRC_PATH + NET_XML
ROU_XML = SRC_PATH + ROU_XML
ADD_XML = SRC_PATH + ADD_XML
SUMOCFG = SRC_PATH + SUMOCFG

import xml.etree.ElementTree as ET

rou_xml = ET.parse(ROU_XML)
routes = rou_xml.getroot()
VEHICLES = len(routes.findall('vehicle'))

sumocfg = ET.parse(SUMOCFG)
configuration = sumocfg.getroot()
SIM_TIME = int(configuration.find('time/end').get('value'))

add_xml = ET.parse(ADD_XML)
additional = add_xml.getroot()
PHASE = 0
for phase in additional.iter('phase'):
    if(phase.get('state').find('y') == -1):
        PHASE += 1