import xml.etree.ElementTree as ET

class ObjectValue:
    def __init__(self, net_path, rou_path, add_path, sumocfg_path, tripinfo_path, fcd_path):
        net_xml = ET.parse(net_path)        # Cr()
        rou_xml = ET.parse(rou_path)        # Total number of vehicles
        add_xml = ET.parse(add_path)
        sumocfg = ET.parse(sumocfg_path)    # simulationTime()
        tripinfo_xml = ET.parse(tripinfo_path)  # journeyTime()
        fcd_xml = ET.parse(fcd_path) # Floating Car Data (FCD) # waitingTime()
        
        self.net = net_xml.getroot()
        self.routes = rou_xml.getroot()
        self.additional = add_xml.getroot()
        self.configuration = sumocfg.getroot()
        self.tripinfos = tripinfo_xml.getroot()
        self.fcd = fcd_xml.getroot()
        
        self.V = len(self.tripinfos.findall('tripinfo'))
        self.C = len(self.routes.findall('vehicle')) - self.V
        self.simulation_time = float(self.configuration.find('.//time/end').get('value'))

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
        for tlLogic in self.additional.findall('tlLogic'):
            for phase in tlLogic.findall('phase'):
                state = phase.get('state')
                try:
                    ratio = (state.count('G') + state.count('g')) / state.count('r')
                except ZeroDivisionError:
                    print("\n!! ERROR: ZERO DIVISION !!\n")
                cr += int(phase.get('duration')) * ratio
        return cr
    
    def getValue(self):
        return (self.journeyTime() + self.waitingTime() + self.C * self.simulation_time) / (self.V ** 2 + self.Cr())

if __name__ == '__main__':
    obj = ObjectValue('final.net.xml', 'final.rou.xml', 'final.add.xml', 'test.sumocfg', 'tripinfo.xml', 'fcd.xml')
    print(obj.getValue())