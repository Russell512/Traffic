import xml.etree.ElementTree as ET

def encode_add_xml(position, i):
    add_xml = ET.parse('final.add.xml')
    additional = add_xml.getroot()
    for j, phase in enumerate(additional.iter('phase')):
        if j % 2 == 0:
            phase.set('duration', str(position[j//2]))
        else:
            phase.set('duration', '5')
    add_file_name = str(i) + ".add.xml"
    add_xml.write(add_file_name)
    return add_file_name

def encode_sumocfg(add_file_name, i):
    sumocfg = ET.parse('test.sumocfg')
    configuration = sumocfg.getroot()
    add_file_name = str(i) + ".add.xml"
    configuration.find('input/additional-files').set('value', add_file_name)
    sumocfg_file_name = str(i) + ".sumocfg"
    sumocfg.write(sumocfg_file_name)
    return sumocfg_file_name