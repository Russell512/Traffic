import numpy as np

from evaluate import ObjectValue
from configuration import *

class Solution:
    def __init__(self, lower_bound, upper_bound, phase):
        self.duration = np.random.randint(lower_bound, upper_bound + 1, size=phase)
        self.value = 0

    def evaluate(self, i):
        add_path = HIS_PATH + str(i) + '.add.xml'
        tripinfo_path = HIS_PATH + str(i) + '.tripinfo.xml'
        fcd_path = HIS_PATH + str(i) + '.fcd.xml'
        obj = ObjectValue(add_path, tripinfo_path, fcd_path)
        self.value = obj.evaluate()