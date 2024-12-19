clc;
clear;

% Import the Python module
test_module = py.importlib.import_module('matlab_interface');

% Simulation configuration
simulation_time=300;
% Simulation configuration
number_of_nodes = int32(5);
number_of_links = int32(4);
dev_coff=0;
x=1:1:simulation_time;
demand_func =abs(sin(0.05.*x))+30;  
supply_func = 150*(ones(1, 300)) ;
%demand_func = ones(1, 300) * 50; % For simpler simulation
% Define the parameters for the nodes and links
%         name, type, inv,capacity ,capin,capout,fixed cost , var cost , process cost , supply func , demand func , neg. reaction /100 , rev 

node_1 ={"factory", "source", 200, 200, 200, 200 , 10 , 0 , 0 , ones(1,300)*100, zeros(1,300), 0.001 , 0};
node_2 ={"supermarket1", "drain", 190, 150, 200, 200, 10 , 0 , 0 , zeros(1,300), demand_func, 0.001 , 10};
node_3 ={"warehouse1", "intermediate", 190, 150, 200, 200, 10 , 0 , 0 , zeros(1,300), 0.3*demand_func, 0.001 , 10};
node_4 = {"supermarket2", "drain", 190, 150, 200, 200, 10 , 0 , 0 , zeros(1,300), demand_func, 0.001 , 10};
node_5 ={"warehouse2", "intermediate", 190, 150, 200, 200, 10 , 0 , 0 , zeros(1,300), 0.3*demand_func, 0.001 , 10};
node_parameter = {node_1, node_2, node_3, node_4, node_5};
%        start , end , capacity , time , unit Size , timeDev (percentage) , timeBack , unit cost , negative Reaction (percentage), negative Reaction variable (percentage), reactionDev (percentage)
link_1 = {"factory", "warehouse1", 10, 5, 100 , dev_coff , 4 , 3 , 2 , 0.1 , dev_coff};
link_2 = {"warehouse1", "supermarket1", 10, 2, 50 , dev_coff , 2 , 4 , 2 , 0.1 , dev_coff};
link_3 = {"warehouse2", "supermarket2", 10, 2, 50 , dev_coff , 2 , 4 , 2 , 0.1 , dev_coff};
link_4 = {"factory", "warehouse2", 10, 5, 100 , dev_coff , 4 , 3 , 2 , 0.1 , dev_coff};

link_parameter= {link_1, link_2, link_3, link_4};


% List of parameters to sweep for nodes and links
parameters_to_sweep_nodes = {'cap', 'capin', 'capout'};
parameters_to_sweep_links = {'cap', 'unitsize'};

% Initialize results storage
results = {}; % Store results for nodes and links

% Node Sweeping Logic
figure_handles_nodes = gobjects(1, number_of_nodes);

for node_idx = 1:number_of_nodes
    %figure_handles_nodes(node_idx) = figure;
    %node_name = node_parameter{node_idx}{1};
    %sgtitle(['Node: ', char(node_name)]);
end

best_values_nodes = zeros(1, length(parameters_to_sweep_nodes));
best_values_links = zeros(1, length(parameters_to_sweep_links));

% Initialize variable to store the maximum profit
max_profit_so_far = -Inf;
best_combination = [];

% Sweep Node Parameters
for param_idx = 1:length(parameters_to_sweep_nodes)
    param = parameters_to_sweep_nodes{param_idx};

    for node_idx = 1:number_of_nodes
        node_name = node_parameter{node_idx}{1};
        varing_profit = [];
        varing_cost = [];
        varing_revenue = [];

        sweep_values = 50:50:500;

        for i = 1:length(sweep_values)
            original_value = node_parameter{node_idx}{4 + param_idx};
            node_parameter{node_idx}{4 + param_idx} = sweep_values(i);

            % Lock other parameters to their best value so far
            for p = 1:param_idx
                node_parameter{node_idx}{4 + p} = best_values_nodes(p);
            end

            try
                data = test_module.construct_and_simulate(int32(simulation_time),number_of_nodes, node_parameter, number_of_links, link_parameter);
            catch ME
                disp('Error in construct_and_simulate:');
                disp(ME.message);
                return;
            end

           % node_parameter{node_idx}{4 + param_idx} = original_value;

            cost = data{'system'}{'cost'};
            revenue = data{'system'}{'revenue'};
            profit = revenue - cost;

            varing_profit(i) = profit;
            varing_cost(i) = cost;
            varing_revenue(i) = revenue;
        end

        [~, max_profit_idx] = max(varing_profit);
        best_values_nodes(param_idx) = sweep_values(max_profit_idx);

        results = [results; {
            char(node_name), param, '', '', sweep_values(max_profit_idx), max(varing_profit),
        }];

        if max(varing_profit) > max_profit_so_far
            max_profit_so_far = max(varing_profit);
            best_combination = {
                'Node Parameters', node_parameter, 'Link Parameters', link_parameter
            };
        end

    end
end

% Sweep Link Parameters
figure_handles_links = gobjects(1, number_of_links);


for param_idx = 1:length(parameters_to_sweep_links)
    param = parameters_to_sweep_links{param_idx};

    for link_idx = 1:number_of_links
        link_name = link_parameter{link_idx}{1};
        varing_profit = [];

        sweep_values = 50:50:500;

        for i = 1:length(sweep_values)
            original_value = link_parameter{link_idx}{3 + param_idx};
            link_parameter{link_idx}{3 + param_idx} = sweep_values(i);

            for p = 1:param_idx-1
                link_parameter{link_idx}{3 + p} = best_values_links(p);
            end

            try
                data = test_module.construct_and_simulate(int32(simulation_time),number_of_nodes, node_parameter, number_of_links, link_parameter);
            catch ME
                disp('Error in construct_and_simulate:');
                disp(ME.message);
                return;
            end

            link_parameter{link_idx}{3 + param_idx} = original_value;

            cost = data{'system'}{'cost'};
            revenue = data{'system'}{'revenue'};
            profit = revenue - cost;

            varing_profit(i) = profit;
        end

        [~, max_profit_idx] = max(varing_profit);
        best_values_links(param_idx) = sweep_values(max_profit_idx);

        results = [results; {
            char(link_name), '', param, sweep_values(max_profit_idx), '', max(varing_profit),
        }];

        if max(varing_profit) > max_profit_so_far
            max_profit_so_far = max(varing_profit);
            best_combination = {
                'Node Parameters', node_parameter, 'Link Parameters', link_parameter
            };
        end

    end
end


% Show the best combination of parameters
disp('Best Combination of Parameters for Maximum Profit:');
disp(best_combination);

% Create a detailed popup showing all parameters and max profit
detailed_popup = figure('Name', 'Detailed System Parameters', 'NumberTitle', 'off', 'Position', [200, 200, 900, 500]);

data = {['Maximum Profit: ', num2str(max_profit_so_far)]};
data = [data; {'Node Parameters:'}];
for i = 1:number_of_nodes
    node_params = node_parameter{i};
    node_info = sprintf('Node %d: Name=%s, Type=%s, Inv=%d, Capacity=%d, CapIn=%d, CapOut=%d, FixedCost=%d, VarCost=%d, ProcessCost=%d', ...
        i, node_params{1}, node_params{2}, node_params{3}, node_params{4}, node_params{5}, node_params{6}, node_params{7}, node_params{8}, node_params{9});
    data = [data; {node_info}];
end

data = [data; {'Link Parameters:'}];
for i = 1:number_of_links
    link_params = link_parameter{i};
    link_info = sprintf('Link %d: Start=%s, End=%s, Capacity=%d, Time=%d, UnitSize=%d, TimeDev=%f, TimeBack=%d, UnitCost=%d, NegReaction=%f, ReactionDev=%f', ...
        i, link_params{1}, link_params{2}, link_params{3}, link_params{4}, link_params{5}, link_params{6}, link_params{7}, link_params{8}, link_params{9}, link_params{10});
    data = [data; {link_info}];
end

uitable('Parent', detailed_popup, 'Data', data, 'RowName', [], 'ColumnName', {'Details'}, 'Position', [20, 20, 860, 460]);
