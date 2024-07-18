import xml.etree.ElementTree as et

class ObjectValue:
    def __init__(self, net_path, rou_path, sumocfg_path, tripinfo_path):
        net_xml = et.parse(net_path)
        rou_xml = et.parse(rou_path)
        sumocfg = et.parse(sumocfg_path)
        tripinfo_xml = et.parse(tripinfo_path)
        
        self.net = net_xml.getroot()
        self.routes = rou_xml.getroot()
        self.configuration = sumocfg.getroot()
        self.tripinfos = tripinfo_xml.getroot()
        
        self.V = len(self.tripinfos.findall('tripinfo'))
        self.C = len(self.routes.findall('vehicle')) - self.V

    def journeyTime(self):
        total_journey_time = 0.0
        for tripinfo in self.tripinfos.findall('tripinfo'):
            total_journey_time += float(tripinfo.get('duration'))
        return total_journey_time
    
    def waitingTime(self):
        total_waiting_time = 0.0
        for tripinfo in self.tripinfos.findall('tripinfo'):
            total_waiting_time += float(tripinfo.get('waitingTime'))
        """
        !! 缺少 時限內未抵達目的地的車輛 的waiting time
        """
        return total_waiting_time

    def simulationTime(self):
        return float(self.configuration.find('.//time/end').get('value'))
    
    def Cr(self):
        cr = 0.0
        for tlLogic in self.net.findall('tlLogic'):
            for phase in tlLogic.findall('phase'):
                state = phase.get('state')
                try:
                    ratio = (state.count('G') + state.count('g')) / state.count('r')
                except ZeroDivisionError:
                    print("\n!! ERROR: ZERO DIVISION !!\n")
                cr += int(phase.get('duration')) * ratio
        return cr
    
    def value(self):
        return (self.journeyTime() + self.waitingTime() + self.C * self.simulationTime()) / (self.V ** 2 + self.Cr())

obj = ObjectValue('final.net.xml', 'final.rou.xml', 'test.sumocfg', 'tripinfo.xml')
print(obj.value())