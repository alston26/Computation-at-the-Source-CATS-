import subprocess
import matplotlib.pyplot as plt
import numpy as np
import re
import itertools as iter
import plotly.graph_objects as go

class ramulatorInterface():
    
    def __init__(self):
        self.standard = "DDR4"
        self.channel = 1
        self.ranks = 1
        self.speed = "DDR4_2400R"
        self.org = "DDR4_4Gb_x8"
        self.record_cmd_trace = "off"
        self.print_cmd_trace = "off"
        self.cpu_tick = 8
        self.mem_tick =3
        self.early_exit = "on"
        self.expected_limit_insts = "200000000"
        self.warmup_insts = 0
        self.cache = "no"
        self.translation = "None"

    def generateConfig(self):
        filename = f"{self.standard}_{self.speed}_{self.org}.cfg"
        mkdir_command = f"mkdir -p custom_configs"
        subprocess.run(mkdir_command, check=True, shell=True)
        cd_command = f"cd custom_configs"
        subprocess.run(cd_command, check=True, shell=True)
        touch_command = f"touch {filename}"
        subprocess.run(touch_command, check=True, shell=True)
        cfg_file = open(f"custom_configs/{filename}", "w+")
        cfg_file.write("standard = " + self.standard + "\n")
        
        if self.standard == "WideIO" or self.standard == "WideIO2":
            cfg_file.write("channels = " + "4" + "\n")
        elif self.standard == "HBM":
            cfg_file.write("channels = " + "8" + "\n")
        else:
            cfg_file.write("channels = " + str(self.channel) + "\n")
            
            
        if self.standard == "DSARP":
            cfg_file.write("subarray = " + "4"+ "\n")
        elif self.standard == "TLDRAM":
            cfg_file.write("subarrays = " + "16" + "\n")
        elif self.standard == "SALP-MASA":
            cfg_file.write("subarrays = " + "8" + "\n")
            
        cfg_file.write("ranks = " + str(self.ranks) + "\n")
        cfg_file.write("speed = " + self.speed + "\n")
        cfg_file.write("org = " + self.org + "\n")
        cfg_file.write("record_cmd_trace = " + self.record_cmd_trace + "\n")
        cfg_file.write("print_cmd_trace = " + self.print_cmd_trace + "\n")
        cfg_file.write("cpu_tick = " + str(self.cpu_tick) + "\n")
        cfg_file.write("mem_tick = " + str(self.mem_tick) + "\n")
        cfg_file.write("early_exit = " + self.early_exit + "\n")
        cfg_file.write("expected_limit_insts = " + self.expected_limit_insts + "\n")
        cfg_file.write("warmup_insts = " + str(self.warmup_insts) + "\n")
        cfg_file.write("cache = " + self.cache + "\n")
        cfg_file.write("translation = " + self.translation + "\n")
        cfg_file.close()
    
    def generateOutputsTable(self, input):
        #open the output file and read the values
        path = "my_output.txt"
        with open(path, 'r') as f:
            lines = f.readlines()
        
        lines = map(lambda x: x.rstrip(), lines)
        param = {}
        
        #parse the values
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0]
                value = parts[1]
                if key != '[0]' and key == input:
                    param[key] = value
        
        return param
    
    def generateOutputsGraph(self, filepath, input):
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        lines = map(lambda x: x.rstrip(), lines)
        
        #parse the values
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0]
                value = parts[1]
                if key == input:
                    return value

    def generateTable(self, values):
        param = values
        
        fig, ax = plt.subplots()
        ax.axis('tight')
        ax.axis('off')
        
        table_data = [["Key", "Value"]]
        for key, value in param.items():
            table_data.append([key, value])
        
        table = ax.table(cellText=table_data, colLabels=None, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(6)
        table.scale(1, 1)
        
        plt.show()
    
    def generateGraph(self, dramType, dram_speed, dram_org, values, testing_value):
        print("generating graph")
        dramType_new = np.array(dramType)
        dram_speed_new = np.array(dram_speed)
        dram_org_new = np.array(dram_org)
        values = np.array(values)

        plt.figure(figsize=(36, 14))

        x_labels_new = [f'Type {Type}, Speed {speed}, Org {org}' for Type in dramType_new for speed in dram_speed_new for org in dram_org_new]
        x_ticks_new = range(len(x_labels_new))

        values_new = values.flatten()

        plt.plot(x_ticks_new, values_new, marker='o', linestyle='-')

        plt.xticks(x_ticks_new, x_labels_new, rotation=90)
        plt.xlabel('dramType, dramSpeed, dramOrg')
        plt.ylabel(f'{testing_value}')
        plt.title(f'{testing_value} for Different Dram Types, Speed, and Organization')
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(f"custom_graphs/{testing_value}_{dramType[0]}.png")
        plt.show()
        
        
    def generateBarGraph(self, speed, org, parameters_dict, test, colors_dict):
        speed_new = np.array(speed)
        org_new = np.array(org)
        x_labels_new = [f'{speeds}, {organ}' for speeds in speed_new for organ in org_new]

        fig, ax = plt.subplots(figsize=(10, 6), facecolor="#6b76b1")
        
        bar_width = 0.3
        index = np.arange(len(x_labels_new))

        for i, (param_name, parameters) in enumerate(parameters_dict.items()):
            parameters_new = np.array(parameters).flatten()
            color = colors_dict.get(param_name, None) if colors_dict else None
            ax.bar(index + i * bar_width, parameters_new, bar_width, label=param_name, color=color)

        ax.set_title(f'Max Bandwidth for Different Memory Speeds and Organizations')
        ax.set_xlabel('Memory Speeds and Organizations')
        ax.set_ylabel('(Bits per Second)')
        ax.set_xticks(index + bar_width * (len(parameters_dict) - 1) / 2)
        ax.set_xticklabels(x_labels_new, rotation=-45, ha='left')
        ax.set_facecolor("#e8eaeb")
        ax.legend()

        plt.tight_layout()
        plt.savefig("Ramulator Bandwidth" + ".png")
        plt.show()
        
    
        
if __name__ == "__main__":
    dramType = ["DDR3", "DDR4", "HBM"] #"DDR3", "DDR4", "GDDR5", "HBM", "DSARP", "LPDDR3","LPDDR4", "PCM", "SALP-MASA", "STTMRAM", "TLDRAM", "WideIO", "WideIO2"
    dram_speed = [ "DDR3_1600K", "DDR4_2400R", "HBM_1Gbps"] #, "DDR4_2400R", "GDDR5_6000", "HBM_1Gbps", "DSARP_1333", "LPDDR3_1600", "LPDDR4_2400", "PCM_800D", "SALP_1600K", "STT_1600_1_2", "TLDRAM_1600K", "WideIO_266", "WideIO2_1066"
    dram_org = ["DDR3_2Gb_x8", "DDR4_4Gb_x8", "HBM_4Gb"] #"DDR4_4Gb_x8", "GDDR5_8Gb_x32", "HBM_4Gb", "DSARP_8Gb_x8", "LPDDR3_8Gb_x32", "LPDDR4_8Gb_x16", "PCM_2Gb_x8", "SALP_4Gb_x8", "STT_2Gb_x8", "TLDRAM_4Gb_x32", "WideIO_8Gb", "WideIO2_8Gb"
    
    #ramulator.maximum_bandwidth, ramulator.dram_capacity, ramulator.dram_cycles, ramulator.in_queue_req_num_avg, ramulator.read_latency_avg_0, ramulator.active_cycles_0
    test = "ramulator.maximum_bandwidth"
    
    #"HBM", "LPDDR3","LPDDR4", "PCM", "SALP-MASA", "STTMRAM", "WideIO"
    #"HBM_1Gbps", "DSARP_1333", "LPDDR3_1600", "LPDDR4_2400", "PCM_800D", "SALP_1600K", "STT_1600_1_2", "WideIO_266", "WideIO2_1066"
    #, "HBM_4Gb", "DSARP_8Gb_x8", "LPDDR3_8Gb_x32", "LPDDR4_8Gb_x16", "PCM_2Gb_x8", "SALP_4Gb_x8", "STT_2Gb_x8", "WideIO_8Gb", "WideIO2_8Gb"
    issues = []
    mode = "dram"
    parameters_dict = {
                'DDR3': [],
                'DDR4': [],
                'HBM': [],
                }
    colors_dict={'DDR3': "#bcbddb", 
                 'DDR4': "#6b76b1",  
                 'HBM': "#f9e94d",}
    
    for standard in dramType:
        values = []
        for combo in iter.product(dram_speed, dram_org):
                ramulator = ramulatorInterface()
                ramulator.standard = standard
                ramulator.speed = combo[0]
                ramulator.org = combo[1]
                # ramulator.generateConfig()
                ramConfig = standard + "_" + combo[0] + "_" + combo[1]
                modeOutput = ramConfig + "_" + f"{mode}"
                # print(ramConfig)
                ramulator_command = f"./ramulator custom_configs/{ramConfig}.cfg --mode={mode} --stats custom_results/{modeOutput}.txt {mode}.trace"
                try:
                    subprocess.run(ramulator_command, check=True, shell=True)
                    print("Ramulator simulation completed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Error running Ramulator: {e}")
                values.append(ramulator.generateOutputsGraph(f'custom_results/{modeOutput}.txt', test))

        values = [re.findall(r"[-+]?\d*\.\d+|\d+", i) for i in values]
        values_new = []
        for i in range(0, len(values), 3):
            addedValues = sum((values[i+j] for j in range(3)), [])
            values_new.append([float(t) for t in addedValues])
        parameters_dict[standard] = [item for sublist in values_new for item in sublist]
    print(parameters_dict)
    ramulator.generateBarGraph(dram_speed, dram_org, parameters_dict, test, colors_dict)
