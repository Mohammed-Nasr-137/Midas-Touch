# import numpy as np
# import matplotlib.pyplot as plt
import test2
# from scipy.io import savemat
# import os
# import csv
# import pprint

# time_steps = test2.time_steps
dt = test2.dt


class SupplyChain:
    def __init__(self):
        self.nodes = {}
        self.links = []
        self.history = {"time": [], "nodes": {}, "links": [],"system":{}}

    def add_node(self, name, **kwargs):
        node = test2.Node(name=name, **kwargs)
        self.nodes[name] = node
        # print(self.nodes)

    def add_link(self, from_node, to_node, **kwargs):
        # print(from_node, to_node)
        # print(self.nodes)
        # print(self.nodes.keys())
        if from_node not in self.nodes.keys() or to_node not in self.nodes.keys():
            raise ValueError(f"Nodes '{from_node}' and '{to_node}' must be added before creating a link.")
        link = test2.Link(from_node=self.nodes[from_node], to_node=self.nodes[to_node], **kwargs)
        self.links.append(link)
        # print(self.links)

    def simulation(self, simulation_time):
        cost = 0
        revenue = 0
        for node_name, node in self.nodes.items():
            self.history["nodes"][node_name] = {"invIn": [], "invOut": [], "processing_rate": [], "costs": [],
                                                "demand": [] , "revenue": []}

        for u in self.links:
            self.history["links"].append({"unitsNow": [] , "unitsBack":[] , "cost" : []})

        for step in range(simulation_time):
            self.history["time"].append(step * dt)
            for i in range(len(self.links)):
                link = self.links[i]
                link.transfer_goods(dt)
                link.update_transit_goods(dt)
                self.history["links"][i]["unitsNow"].append(sum(u[0] for u in link.goods_in_transit))
                self.history["links"][i]["unitsBack"].append(sum(u[0] for u in link.unitsBack))
                self.history["links"][i]["cost"].append(link.addedCost)

            for node_name, node in self.nodes.items():
                node.updateInput(node.supply_function[step])
                if len(node.outgoing_links) > 0:
                    node.update_routing_coeffs(step)
                node.meetDemand(step)
                node.process()
                node.negative_reaction()
                # print(node.outgoing_links)
                # if node.node_type == "intermediate":
                #     print(node.routing_coeffs)
                # print(self.history["links"])

                self.history["nodes"][node_name]["invIn"].append(node.invIn)
                self.history["nodes"][node_name]["invOut"].append(node.invOut)
                self.history["nodes"][node_name]["processing_rate"].append(node.processing_rate)
                self.history["nodes"][node_name]["demand"].append(node.demand_function[step])
                self.history["nodes"][node_name]["costs"].append(node.get_total_cost())
                self.history["nodes"][node_name]["revenue"].append(node.revenue)
            for node_name, node in self.nodes.items():
                cost += sum(self.history["nodes"][node_name]["costs"])
                revenue += sum(self.history["nodes"][node_name]["revenue"])
            for i in range(len(self.links)):
                cost += sum(self.history["links"][i]["cost"])
            self.history["system"]["revenue"] = revenue
            self.history["system"]["cost"] = cost
        return self.history

    # def save_to_matlab(self, filename):
    #     matlab_data = {"time": self.history["time"], "nodes": {}}
    #     for node_name, data in self.history["nodes"].items():
    #         matlab_data["nodes"][node_name] = data
    #     savemat(filename, matlab_data)

    # def save_as_csv(self, file_path):
    #     file_exists = os.path.isfile(file_path)
    #     with open(file_path, mode='a', newline='') as f:
    #         writer = csv.DictWriter(f, fieldnames=self.history.keys())
    #         if not file_exists:
    #             writer.writeheader()
    #         writer.writerow(self.history)

