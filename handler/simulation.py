
#----调用PySpice包----
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

#----调用模型库----
libraries_path = 'D:\\Project_2020\\SPICE\\Pyspice\\libraries'
#libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)

class Simulator_CZ :
    
    def __init__( self, title='simulation' ):
        self.circuit = Circuit(title)
    

    def Get_Spice( spice ):
        self.circuit.raw_spice += ".include D:\\Project_2020\\SPICE\\PySpice\\libraries\cmos\\180nm_cmos.mod" 
        self.circuit.raw_spice += spice 
    

    def Sim(sim_type,properties):
        parameter = self.Properties_Parse(sim_type,properties)
        self.simulator = self.circuit.simulator(temperature=25, nominal_temperature=25)
        if(sim_type == 'transient'):
            self.analysis = self.simulator.transient(step_time = parameter['step_time'],
                                                     end_time = parameter['end_time'],
                                                     start_time = parameter['start_time'],
                                                     max_time = parameter['max_time'], 
                                                     use_initial_condition = parameter['use_initial_condition'])
            pass
        elif(sim_type == 'dc' ):
            pass
        elif(sim_type == 'ac' ):
            pass
        else:
            pass
    
    def Properties_Parse(sim_type,properties):
        parameter = {}
        if(sim_type == 'transient'):
            parameter["step_time"] = 0
        pass 

