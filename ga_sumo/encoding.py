import xml.etree.ElementTree as ET

def encode_add_xml(ADD_XML, i, duration):
    add_xml = ET.parse(ADD_XML)
    additional = add_xml.getroot()
    for j, phase in enumerate(additional.iter('phase')):
        if j % 2 == 0:
            phase.set('duration', str(duration[j//2]))
        else:
            phase.set('duration', '5')
    if i == 'optimal':
        add_path = i + ".add.xml"
    else:
        add_path = str(i) + ".add.xml"
    add_xml.write(add_path)
    return add_path

def encode_sumocfg(SUMOCFG, i, add_path):
    sumocfg = ET.parse(SUMOCFG)
    configuration = sumocfg.getroot()
    if i == 'optimal':
        configuration.find('input/additional-files').set('value', add_path)
        configuration.find('output/tripinfo-output').set('value', i +".tripinfo.xml")
        configuration.find('output/fcd-output').set('value', i +".fcd.xml")
        sumocfg_path = i + ".sumocfg"
    else:
        configuration.find('input/additional-files').set('value', add_path)
        configuration.find('output/tripinfo-output').set('value', str(i)+".tripinfo.xml")
        configuration.find('output/fcd-output').set('value', str(i)+".fcd.xml")
        sumocfg_path = str(i) + ".sumocfg"
    sumocfg.write(sumocfg_path)
    return sumocfg_path