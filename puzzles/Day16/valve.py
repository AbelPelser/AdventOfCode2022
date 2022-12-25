from typing import List


class Valve:
    def __init__(self, name, flow_rate, target_valve_names: List[str]):
        self.name = name
        self.flow_rate = flow_rate
        self.target_valve_names = target_valve_names

    def __repr__(self):
        return f'{self.name} with flowrate {self.flow_rate}'
