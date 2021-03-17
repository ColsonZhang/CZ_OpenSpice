
import re

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
    

    def Get_Spice(self, spice ):
        the_circuit = ".include D:\\Project_2020\\SPICE\\PySpice\\libraries\cmos\\180nm_cmos.mod \n" 
        the_circuit += spice
        self.circuit.raw_spice = the_circuit
    

    def Sim(self, sim_type,properties):

        parameter = self.Properties_Parse(sim_type,properties)
        print("parameter:\n",parameter)
        self.simulator = self.circuit.simulator(temperature=25, nominal_temperature=25)
        # print('simulator:\n',self.simulator)
        if(sim_type == 'transient'):
            self.analysis = self.simulator.transient(step_time = parameter['step_time'],
                                                     end_time = parameter['end_time'],
                                                     start_time = parameter['start_time'],
                                                     max_time = parameter['max_time'], 
                                                     use_initial_condition = parameter['use_initial_condition'])
            print(self.analysis)
            return self.analysis
        elif(sim_type == 'dc' ):
            pass
        elif(sim_type == 'ac' ):
            pass
        else:
            pass
        
    
    # 属性解析
    def Properties_Parse(self, sim_type,properties):
        parameter = {}
        if(sim_type == 'transient'):
            parameter["step_time"]  = self.unit_tran(properties["step_time"])
            parameter["end_time"]   = self.unit_tran(properties["end_time"])
            parameter["start_time"] = self.unit_tran(properties["start_time"])
            parameter["max_time"]   = self.unit_tran(properties["max_time"])
            parameter["use_initial_condition"] = self.unit_tran(properties["use_initial_condition"])

        elif(sim_type == 'dc' ):
            pass
        elif(sim_type == 'ac' ):
            pass

        return parameter

    # 单位转换函数
    def unit_tran(self , value_raw):
        # 匹配数字的正则表达式
        regInt = '\d+'
        regFloat  = '^\d+\.\d+'
        regNumber = regFloat + '|' + regInt
        pattern_number = re.compile(regNumber)

        # 匹配字符的正则表达式
        regChars = '([a-z]+)'
        pattern_char = re.compile(regChars, re.I)

        # 进行数字和单位的提取
        unit_chars = pattern_char.findall(value_raw)
        unit_num = pattern_number.findall(value_raw)

        # 进行格式转换
        # 有单位时的情况
        if(unit_chars != []):   
            the_unit = unit_chars[0]

            if the_unit in ['true','TRUE','True']:
                return True
            
            elif the_unit in ['false','FALSE','False']:
                return False

            elif the_unit in ['none','NONE','None']:
                return None

            elif the_unit in ['us','US','uS','Us']:
                if(unit_num != []):
                    the_num = float(unit_num[0])
                else:
                    the_num = float(0)
                return u_us(the_num)

            elif the_unit in ['ms','MS','mS','Ms']:
                if(unit_num != []):
                    the_num = float(unit_num[0])
                else:
                    the_num = float(0)     
                return u_us(the_num)      
         # 无单位时的情况
        else:  
            if(unit_num != []):
                the_num = float(unit_num[0])
            else:
                the_num = float(0)            
            return the_num
        pass


