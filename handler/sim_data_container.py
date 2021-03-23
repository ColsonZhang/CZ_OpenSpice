

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
            pass
            

    
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

    def simulation_info_request(self, simtype):
        return self.result[simtype]
