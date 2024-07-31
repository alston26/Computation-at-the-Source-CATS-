#!/usr/bin/env python3

#from nvmexplorer_src.input_defs.cell_cfgs import *
import subprocess
import matplotlib.pyplot as plt
import re
import plotly.graph_objects as go
import numpy as np

class CactiInputInterface:
    def __init__(self, mem_cfg_path="test3.cfg",
                 page_size=8192, burst_depth=8, io_width=4,
                 system_frequency=677, stacked_die=4, 
                 partitioning_granul=0, tsv_proj=1, cache_type = '"3D memory or 2D main memory"'):
        #3D memory cronfig start
        self.mem_cfg_path = mem_cfg_path
        self.page_size = page_size
        self.burst_depth = burst_depth
        self.io_width = io_width
        self.system_frequency = system_frequency
        self.stacked_die = stacked_die
        self.partitioning_granul = partitioning_granul
        self.tsv_proj = tsv_proj
        #3D memory config end

        self.size = 2
        #8192
        self.block_size = 64
        self.associativity = 1
        #1, 2, 4, 8
        self.rw_port = 1
        #1
        self.ex_read_port = 0
        #0
        self.ex_write_port = 0
        #0
        self.search_port = 1
        #0
        self.bank_count = 1
        #1
        self.tech_node = .022
        #.050, 0.080, 0.078
        
        self.out_in_bus_width = 512
        #64
        self.tag_size = '"default"'
        #45
        self.specific_tag = 0
        self.access_mode = '"normal"'
        #normal, sequential, fast
        self.cache_type = cache_type
        #cache, ram, main memory
        self.cache_model = '"UCA"'
        #UCA, NUCA
        self.dev_obj = "0:0:0:100:0"
        self.deviate = "20:100000:100000:100000:1000000"
        #Could use the opt_targets for this?
        #weight delay, dynamic power, leakage power, cycle time, area

        self.opt_ED = '"ED^2"'
        #ED, ED^2, NONE
        self.temp = 350
        #300
        self.wire_sig = '"lowswing"'
        #fullswing, lowswing, default
        self.data_cell = '"itrs-hp"'
        #comm-dram
        self.data_peri = '"itrs-hp"'
        #itrs-lstp
        self.tag_cell = '"itrs-hp"'
        #itrs-lstp
        self.tag_peri = '"itrs-hp"'
        #itrs-lstp
        self.inter_proj = '"conservative"'
        #conservative
        self.wire_in = '"semi-global"'
        #global
        self.wire_out = '"semi-global"'
        #global
        self.int_pre_width = 1
        #1
        self.ndwl = 1
        self.ndbl = 1
        self.nspd = 0
        self.ndcm = 1
        self.ndsam1 = 0
        self.ndsam2 = 0
        self.ecc = '"NO_ECC"'
        self.dram_type = '"DDR3"'
        self.io_state = '"READ"'
        self.addr_timing = 1.0
        self.mem_density = "4 Gb"
        self.bus_freq = "800 MHz"
        self.duty_cycle = "0.5"
        self.activity_dq = "1.0"
        self.actvity_ca = "1.0"
        self.num_dq = 72
        self.num_dqs = 18
        self.num_ca = 25
        self.num_clk = 2
        self.num_mem_dq = 2
        self.mem_data_width = 8
        self.rtt_value = 10000
        self.ron_value = 34
        self.num_bobs = 1
        self.capacity = 80
        self.num_channels_per_bob = 1
        self.first_metric = '"Cost"'
        self.second_metric = '"Bandwidth"'
        self.third_metric = '"Energy"'
        self.dimm_model = '"ALL"'
        self.mirror_in_bob = '"F"'
        self.print_level = '"CONCISE"'

    def generateCactiConfig(self):
        print(self.dram_type)
        cfg_file = open(self.mem_cfg_path, "w+")
        if self.cache_type == '"3D memory or 2D main memory"':
            cfg_file.write("-size (Gb) " + str(self.size) + "\n")
        else:
            cfg_file.write("-size (bytes) " + str(self.size) + "\n")
        cfg_file.write("-block size (bytes) " + str(self.block_size) + "\n")
        cfg_file.write("-associativity " + str(self.associativity) + "\n")
        cfg_file.write("-read-write port " + str(self.rw_port) + "\n")
        
        ###3D Specific
        if self.cache_type == '"3D memory or 2D main memory"':  
            cfg_file.write("-burst depth " + str(self.burst_depth) + "\n")
            cfg_file.write("-IO width " + str(self.io_width) + "\n")
            cfg_file.write("-system frequency (MHz) " + str(self.system_frequency) + "\n")
            cfg_file.write("-stacked die count " + str(self.stacked_die) + "\n")
            cfg_file.write("-partitioning granularity " + str(self.partitioning_granul) + "\n")
            cfg_file.write("-TSV projection " + str(self.tsv_proj) + "\n")
        # #3D Specific end
        else:
            cfg_file.write("burst length " + str(self.burst_depth) + "\n")
        cfg_file.write("-exclusive read port " + str(self.ex_read_port) + "\n")
        cfg_file.write("-exclusive write port " + str(self.ex_write_port) + "\n")
        cfg_file.write("-search port " + str(self.search_port) + "\n")

        if self.cache_type == '"3D memory or 2D main memory"':
            cfg_file.write("-UCA bank count 8" + "\n")
        else:
            cfg_file.write("-UCA bank count " + str(self.bank_count) + "\n")
        
        cfg_file.write("-technology (u) " + str(self.tech_node) + "\n")
        cfg_file.write("-output/input bus width " + str(self.out_in_bus_width) + "\n")
        cfg_file.write("-tag size (b) " + str(self.tag_size) + "\n")
        cfg_file.write("-access mode " + str(self.access_mode) + "\n")
        cfg_file.write("-cache type " + str(self.cache_type) + "\n")
        cfg_file.write("-Cache model (NUCA, UCA) " + str(self.cache_model) + "\n")
        cfg_file.write("-design objective (weight delay, dynamic power, leakage power, cycle time, area) " + str(self.dev_obj) + "\n")
        cfg_file.write("-deviate (weight delay, dynamic power, leakage power, cycle time, area) " + str(self.deviate) + "\n")
        cfg_file.write("-Optimize ED or ED^2 (ED, ED^2, NONE): " + str(self.opt_ED) + "\n")
        cfg_file.write("-operating temperature (K) " + str(self.temp) + "\n")
        cfg_file.write("-Wire signalling (fullswing, lowswing, default) - " + str(self.wire_sig) + "\n")

        if self.cache_type == '"3D memory or 2D main memory"':
            if self.data_cell != '"comm-dram"':
                self.data_cell = '"comm-dram"'
                cfg_file.write("-Data array cell type - " + str(self.data_cell) + "\n")
            cfg_file.write("-Data array peripheral type - " + str(self.data_peri) + "\n")
            cfg_file.write("-Tag array cell type - " + str(self.tag_cell) + "\n")
            cfg_file.write("-Tag array peripheral type - " + str(self.tag_peri) + "\n")
        else:
            cfg_file.write("-Data array cell type - " + str(self.data_cell) + "\n")
            cfg_file.write("-Data array peripheral type - " + str(self.data_peri) + "\n")
            cfg_file.write("-Tag array cell type - " + str(self.tag_cell) + "\n")
            cfg_file.write("-Tag array peripheral type - " + str(self.tag_peri) + "\n")

        cfg_file.write("-Interconnect projection - " + str(self.inter_proj) + "\n")
        cfg_file.write("-Wire inside mat - " + str(self.wire_in) + "\n")
        cfg_file.write("-Wire outside mat - " + str(self.wire_out) + "\n")
        cfg_file.write("-page size (bits) " + str(self.page_size) + "\n")
        cfg_file.write("-internal prefetch width " + str(self.int_pre_width) + "\n")
        cfg_file.write("-Ndwl " + str(self.ndwl) + "\n")
        cfg_file.write("-Ndbl " + str(self.ndbl) + "\n")
        cfg_file.write("-Nspd " + str(self.nspd) + "\n")
        cfg_file.write("-Ndcm " + str(self.ndcm) + "\n")
        cfg_file.write("-Ndsam1 " + str(self.ndsam1) + "\n")
        cfg_file.write("-Ndsam2 " + str(self.ndsam2) + "\n")
        cfg_file.write("-specific tag = " + str(self.specific_tag) + "\n")
        cfg_file.write("-dram type " + str(self.dram_type) + "\n")
        cfg_file.write("-io state " + str(self.io_state) + "\n")
        cfg_file.write("-addr_timing " + str(self.addr_timing) + "\n")
        cfg_file.write("-mem_density " + str(self.mem_density) + "\n")
        cfg_file.write("-bus_freq " + str(self.bus_freq) + "\n")
        cfg_file.write("-duty_cycle " + str(self.duty_cycle) + "\n")
        cfg_file.write("-activity_dq " + str(self.activity_dq) + "\n")
        cfg_file.write("-activity_ca " + str(self.actvity_ca) + "\n")
        cfg_file.write("-num_dq " + str(self.num_dq) + "\n")
        cfg_file.write("-num_dqs " + str(self.num_dqs) + "\n")
        cfg_file.write("-num_ca " + str(self.num_ca) + "\n")
        cfg_file.write("-num_clk " + str(self.num_clk) + "\n")
        cfg_file.write("-num_mem_dq " + str(self.num_mem_dq) + "\n")
        cfg_file.write("-mem_data_width " + str(self.mem_data_width) + "\n")
        cfg_file.write("-rtt_value " + str(self.rtt_value) + "\n")
        cfg_file.write("-ron_value " + str(self.ron_value) + "\n")
        cfg_file.write("-tflight_value" + "\n")
        cfg_file.write("-num_bobs " + str(self.num_bobs) + "\n")
        cfg_file.write("-capacity " + str(self.capacity) + "\n")
        cfg_file.write("-num_channels_per_bob " + str(self.num_channels_per_bob) + "\n")
        cfg_file.write("-first metric " + str(self.first_metric) + "\n")
        cfg_file.write("-second metric " + str(self.second_metric) + "\n")
        cfg_file.write("-third metric " + str(self.third_metric) + "\n")
        cfg_file.write("-DIMM model " + str(self.dimm_model) + "\n")
        cfg_file.write("-mirror_in_bob " + str(self.mirror_in_bob) + "\n")
        cfg_file.write("-Print level (DETAILED, CONCISE) - " + str(self.print_level) + "\n")
        cfg_file.write("-dram ecc " + str(self.ecc) + "\n")
        cfg_file.close()
    
    def getParameters(self, num):
        #Reads the output file and returns the parameters
        if self.cache_type == '"3D memory or 2D main memory"':
            #when the cache type is 3D memory, the output file is 3D.txt
            path = "3D.txt"
            with open(path, 'r') as f:
                lines = f.readlines()
            lines = [line.rstrip() for line in lines]
            param = []
            for count in range(num, len(lines), 1):
                param.append(lines[count])
            return param
        else:  
            #when the cache type is not 3D memory, the output file is test3.cfg.out
            path = "test3.cfg.out"
            with open(path, 'r') as f:
                lines = f.readlines()
            lines = map(lambda x: x.rstrip(), lines)
            param = []
            for line in lines:
                parts = line.split()
                count = 0
                for part in parts:
                    count += 1
                    if count == num:
                        param.append(part)
            return param

    def generateInteractiveGraph(self, associativity, cache_sizes, parameters_dict, file_path):
        #associativity, technology, and cache_sizes are lists of values
        associativity_new = np.array(associativity)
        # technology_new = np.array(technology)
        cache_sizes_new = np.array(cache_sizes)

        #for 3D memory, the cache size is in GB, for 2D main memory, the cache size is in MB

        x_labels_new = [f'{cache_size}MB, Assoc {assoc}' for cache_size in cache_sizes_new for assoc in associativity_new]

        fig = go.Figure()

        #for each parameter, add a trace to the figure
        for param_name, parameters in parameters_dict.items():
            parameters_new = np.array(parameters).flatten()
            fig.add_trace(go.Scatter(x=list(range(len(x_labels_new))), y=parameters_new, mode='markers+lines', name=param_name))

        #update the layout of the figure
        fig.update_layout(
            title=f'Time for Different Cache Sizes, and Associativity {file_path} {self.cache_type}',
            xaxis_title='Cache Size, Associativity',
            yaxis_title='(ns)',
            xaxis=dict(tickvals=list(range(len(x_labels_new))), ticktext=x_labels_new),
            xaxis_tickangle=-45
        )

        #write the figure to an html file
        fig.write_html(file_path + ".html")

        fig.show()

    def generateInteractiveBarGraph(self, associativity, cache_sizes, parameters_dict, test, colors_dict):
        associativity_new = np.array(associativity)
        cache_sizes_new = np.array(cache_sizes)

        x_labels_new = [f'Associativity {assoc}, Cache Size {size}' for assoc in associativity_new for size in cache_sizes_new]

        fig = go.Figure()

        for param_name, parameters in parameters_dict.items():
            parameters_new = np.array(parameters).flatten()
            color = colors_dict.get(param_name, None) if colors_dict else None
            fig.add_trace(go.Bar(x=list(range(len(x_labels_new))), y=parameters_new, name=param_name, marker_color=color))

        fig.update_layout(
            title=f'{test} for Different Cache Configurations',
            xaxis_title='Associativity and Cache Size',
            yaxis_title='(ns)',
            xaxis=dict(tickvals=list(range(len(x_labels_new))), ticktext=x_labels_new),
            xaxis_tickangle=-45,
            barmode='group'
        )

        fig.write_html(test + ".html")
        fig.show()
        fig.show()


    def generateBarGraph(self, associativity, cache_sizes, parameters_dict, test, colors_dict):
        associativity_new = np.array(associativity)
        cache_sizes_new = np.array(cache_sizes)

        x_labels_new = [f'Associativity {assoc}, Cache Size {size}' for assoc in associativity_new for size in cache_sizes_new]

        fig, ax = plt.subplots(figsize=(14,10), facecolor="#bcbddb")

        bar_width = 0.2
        index = np.arange(len(x_labels_new))

        for i, (param_name, parameters) in enumerate(parameters_dict.items()):
            parameters_new = np.array(parameters).flatten()
            color = colors_dict.get(param_name, None) if colors_dict else None
            ax.bar(index + i * bar_width, parameters_new, bar_width, label=param_name, color=color)

        ax.set_title(f'Access Time for Different Cache Configurations')
        ax.set_xlabel('Associativity and Cache Size')
        ax.set_ylabel('(nanoseconds)')
        ax.set_xticks(index + bar_width * (len(parameters_dict) - 1) / 2)
        ax.set_xticklabels(x_labels_new, rotation=-45, ha='left')
        ax.set_facecolor("#e8eaeb")
        ax.legend()

        plt.tight_layout()
        plt.savefig(test + ".png")
        plt.show()
        
    def generateGraph(self, associativity, cache_sizes, io_width, parameters_dict, file_path):
        #associativity, technology, and cache_sizes are lists of values
        associativity_new = np.array(associativity)
        cache_sizes_new = np.array(cache_sizes)
        Io_new = np.array(io_width)


        plt.figure(figsize=(14, 8))

        #for 3D memory, the cache size is in GB, for 2D main memory, the cache size is in MB
        if self.cache_type == '"3D memory or 2D main memory"':
            x_labels_new = [f'{cache_size}GB, Assoc {assoc}, Io Width {Io}' for cache_size in cache_sizes_new for assoc in associativity_new for Io in Io_new]
        else:
            x_labels_new = [f'{cache_size*1024*1024}B, Assoc {assoc}, Io Width {Io}' for cache_size in cache_sizes_new for assoc in associativity_new for Io in Io_new]
        x_ticks_new = range(len(x_labels_new))

        #for each parameter, plot a line graph
        for key, values in parameters_dict.items():
            if len(x_ticks_new) != len(values):
                raise ValueError(f"Length mismatch: x ({len(x_ticks_new)}) and y ({len(values)}) must have the same length for key {key}")
            plt.plot(x_ticks_new, values, marker='o', linestyle='-', label=key)

        #update the layout of the graph
        plt.xticks(x_ticks_new, x_labels_new, rotation=90)
        plt.xlabel('Cache Size, Associativity, Io Width')
        plt.ylabel('nJ')
        plt.title(f'Energy for Different Cache Sizes, Io Widths, and Associativity {file_path} {self.cache_type}')
        plt.grid(True)
        plt.legend()

        #save the graph to a file based on the type of memory
        plt.tight_layout()
        plt.savefig(file_path + ".png")
        print("figure generated")
        plt.show()

        

if __name__ == '__main__':
    #lists of values for cache sizes, associativity, technology, wire signal, dram type, access mode, and io width
    cache_sizes = [1, 2, 4, 8]
    associativity = [2, 4, 8, 16]
    technology = [0.032, 0.040, 0.050, 0.065, 0.09]
    wire_signal = ['"fullswing"', '"lowswing"', '"default"']
    dram_type = ['"DDR3"', '"DDR4"']
    access_mode = ['"normal"', '"sequential"', '"fast"']
    io_width = [1, 2, 4, 8]
    cache_type = ['"cache"', '"ram"', '"main memory"', '"3D memory or 2D main memory"']

    #main loop to generate the cacti config files and run the cacti simulation
    parameters_dict = {
                '"cache"': [],
                '"ram"': [],
                '"main memory"': [],
                '"3D memory or 2D main memory"': [],
                }
    colors_dict={'"cache"': "#bcbddb", 
                 '"ram"': "#6b76b1", 
                 '"main mmeory"': "#fcf9dd", 
                 '"3D memory or 2D main memory"': "#f9e94d",}
            
    for cache in cache_type:
        open('test3.cfg.out', 'w').close()
        open('3D.txt', 'w').close() 
        for size in cache_sizes:
            for assoc in associativity:
                cacti_interface = CactiInputInterface()
                if cacti_interface.dram_type == '"DDR3"':
                    cacti_interface.bus_freq = "800 MHz"
                    cacti_interface.duty_cycle = "0.5"
                elif cacti_interface.dram_type == '"DDR4"':
                    cacti_interface.bus_freq = "1600 MHz"
                    cacti_interface.duty_cycle = "0.5"
                # cacti_interface.access_mode = access
                # cacti_interface.tech_node = tech
                # cacti_interface.io_width = io
                cacti_interface.cache_type = cache
                cacti_interface.associativity = assoc
                if cacti_interface.cache_type == '"3D memory or 2D main memory"':
                    cacti_interface.size = size
                else:
                    cacti_interface.size = size * 1024 * 1024
                cacti_interface.generateCactiConfig()
                config_file_path = cacti_interface.mem_cfg_path
                print("Cacti config file generated")
                cacti_command = f"./cacti -infile {config_file_path}"

                try:
                    subprocess.run(cacti_command, check=True, shell=True)
                    print("CACTI simulation completed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Error running CACTI: {e}")
        #6 is access time, 7 is random cycle time, 8 is Dynamic search energy (nJ), 9 is Dynamic read energy (nJ), 10 is Dynamic write energy (nJ)
        #19 is data
        if cache == '"3D memory or 2D main memory"':

            parameter_indices = {
                't_CAS': 0,
                }

            for param_name, index in parameter_indices.items():
                #cacti_interface.getParameters(index) returns a list of strings
                accessTime = cacti_interface.getParameters(index)
                accesses = [re.findall(r"[-+]?\d*\.\d+|\d+", i) for i in accessTime]
                actAccess = []
                # print(parameters_dict)
                for l in range(0, len(accesses), 4):
                    if l + 3 < len(accesses): 
                        addedAccess = sum((accesses[l + j] for j in range(4)), [])
                        actAccess.append([round(float(t) * 1e-5, 4) for t in addedAccess])
                parameters_dict[cache] = [item for sublist in actAccess for item in sublist]
        else:

            parameter_indices = {
                'access_time': 6,
                }

            for param_name, index in parameter_indices.items():
                accessTime = cacti_interface.getParameters(index)
                accesses = [re.findall(r"[-+]?\d*\.\d+|\d+", i) for i in accessTime]
                actAccess = []
                # print(access)
                for l in range(0, len(accesses), 4):
                    if l + 3 < len(accesses):  
                        addedAccess = sum((accesses[l + j] for j in range(4)), [])
                        actAccess.append([float(t) for t in addedAccess])
                parameters_dict[cache] = [item for sublist in actAccess for item in sublist]
    print(parameters_dict)
    #generate the graph
    # cacti_interface.generateInteractiveGraph(associativity, cache_sizes, parameters_dict, "cacti")
    cacti_interface.generateBarGraph(associativity, cache_sizes, parameters_dict, "cacti",colors_dict)
    # cacti_interface.generateInteractiveBarGraph(associativity, cache_sizes, parameters_dict, "cacti",colors_dict)
        
