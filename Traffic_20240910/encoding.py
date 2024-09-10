import xml.etree.ElementTree as ET
from configuration import SRC_PATH, HIS_PATH, OPT_PATH, ADD_XML, SUMOCFG

class State:
    no_y = []
    def __init__(self, add_path):
        add_xml = ET.parse(add_path)
        additional = add_xml.getroot()
        for phase in additional.iter('phase'):
            if phase.get('state').find('y') == -1:
                self.no_y.append(True)
            else:
                self.no_y.append(False)
State(SRC_PATH + ADD_XML)

# 依照傳入的i值與duration生成'.add.xml'和'.sumocfg'
def encode(i, duration):
    # 從SRC獲取檔案以修改
    add_xml = ET.parse(SRC_PATH + ADD_XML)
    additional = add_xml.getroot()
    sumocfg = ET.parse(SRC_PATH + SUMOCFG)
    configuration = sumocfg.getroot()

    idx = 0
    j = 0
    for phase in additional.iter('phase'):
        if State.no_y[idx] == True:
            phase.set('duration', str(duration[j]))
            j += 1
        else:
            phase.set('duration', '5')
        idx += 1

    if isinstance(i, int):
        i_add_xml = str(i) + '.add.xml'
        add_xml.write(HIS_PATH + i_add_xml)

        i_sumocfg = str(i) + '.sumocfg'
        configuration.find('input/additional-files').set('value', i_add_xml)
        configuration.find('output/tripinfo-output').set('value', str(i) + '.tripinfo.xml')
        configuration.find('output/fcd-output').set('value', str(i) + '.fcd.xml')
        sumocfg.write(HIS_PATH + i_sumocfg)
        return i_sumocfg
    else:
        opt_add_xml = i + '.add.xml'
        add_xml.write(OPT_PATH + opt_add_xml)

        opt_sumocfg = i + '.sumocfg'
        configuration.find('input/additional-files').set('value', opt_add_xml)
        configuration.find('output/tripinfo-output').set('value', i + '.tripinfo.xml')
        configuration.find('output/fcd-output').set('value', i + '.fcd.xml')
        sumocfg.write(OPT_PATH + opt_sumocfg)
        return opt_sumocfg