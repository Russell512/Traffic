import os

NET_XML = 'final.net.xml'
ROU_XML = 'final.rou.xml'
ADD_XML = 'final.add.xml'
SUMOCFG = 'final.sumocfg'

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