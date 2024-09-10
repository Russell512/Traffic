import xml.etree.ElementTree as ET
from configuration import VEHICLES, SIM_TIME, SRC_PATH, ADD_XML

class Ratio:
    ratios = []
    def __init__(self, add_path):
        add_xml = ET.parse(add_path)
        additional = add_xml.getroot()
        for phase in additional.iter('phase'):
            state = phase.get('state')
            green = (state.count('G') + state.count('g'))
            red = state.count('r')
            if red != 0:
                ratio = green / red
            elif green != 0:
                ratio = 1
            else:
                ratio = 0
            self.ratios.append(ratio)
Ratio(SRC_PATH + ADD_XML)

class ObjectValue:
    def __init__(self, add_path, tripinfo_path, fcd_path):
        add_xml = ET.parse(add_path)        # Cr()
        tripinfo_xml = ET.parse(tripinfo_path)  # journeyTime()
        fcd_xml = ET.parse(fcd_path)        # Floating Car Data (FCD) # waitingTime()
        
        self.additional = add_xml.getroot()
        self.tripinfos = tripinfo_xml.getroot()
        self.fcd = fcd_xml.getroot()
        
        self.V = len(self.tripinfos.findall('tripinfo'))
        self.C = VEHICLES - self.V

    # Calculate the total journey time of all vehicles that arrive their destination
    def journeyTime(self):
        total_journey_time = 0.0
        for tripinfo in self.tripinfos.findall('tripinfo'):
            total_journey_time += float(tripinfo.get('duration'))
        return total_journey_time
    
    def waitingTime(self):
        total_waiting_time = 0.0
        for vehicle in self.fcd.iter('vehicle'):
            if float(vehicle.get('speed')) < 0.1:
                total_waiting_time += 1
        # Depart speed is zero but should not be counted in waiting time
        return total_waiting_time - (self.V + self.C)
    
    def Cr(self):
        cr = 0.0
        i = 0
        for phase in self.additional.iter('phase'):
            cr += int(phase.get('duration')) * Ratio.ratios[i]
            i += 1
        return cr
    
    def evaluate(self):
        return (self.journeyTime() + self.waitingTime() + self.C * SIM_TIME) / (self.V ** 2 + self.Cr())\
        