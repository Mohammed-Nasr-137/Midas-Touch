import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# time_steps = 300
dt  = 0.1


class Node:
    def __init__(self, name, node_type, fixed_costs, variable_costs_coeff, processing_costs_coeff, supply_function,
                 demand_function, capacity=float('inf'), capIn=float('inf'), capOut=float('inf'),
                 inv=0, decay_rate=0.02,revenueRate = 0):
        self.name = name
        self.capacity = capacity  # Max node processing rate capacity
        self.capIn = capIn  # Max node input capacity
        self.capOut = capOut  # Max node output capacity
        self.routing_coeffs = []
        # self.link_routing_coeffs_pairs = []  # pair routing coeffs with links
        self.incoming_links = []  # links manage this (can make it as list of links objects)
        self.outgoing_links = []  # links manage this (can make it as list of links objects)
        self.processing_rate = 0  # Current processing rate
        self.fixed_costs = fixed_costs  # fixed costs like rent or salaries
        self.variable_costs_coeff = variable_costs_coeff  # variable costs that depends on inventory levels
        self.processing_costs_coeff = processing_costs_coeff  # cost of processing
        # input costs per one timestep
        self.revenue = 0
        self.revenueRate = revenueRate
        self.invIn = 0  # initial input inventory (changed from 500 to 0 for consistency)
        self.invOut = inv  # initial output inventory
        self.supply_function = supply_function
        self.demand_function = demand_function
        self.node_type = node_type  # will be source, drain or intermediate
        self.decay_rate = decay_rate  # for every 100 steps
        self.isprocessing = False  # flag to know if the node is currently processing


    def add_incoming_links(self, link):
        self.incoming_links.append(link)

    def add_outgoing_links(self, link):
        self.outgoing_links.append(link)

    def updateInput(self, supply): # i: counter for steps
        self.invIn += supply * dt if self.invIn + supply * dt <= self.capIn else 0
        self.processing_rate = min(self.capacity, self.invIn / dt) if self.invOut <= self.capOut else 0

    def process(self):
        if self.invIn >= self.processing_rate * dt and self.invOut + self.processing_rate * dt <= self.capOut:
            self.isprocessing = True
            self.invOut += self.processing_rate * dt
            self.invIn -= self.processing_rate * dt
        else:
            self.isprocessing = False

    def meetDemand(self, i): # i: counter for steps
        sales = self.demand_function[i] * dt if self.invOut >= self.demand_function[i] * dt else self.invOut
        self.invOut -= sales
        self.revenue = sales*self.revenueRate

    def passiveGain(self, gain):
        self.invIn += gain * dt if self.invIn + gain * dt <= self.capIn else 0

    def updateOutput(self, output):
        self.invOut -= output

    def get_total_cost(self):
        total_cost = (self.fixed_costs + self.variable_costs_coeff * (self.invIn + self.invOut))*dt
        if self.isprocessing:
            total_cost += self.processing_costs_coeff * self.processing_rate * dt
        return total_cost

    def negative_reaction(self): # i: counter for steps
        self.invIn -= self.invIn * self.decay_rate*dt
        self.invOut -= self.invOut * self.decay_rate*dt

    def calc_rc(self, link, time_step):
        weights_matrix = [1, 1, 1, 1, 1, 1, 1, 1]
        # weights_matrix = [0, 0, 0, 0, 0, 0, 0, 1]
        epsilon = 1e-9
        downstream_node = link.to_node
        available_capacity = link.capacity - sum(u[0] for u in link.goods_in_transit)
        if available_capacity < 0:
            available_capacity = 0
        transit_time = link.time
        transportation_cost = link.cost
        link_decay_rate = link.negReaction
        inv_downstream = downstream_node.invOut
        downstream_demand = downstream_node.demand_function[time_step] * dt
        unsatisfied_demand = downstream_demand - downstream_node.invOut
        if unsatisfied_demand < 0:
            unsatisfied_demand = 0
        processing_downstream = downstream_node.processing_**rate
        processing_cap_downstream = downstream_node.capacity
        downstream_revenue_rate = downstream_node.revenueRate
        w = (weights_matrix[0] * (available_capacity / (link.capacity + epsilon)) + weights_matrix[1] * transit_time +
             weights_matrix[2] * (1 / (transportation_cost + epsilon)) + weights_matrix[3] * (1 / (link_decay_rate + epsilon)) +
             weights_matrix[4] * (1 / (inv_downstream + epsilon)) +
             weights_matrix[5] * (unsatisfied_demand / (downstream_demand + epsilon)) +
             weights_matrix[6] * (processing_downstream / (processing_cap_downstream + epsilon)) +
             weights_matrix[7] * downstream_revenue_rate)

        return w


    def update_routing_coeffs(self, i):
        total_weight = 0
        weights = []
        for link in self.outgoing_links:
            # Weight based on available capacity and transit time
            # weight = max(0, available_capacity / (link.time + link.timeDev))
            weight = self.calc_rc(link, i)
            weights.append(weight)
            total_weight += weight

        if total_weight > 0:
            self.routing_coeffs = [weight / total_weight for weight in weights]
        else:
            # print(len(self.outgoing_links))
            # Equal distribution if no capacity
            self.routing_coeffs = [1 / min(len(self.outgoing_links),1)] * len(self.outgoing_links)

        self.assign_rc_to_links()
        # total_outgoing_flux = self.invOut  # Total flux leaving the node (might need config)
        # for i, link in enumerate(self.outgoing_links):
        #     link.current_flux = self.routing_coeffs[i] * total_outgoing_flux

    def assign_rc_to_links(self):
        for i in range(len(self.outgoing_links)):
            self.outgoing_links[i].routing_coeff = self.routing_coeffs[i]
            self.outgoing_links[i].routing_history.append(self.routing_coeffs[i])


class Link:
    def __init__(self, from_node, to_node, capacity, time , timeBack , cost=0, unit_size=1, timeDev = 0.01 , negReaction = 0 , negReactionVar = 0 , reactionDev = 0):

        self.from_node = from_node
        self.to_node = to_node
        self.capacity = capacity  # can be number of units or total capacity (num)
        self.time = time  # time unit takes to travel from one node to another
        self.timeBack = timeBack  # time unit takes to travel back
        self.cost = cost  # need configuration
        self.timeDev = timeDev  # Standard Deviation of time
        self.unit_size = unit_size  # unit size for quantization
        self.addedCost = 0
        self.negReaction = negReaction
        self.negReactionVar = negReactionVar
        self.reactionDev = reactionDev
        self.goods_in_transit = []  # list of goods in transit {number of units, time remaining}
        self.unitsBack = []  # list of goods in transit {number of units, time remaining}
        self.routing_coeff = 0
        self.routing_history = []
        from_node.add_outgoing_links(self)
        to_node.add_incoming_links(self)

    def transfer_goods(self, dt):
        transitNum = sum(u[0] for u in self.goods_in_transit) + sum(u[0] for u in self.unitsBack)  # Corrected to sum the number of units in transit
        self.addedCost = 0
        if self.capacity - transitNum > 0 and self.from_node.invOut * self.routing_coeff >= self.unit_size:
            quantity = min(int(self.from_node.invOut * self.routing_coeff / self.unit_size), self.capacity - transitNum)
            if quantity > 0:
                self.from_node.updateOutput(quantity * self.unit_size)
                time = self.timeCalc(quantity, self.time)
                self.goods_in_transit.append([quantity, time])
                self.addedCost = self.cost * quantity
            

    def timeCalc(self,n,time):
        times = []
        for i in range(int(n)):
            times.append(np.random.normal(time, self.timeDev/100*time))
            # print(times)
        return np.average(times)
    
    def reactionCalc(self,t):
        total = self.negReaction + (self.time + abs(t))/dt*self.negReactionVar
        return min(np.random.normal(total, self.reactionDev),100)

    def update_transit_goods(self, dt):
        for u in self.goods_in_transit[:]:
            u[1] -= dt
            if u[1] <= 0:
                remaining_capacity = self.to_node.capIn - self.to_node.invIn
                if remaining_capacity == float('inf'):
                    remaining_capacity = 1e9  # Set to a very large number if infinite
                if remaining_capacity >= self.unit_size:
                    units_to_transfer = min(int(remaining_capacity / self.unit_size), u[0])
                    reaction = self.reactionCalc(u[1])
                    self.to_node.updateInput(units_to_transfer * self.unit_size *(1-abs(reaction/100)))
                    u[0] -= units_to_transfer  # Reduce the number of units in transit
                    if units_to_transfer >0:
                        time = self.timeCalc(units_to_transfer,self.timeBack)
                        self.unitsBack.append([units_to_transfer,time])
                    if u[0] == 0:
                        self.goods_in_transit.remove(u)
        for u in self.unitsBack[:]:
            u[1] -= dt
            if u[1] <= 0:
                self.unitsBack.remove(u)
