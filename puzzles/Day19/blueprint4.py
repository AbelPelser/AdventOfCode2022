from copy import copy, deepcopy

import math

ROBOTS = ['ore', 'clay', 'obsidian', 'geode']

CACHE = {}


class BlueprintBruteForceNew:
    def __init__(self, blueprint_nr: int, robot_cost: dict[str, dict[str, int]], max_n_minutes=24):
        self.max_n_minutes = max_n_minutes
        self.blueprint_nr = blueprint_nr
        self.robot_cost = robot_cost
        self.n_robots = {robot_type: 1 if robot_type == 'ore' else 0 for robot_type in ROBOTS}
        self.n_materials = {robot_type: 0 for robot_type in ROBOTS}
        self.minute = 0

    def step(self):
        self.minute += 1
        for robot_type, amount in self.n_robots.items():
            self.n_materials[robot_type] += amount

    def get_missing_resources_for_robot(self, robot_type):
        result = {}
        for resource, cost in self.robot_cost[robot_type].items():
            n_available = self.n_materials[resource]
            result[resource] = max(cost - n_available, 0)
        return result

    def get_time_needed_for_resources(self, resource_type, number):
        missing = self.n_materials[resource_type] - number
        if missing <= 0:
            return 0
        return self.get_time_needed_for_extra_resources(resource_type, missing)

    def get_time_needed_for_extra_resources(self, resource_type, number):
        gain_per_minute = self.n_robots[resource_type]
        if gain_per_minute == 0:
            return math.inf
        return math.ceil(number / gain_per_minute)

    def get_time_needed_per_resource(self, robot_type):
        result = {}
        for resource, missing in self.get_missing_resources_for_robot(robot_type).items():
            result[resource] = self.get_time_needed_for_extra_resources(resource, missing)
        return result

    def get_time_until_can_build(self, robot_type):
        # + 1 minute to build the robot
        return max(self.get_time_needed_per_resource(robot_type).values()) + 1

    def build(self, robot_type):
        # print(f'Building {robot_type} in minute {self.minute}')
        for resource, cost in self.robot_cost[robot_type].items():
            self.n_materials[resource] -= cost
            assert self.n_materials[resource] >= 0
        self.n_robots[robot_type] += 1

    def get_best_result_without_build(self):
        result = self.n_materials['geode']
        return result + ((self.max_n_minutes - self.minute) * self.n_robots['geode'])

    def build_can_contribute_geodes(self, robot_type, active_at_start_of_minute):
        if robot_type == 'geode':
            return True
        elif self.get_time_until_can_build('geode') == 1:
            return False
        elif robot_type == 'obsidian' and math.isinf(self.get_time_until_can_build('geode')):
            return True
        elif robot_type == 'clay' and math.isinf(self.get_time_until_can_build('obsidian')):
            return True
        if active_at_start_of_minute >= self.max_n_minutes - 2:
            # Minute 0
            # ...
            # Minute -5 18 <- Last minute in which building a clay robot could make sense
            # Minute -5 19 <- Last minute in which a clay increase (for building obsidian robot) could make sense
            # Minute -4 20 <- Last minute in which building any ore/obsidian bot could make sense
            # Minute -3 21 <- Last minute in which any resource rate increase (for building the geode bot) helps
            # Minute -2 22 <- Last minute in which building geode bot makes sense
            # Minute -1 23 <- Last minute to get geode
            return False
        if robot_type == 'clay' and active_at_start_of_minute >= self.max_n_minutes - 4:
            return False
        # time_to_get_resources_for_geode_robot = self.get_time_needed_per_resource('geode')
        # If this resource is needed for a geode robot, but we already have enough, return false
        if robot_type == 'obsidian' and self.n_materials['obsidian'] >= self.robot_cost['geode']['obsidian']:
            return False
        if robot_type == 'clay' and self.n_materials['clay'] >= self.robot_cost['obsidian']['clay']:
            return False
        return True

    def get_robots_to_try(self, last_built):
        if last_built is None:
            return ROBOTS[:2]
        index = ROBOTS.index(last_built)
        from_index = max(0, index - 1)
        return ROBOTS[from_index:index + 2]

    def run(self, debug=False, last_built=None):
        best_result = self.get_best_result_without_build()
        best_path = []
        build_costs = {}

        for robot_type in self.get_robots_to_try(last_built):
            time_taken_for_build = self.get_time_until_can_build(robot_type)
            if math.isinf(time_taken_for_build):
                continue
            robot_active_from = self.minute + time_taken_for_build
            if robot_active_from >= self.max_n_minutes or not self.build_can_contribute_geodes(robot_type,
                                                                                               robot_active_from):
                continue
            build_costs[robot_type] = time_taken_for_build
        for robot_type, costs in build_costs.items():
            result, subpath = self.clone_and_step_and_build_and_run(costs, robot_type)
            if result > best_result:
                best_result = result
                best_path = [(self.minute + costs, robot_type)] + subpath
        return best_result, best_path

    def clone_and_step_and_build_and_run(self, n_steps, robot_type):
        self_copy = copy(self)
        for _ in range(n_steps):
            self_copy.step()
        self_copy.build(robot_type)
        return self_copy.run(last_built=robot_type)

    def __copy__(self):
        result = BlueprintBruteForceNew(self.blueprint_nr, self.robot_cost, max_n_minutes=self.max_n_minutes)
        result.n_robots = deepcopy(self.n_robots)
        result.n_materials = deepcopy(self.n_materials)
        result.minute = self.minute
        return result

    @staticmethod
    def parse(line, max_n_minutes=24):
        blueprint_nr = int(line.split('Blueprint ')[-1].split(':')[0])
        ore_robot_cost = int(line.split('Each ore robot costs ')[-1].split(' ore')[0])
        clay_robot_cost = int(line.split('Each clay robot costs ')[-1].split(' ore')[0])
        obsidian_robot_cost = line.split('Each obsidian robot costs ')[-1].split(' Each geode')[0]
        obsidian_robot_cost_ore = int(obsidian_robot_cost.split(' ore')[0])
        obsidian_robot_cost_clay = int(obsidian_robot_cost.split('ore and ')[-1].split(' clay.')[0])
        geode_robot_cost = line.split('Each geode robot costs ')[-1]
        geode_robot_cost_ore = int(geode_robot_cost.split(' ore')[0])
        geode_robot_cost_obsidian = int(geode_robot_cost.split('ore and ')[-1].split(' obsidian.')[0])
        robot_costs = {
            'ore': {'ore': ore_robot_cost},
            'clay': {'ore': clay_robot_cost},
            'obsidian': {'ore': obsidian_robot_cost_ore, 'clay': obsidian_robot_cost_clay},
            'geode': {'ore': geode_robot_cost_ore, 'obsidian': geode_robot_cost_obsidian}
        }
        return BlueprintBruteForceNew(blueprint_nr, robot_costs, max_n_minutes=max_n_minutes)
