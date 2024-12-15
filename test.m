%insert(py.sys.path, int32(0), '"E:\uni\sec\term1\proj\phase3\V1\supply_chain_constructor.py"');
test_module = py.importlib.import_module('matlab_interface');

number_of_nodes = int32(2);
number_of_links = int32(1);
demand_function_inc = (1:1:100)*0.1;
demand_function_dec = (100:-1:21)*0.1;
demand_function_dec2 = ones(1,120)*2.1;
demand_func = [ones(1,300)*50];
%        name, type, inv, capacity , capin,capout , fixed cost , var cost , process cost , supply func , demand func , neg. reaction /100 , rev
node_1 ={"factory", "source", 200, 200, 200, 200 , 10 , 0 , 0 , ones(1,300)*100, zeros(1,300), 0.001 , 0};
node_2 ={"supermarket1", "drain", 190, 50, 200, 200, 10 , 0 , 0 , zeros(1,300), demand_func, 0.001 , 10};
% node_3 ={"supermarket2", "drain", 190, 50, 200, 200, 10 , 0 , 0 , zeros(1,300), 0.3*demand_func, 0.001 , 10};
node_parameter ={node_1,node_2};
%        start , end , capacity , time , unit Size , timeDev (percentage) , timeBack , unit cost , negative Reaction (percentage), negative Reaction variable (percentage), reactionDev (percentage)
link_1 = {"factory", "supermarket1", 10, 5, 25 , 1 , 4 , 3 , 2 , 0.1 , 2};
% link_2 = {"factory", "supermarket2", 10, 2, 30 , 10 , 2 , 4 , 2 , 0.1 , 2};
link_parameter ={link_1};

supply_func = ones(1,300)*100;
time = int32(300);


data = test_module.construct_and_simulate(time,number_of_nodes,node_parameter,number_of_links,link_parameter);
% figure;
% subplot(3, 2, 1);
% plot(data{'time'},data{'nodes'}{'factory'}{'invOut'})
% title('factory inventory');
% subplot(3, 2, 2);
% plot(data{'time'},data{'nodes'}{'supermarket1'}{'invOut'})
% title('s1 inventory');
% subplot(3, 2, 3);
% plot(data{'time'},data{'nodes'}{'supermarket2'}{'invOut'})
% title('s2 inventory');
% subplot(3, 2, 4);
% plot(data{'time'},data{'links'}{1}{'unitsNow'})
% title('l1 now');
% subplot(3, 2, 5);
% plot(data{'time'},data{'links'}{1}{'unitsBack'})
% title('l1 back');
% subplot(3, 2, 6);
% plot(data{'time'},data{'links'}{1}{'cost'})
% title('l1 cost');

cost = data{'system'}{'cost'}
revenue = data{'system'}{'revenue'}
profit = data{'system'}{'revenue'}-data{'system'}{'cost'}

% data


