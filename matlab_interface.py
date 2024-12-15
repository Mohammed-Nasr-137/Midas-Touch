import numpy as np
# import matplotlib.pyplot as plt
import supply_chain_constructor


def construct_and_simulate(simulation_time, number_of_nodes, nodes_parameters, number_of_links, links_parameters):
    chain = supply_chain_constructor.SupplyChain()
    for i in range(number_of_nodes):
        node_name = nodes_parameters[i][0]
        node_type = nodes_parameters[i][1]
        node_inv = nodes_parameters[i][2]
        node_capacity = nodes_parameters[i][3]
        node_capIn = nodes_parameters[i][4]
        node_capOut = nodes_parameters[i][5]
        node_fixed_costs = nodes_parameters[i][6]
        node_variable_costs_coeff = nodes_parameters[i][7]
        node_processing_costs_coeff = nodes_parameters[i][8]
        node_decay_rate = nodes_parameters[i][11]
        revenueRate = nodes_parameters[i][12]
        if node_type == "source":
            node_supply_function = nodes_parameters[i][9]
            node_demand_function = [0] * simulation_time
        elif node_type == "drain":
            node_supply_function = [0] * simulation_time
            node_demand_function = nodes_parameters[i][10]
        elif node_type == "both":
            node_supply_function = nodes_parameters[i][9]
            node_demand_function = nodes_parameters[i][10]
        else:
            node_supply_function = [0] * simulation_time
            node_demand_function = [0] * simulation_time
        # node_demand = nodes_parameters[i][6]
        chain.add_node(node_name, node_type=node_type, fixed_costs=node_fixed_costs,
                       variable_costs_coeff=node_variable_costs_coeff,
                       processing_costs_coeff=node_processing_costs_coeff, inv=node_inv, capacity=node_capacity,
                       capIn=node_capIn, capOut=node_capOut, supply_function=node_supply_function,
                       demand_function=node_demand_function, decay_rate=node_decay_rate,revenueRate=revenueRate)
        # chain.add_node(node_name, node_type=node_type, inv=node_inv, capacity=node_capacity, capIn=node_capIn,
        #                capOut=node_capOut, demand=node_demand)

    for i in range(number_of_links):
        # start , end , capacity , yime , unitSize
        # print(links_parameters[i])
        link_start = links_parameters[i][0] 
        link_end = links_parameters[i][1]
        link_capacity = links_parameters[i][2]
        link_time = links_parameters[i][3]
        link_unit_size = links_parameters[i][4]
        timeDev = links_parameters[i][5]
        timeBack = links_parameters[i][6]
        cost = links_parameters[i][7]
        negReaction = links_parameters[i][8]
        negReactionVar = links_parameters[i][9]
        reactionDev = links_parameters[i][10]
        chain.add_link(link_start, link_end, capacity=link_capacity, time=link_time, unit_size=link_unit_size,timeDev=timeDev, timeBack=timeBack , cost = cost , negReaction = negReaction , negReactionVar = negReactionVar , reactionDev = reactionDev)

    return chain.simulation(simulation_time)
    # return chain


# time_steps = 300
# time = range(time_steps)
#
# # supply_function = [5 if step % 100 >= 90 or step % 100 <= 10 else 2 * (np.sin(0.1 * step) + 1) for step in time_steps]
# demand_function1 = [5 if step % 100 >= 90 or step % 100 <= 10 else 2 * (np.sin(0.1 * step) + 1) for step in time]
# demand_function2 = [3 if step % 100 >= 90 or step % 100 <= 10 else 1 * (np.sin(0.1 * step) + 1) for step in time]
#
#
# number_of_nodes = 4
# nodes_parameters = [
#     # Node Name, Type, Initial output Inventory, Capacity, Input Cap, Output Cap, fixed_costs, variable_costs,
#     # processing_rate_costs, supply_function, demand_function, decay_rate, revenue_rate
#     ("factory", "source", 0, 150, 500, 50, 2, 2, 2, [150] * time_steps, [0] * time_steps, 0.02, 0.5),
#     ("warehouse", "intermediate", 0, 200, 50, 50, 2, 2, 2, [0] * time_steps, [0] * time_steps, 0.02, 0.5),
#     ("market_1", "drain", 0, 200, 100, 100, 2, 2, 2, [0] * time_steps, demand_function1, 0.02, 0.5),
#     ("market_2", "drain", 0, 100, 75, 75, 2, 2, 2, [0] * time_steps, demand_function2, 0.02, 0.5),
# ]
#
# number_of_links = 3
# links_parameters = [
#     # From Node, To Node, Capacity, Transit Time, Unit Size, timeDev, back time, cost,
#     # negreaction, negreactionvar, rectionDev
#     ("factory", "warehouse", 500, 2, 1, 1, 1, 1, 0.02, 0.002, 0.002, 0.002),
#     ("warehouse", "market_1", 100, 3, 20, 1, 1, 1, 0.02, 0.002, 0.002),
#     ("warehouse", "market_2", 100, 3, 20, 1, 1, 1, 0.02, 0.002, 0.002),
# ]
#
#
# # Run Simulation
# data = construct_and_simulate(
#     time_steps,
#     number_of_nodes,
#     nodes_parameters,
#     number_of_links,
#     links_parameters,
# )


# for node_name, node_data in data["nodes"].items():
#     plt.figure(figsize=(10, 5))
#     plt.plot(node_data["invIn"], label=f"{node_name} Incoming Inventory")
#     plt.plot(node_data["invOut"], label=f"{node_name} Outgoing Inventory")
#     # print(node_data[node_name])
#     plt.plot(node_data["processing_rate"], label=f"{node_name} Processing Rate")
#     plt.plot(node_data["demand"], label=f"{node_name} Demand")
#     plt.legend()
#     plt.title(f"Node: {node_name}")
#     plt.show()
