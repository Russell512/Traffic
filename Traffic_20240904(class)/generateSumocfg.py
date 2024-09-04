import xml.etree.ElementTree as ET

def generate_sumocfg(SRC_PATH, SIM_NAME, SIM_TIME):
    keys = ['net-file', 'route-files', 'additional-files', 'tripinfo-output', 'fcd-output', 'begin', 'end']
    values = [SIM_NAME+'.net.xml', SIM_NAME+'.rou.xml', SIM_NAME+'.add.xml', SIM_NAME+'.tripinfo.xml', SIM_NAME+'.fcd.xml', '0', str(SIM_TIME)]

    configuration = ET.Element('configuration')
    input = ET.Element('input')
    output = ET.Element('output')
    time = ET.Element('time')

    for i in range(len(keys)):
        element = ET.Element(keys[i])
        element.set('value', values[i])
        if i <= 2:
            input.append(element)
        elif 3 <= i <= 4:
            output.append(element)
        else:
            time.append(element)

    configuration.append(input)
    configuration.append(output)
    configuration.append(time)

    tree = ET.ElementTree(configuration)
    tree.write(SRC_PATH+SIM_NAME+'.sumocfg', encoding='utf-8', xml_declaration=True)

    print('"' + SIM_NAME + '.sumocfg" has been generated.')