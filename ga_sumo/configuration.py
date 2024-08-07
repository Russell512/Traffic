NET_XML = 'final.net.xml'
ROU_XML = 'final.rou.xml'
ADD_XML = 'final.add.xml'
SUMOCFG = 'final.sumocfg'

import xml.etree.ElementTree as ET
sumo_xml = ET.parse(SUMOCFG)
configuration = sumo_xml.getroot()
SIM_TIME = int(configuration.find('time/end').get('value'))