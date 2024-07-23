import xml.etree.ElementTree as ET

def encode_net_xml(position, i):
    net_xml = ET.parse('final.net.xml')
    net = net_xml.getroot()
    for j, phase in enumerate(net.iter('phase')):
        if j % 2 == 0:
            phase.set('duration', str(position[j//2]))
        else:
            phase.set('duration', '5')
    net_file_name = str(i) + ".net.xml"
    net_xml.write(net_file_name)
    return net_file_name

def encode_sumocfg(net_file_name, i):
    sumocfg = ET.parse('test.sumocfg')
    configuration = sumocfg.getroot()
    net_file_name = str(i) + ".net.xml"
    configuration.find('input/net-file').set('value', net_file_name)
    sumocfg_file_name = str(i) + ".sumocfg"
    sumocfg.write(sumocfg_file_name)
    return sumocfg_file_name