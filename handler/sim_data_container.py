

class Sim_Data_Container :
    def __init__(self):
        self.sim_type = {'transient':False,'ac':False,'dc':False}
        # self.analysis = None
        self.result = {}
        print('container initial sucessfully !!!')
    
    def load_analysis(self, simtype, analysis):
        print()
        self.sim_type[simtype] = True
        # self.analysis = analysis
        # print("loading analysising")
        if(simtype == 'transient'):
            self.parse_transient(analysis)

    
    def del_analysis(self):
        self.sim_type = {'transient':False,'ac':False,'dc':False}
        self.result = {}
    
    def parse_transient(self, analysis):
        # print('parsing the transient analysising !!!')
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

    def simulation_info_request(self, simtype):
        return self.result[simtype]
