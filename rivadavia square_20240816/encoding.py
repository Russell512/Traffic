import xml.etree.ElementTree as ET
from configuration import SRC_PATH, HIS_PATH

def encode(ADD_XML, SUMOCFG, i, duration):
    add_xml = ET.parse(ADD_XML)
    additional = add_xml.getroot()
    sumocfg = ET.parse(SUMOCFG)
    configuration = sumocfg.getroot()

    j = 0
    for phase in additional.iter('phase'):
        if phase.get('state').find('y') == -1:
            phase.set('duration', str(duration[j]))
            j += 1
        else:
            phase.set('duration', '5')

    if i == 'optimal':
        add_path = i + '.add.xml'
        add_xml.write(add_path)

        sumocfg_path = i + '.sumocfg'
        configuration.find('input/net-file').set('value', SRC_PATH + configuration.find('input/net-file').get('value'))
        configuration.find('input/route-files').set('value', SRC_PATH + configuration.find('input/route-files').get('value'))
        configuration.find('input/additional-files').set('value', add_path)
        configuration.find('output/tripinfo-output').set('value', i + '.tripinfo.xml')
        configuration.find('output/fcd-output').set('value', i + '.fcd.xml')
        sumocfg.write(sumocfg_path)
    else:
        add_path = str(i) + '.add.xml'
        add_xml.write(HIS_PATH + add_path)

        configuration.find('input/additional-files').set('value', add_path)
        configuration.find('output/tripinfo-output').set('value', str(i) + '.tripinfo.xml')
        configuration.find('output/fcd-output').set('value', str(i) + '.fcd.xml')
        sumocfg_path = str(i) + '.sumocfg'
        sumocfg.write(HIS_PATH + sumocfg_path)
    
    return sumocfg_path