import numpy as np

class Sim_Data_Container :
    def __init__(self):
        self.sim_type = {'transient':False,'ac':False,'dc':False}

        self.result = {}
        print('container initial sucessfully !!!')
    
    def load_analysis(self, simtype, analysis):
        self.sim_type[simtype] = True

        if(simtype == 'transient'):
            self.parse_transient(analysis)
        elif(simtype == 'dc'):
            self.parse_dc(analysis)
        elif(simtype == 'ac'):
            self.parse_ac(analysis)
            

    
    def del_analysis(self):
        self.sim_type = {'transient':False,'ac':False,'dc':False}
        self.result = {}
    
    def parse_transient(self, analysis):

        result_tran = {}
        result_tran['time'] = [float(i) for i in analysis.time]
        result_tran['nodes_name'] = list(analysis.nodes.keys())
        nodes = {}
        for i in result_tran['nodes_name'] :
            nodes[i] = [float(j) for j in analysis.nodes[i]]
        result_tran['nodes'] = nodes

        result_tran['branches_name'] = list(analysis.branches.keys())
        branches = {}
        for i in result_tran['branches_name']:
            branches[i] = [float(j) for j in analysis.branches[i]]
        result_tran['branches'] = branches

        self.result['transient'] = result_tran


    def parse_dc(self, analysis):
        result_dc = {}
        result_dc['sweep'] = [float(i) for i in analysis.sweep]
        result_dc['nodes_name'] = list(analysis.nodes.keys())

        nodes = {}
        for i in result_dc['nodes_name'] :
            nodes[i] = [float(j) for j in analysis.nodes[i]]
        result_dc['nodes'] = nodes

        result_dc['branches_name'] = list(analysis.branches.keys())
        branches = {}
        for i in result_dc['branches_name']:
            branches[i] = [float(j) for j in analysis.branches[i]]
        result_dc['branches'] = branches

        self.result['dc'] = result_dc


    def parse_ac(self, analysis):
        result_ac = {}
        result_ac['frequency'] = [float(i) for i in analysis.frequency]
        result_ac['nodes_name'] = list(analysis.nodes.keys())

        nodes_gain = {}
        nodes_phase = {}
        for i in result_ac['nodes_name'] :
            the_gain = 20*np.log10(np.absolute(analysis.nodes[i]))
            the_phase = np.angle(analysis.nodes[i], deg=False)
            # print(the_gain)
            nodes_gain[i] = [float(j) for j in the_gain]
            nodes_phase[i] = [float(j) for j in the_phase]

        result_ac['nodes_gain'] = nodes_gain
        result_ac['nodes_phase'] = nodes_phase
        # print(nodes_gain)
        # print(nodes_phase)

        result_ac['branches_name'] = list(analysis.branches.keys())
        branches_gain = {}
        branches_phase = {}
        for i in result_ac['branches_name']:
            the_gain = 20*np.log10(np.absolute(analysis.branches[i]))
            the_phase = np.angle(analysis.branches[i], deg=False)
            branches_gain[i] = [float(j) for j in the_gain]
            branches_phase[i] = [float(j) for j in the_phase]            
        result_ac['branches_gain'] = branches_gain
        result_ac['branches_phase'] = branches_phase


        self.result['ac'] = result_ac


    def simulation_info_request(self, simtype):
        return self.result[simtype]
