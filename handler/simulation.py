
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
# libraries_path = 'D:\\Project_2020\\SPICE\\Pyspice\\libraries'
libraries_path = '/root/workspace/libraries'
#libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)

DEBUG = False

class Simulator_CZ :
    
    def __init__( self, title='simulation' ):
        self.circuit = Circuit(title)
    

    def Get_Spice(self, spice ):
        # the_circuit = ".include D:\\Project_2020\\SPICE\\PySpice\\libraries\cmos\\180nm_cmos.mod \n"
        the_circuit = ".include /root/workspace/libraries/cmos/180nm_cmos.mod \n"

        the_circuit += spice
        self.circuit.raw_spice = the_circuit
    

    def Sim(self, sim_type,properties):

        parameter = self.Properties_Parse(sim_type,properties)
        if DEBUG:
            print("parameter:\n",parameter)
        self.simulator = self.circuit.simulator(temperature=25, nominal_temperature=25)
        # print('simulator:\n',self.simulator)
        if(sim_type == 'transient'):
            self.analysis = self.simulator.transient(step_time = parameter['step_time'],
                                                     end_time = parameter['end_time'],
                                                     start_time = parameter['start_time'],
                                                     max_time = parameter['max_time'], 
                                                     use_initial_condition = parameter['use_initial_condition'])
            return self.analysis
        elif(sim_type == 'dc' ):
            if DEBUG:
                print("doing the dc simulation !!!")
            src_name = parameter['src_name']
            vstart = parameter['start']
            vstop = parameter['stop']
            vstep = parameter['step']
            the_args = "{} = slice({},{},{})".format(src_name, vstart, vstop, vstep)

            exec("self.analysis = self.simulator.dc( {} )".format(the_args))
            if DEBUG:
                print("dc simulation finished !!!")

            return self.analysis

        elif(sim_type == 'ac' ):
            if DEBUG:
                print("doing the ac simulation !!!")
            self.analysis = self.simulator.ac(  start_frequency = parameter['start_frequency'],
                                                stop_frequency = parameter['stop_frequency'],
                                                number_of_points = parameter['number_of_points'],
                                                variation = parameter['variation'])
            if DEBUG:
                print("dc simulation finished !!!")
            return self.analysis

            
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
            parameter["src_name"]   = properties["src"]
            parameter["start"]      = properties["start"]
            parameter["stop"]      = properties["stop"]
            parameter["step"]      = properties["step"]

        elif(sim_type == 'ac' ):
            parameter["start_frequency"]  = self.unit_tran(properties["start_frequency"])
            parameter["stop_frequency"]   = self.unit_tran(properties["stop_frequency"])
            parameter["number_of_points"] = int(properties["number_of_points"])
            parameter["variation"]        = properties["variation"]

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

            elif the_unit in ['ps','Ps','pS','PS']:
                the_num = self.get_the_number(unit_num)
                return u_ps(the_num)

            elif the_unit in ['ns','Ns','nS','NS']:
                the_num = self.get_the_number(unit_num)
                return u_ns(the_num)                
                
            elif the_unit in ['us','US','uS','Us']:
                the_num = self.get_the_number(unit_num)
                return u_us(the_num)

            elif the_unit in ['ms','mS']:
                the_num = self.get_the_number(unit_num)   
                return u_ms(the_num)
            
            elif the_unit in ['s','S']:
                the_num = self.get_the_number(unit_num)   
                return u_s(the_num)            

            elif the_unit in ['ks','Ks','kS','KS']:
                the_num = self.get_the_number(unit_num)
                return u_ks(the_num)
                
            elif the_unit in ['Ms','MS']:
                the_num = self.get_the_number(unit_num)
                return u_Ms(the_num)

            
            elif the_unit in ['hz','Hz','HZ']:
                the_num = self.get_the_number(unit_num)  
                return u_Hz(the_num)
            
            elif the_unit in ['kHz','KHz','khz','Khz','kHZ','KHZ']:
                the_num = self.get_the_number(unit_num)
                return u_kHz(the_num)
                
            elif the_unit in ['MHz','Mhz','MHZ']:
                the_num = self.get_the_number(unit_num)
                return u_MHz(the_num)
            
            elif the_unit in ['gHz','GHz','ghz','Ghz','gHZ','GHZ']:
                the_num = self.get_the_number(unit_num)
                return u_GHz(the_num)
            
            elif the_unit in ['mHz','mhz','mHZ']:
                the_num = self.get_the_number(unit_num)
                return u_mHz(the_num)

            elif the_unit in ['uHz','UHz','uhz','Uhz','uHZ','UHZ']:
                the_num = self.get_the_number(unit_num)
                return u_uHz(the_num)
            
            elif the_unit in ['nHz','NHz','nhz','Nhz','nHZ','NHZ']:
                the_num = self.get_the_number(unit_num)
                return u_nHz(the_num)
            
            elif the_unit in ['pHz','PHz','phz','Phz','pHZ','PHZ']:
                the_num = self.get_the_number(unit_num)
                return u_pHz(the_num)



        # 无单位时的情况
        else:  
            if(unit_num != []):
                the_num = float(unit_num[0])
            else:
                the_num = float(0)            
            return the_num
        

    def get_the_number(self, the_unit_num):

        if(the_unit_num != []):
            the_num = float(the_unit_num[0])
        else:
            the_num = float(0)

        return the_num   


# 'u_A', 'u_Bq', 'u_C', 'u_Degree', 'u_F', 'u_GA', 'u_GBq', 'u_GC', 'u_GDegree', 'u_GF', 'u_GGy', 'u_GH', 'u_GHz', 'u_GJ',
# 'u_GK', 'u_GN', 'u_GOhm', 'u_GPa', 'u_GS', 'u_GSv', 'u_GV', 'u_GW', 'u_GWb', 'u_Gcd', 'u_Gkat', 'u_Glm', 'u_Glx', 'u_Gm',
# 'u_Gmol', 'u_Grad', 'u_Gs', 'u_Gsr', 'u_Gy', 'u_GΩ', 'u_H', 'u_Hz', 'u_J', 'u_K', 'u_MA', 'u_MBq', 'u_MC', 'u_MDegree', 
# 'u_MF', 'u_MGy', 'u_MH', 'u_MHz', 'u_MJ', 'u_MK', 'u_MN', 'u_MOhm', 'u_MPa', 'u_MS', 'u_MSv', 'u_MV', 'u_MW', 'u_MWb', 
# 'u_Mcd', 'u_Mkat', 'u_Mlm', 'u_Mlx', 'u_Mm', 'u_Mmol', 'u_Mrad', 'u_Ms', 'u_Msr', 'u_MΩ', 'u_N', 'u_Ohm', 'u_Pa', 'u_S', 
# 'u_Sv', 'u_TA', 'u_TBq', 'u_TC', 'u_TDegree', 'u_TF', 'u_TGy', 'u_TH', 'u_THz', 'u_TJ', 'u_TK', 'u_TN', 'u_TOhm', 'u_TPa', 
# 'u_TS', 'u_TSv', 'u_TV', 'u_TW', 'u_TWb', 'u_Tcd', 'u_Tkat', 'u_Tlm', 'u_Tlx', 'u_Tm', 'u_Tmol', 'u_Trad', 'u_Ts', 'u_Tsr', 
# 'u_TΩ', 'u_V', 'u_W', 'u_Wb', 'u_cd', 'u_kA', 'u_kBq', 'u_kC', 'u_kDegree', 'u_kF', 'u_kGy', 'u_kH', 'u_kHz', 'u_kJ', 'u_kK', 
# 'u_kN', 'u_kOhm', 'u_kPa', 'u_kS', 'u_kSv', 'u_kV', 'u_kW', 'u_kWb', 'u_kat', 'u_kcd', 'u_kkat', 'u_klm', 'u_klx', 'u_km', 
# 'u_kmol', 'u_krad', 'u_ks', 'u_ksr', 'u_kΩ', 'u_lm', 'u_lx', 'u_m', 'u_mA', 'u_mBq', 'u_mC', 'u_mDegree', 'u_mF', 'u_mGy', 
# 'u_mH', 'u_mHz', 'u_mJ', 'u_mK', 'u_mN', 'u_mOhm', 'u_mPa', 'u_mS', 'u_mSv', 'u_mV', 'u_mW', 'u_mWb', 'u_mcd', 'u_mkat', 
# 'u_mlm', 'u_mlx', 'u_mm', 'u_mmol', 'u_mol', 'u_mrad', 'u_ms', 'u_msr', 'u_mΩ', 'u_nA', 'u_nBq', 'u_nC', 'u_nDegree', 'u_nF', 
# 'u_nGy', 'u_nH', 'u_nHz', 'u_nJ', 'u_nK', 'u_nN', 'u_nOhm', 'u_nPa', 'u_nS', 'u_nSv', 'u_nV', 'u_nW', 'u_nWb', 'u_ncd', 
# 'u_nkat', 'u_nlm', 'u_nlx', 'u_nm', 'u_nmol', 'u_nrad', 'u_ns', 'u_nsr', 'u_nΩ', 'u_pA', 'u_pBq', 'u_pC', 'u_pDegree', 
# 'u_pF', 'u_pGy', 'u_pH', 'u_pHz', 'u_pJ', 'u_pK', 'u_pN', 'u_pOhm', 'u_pPa', 'u_pS', 'u_pSv', 'u_pV', 'u_pW', 'u_pWb', 
# 'u_pcd', 'u_pkat', 'u_plm', 'u_plx', 'u_pm', 'u_pmol', 'u_prad', 'u_ps', 'u_psr', 'u_pΩ', 'u_rad', 'u_s', 'u_sr', 'u_uA', 
# 'u_uBq', 'u_uC', 'u_uDegree', 'u_uF', 'u_uGy', 'u_uH', 'u_uHz', 'u_uJ', 'u_uK', 'u_uN', 'u_uOhm', 'u_uPa', 'u_uS', 'u_uSv', 
# 'u_uV', 'u_uW', 'u_uWb', 'u_ucd', 'u_ukat', 'u_ulm', 'u_ulx', 'u_um', 'u_umol', 'u_urad', 'u_us', 'u_usr', 'u_Ω', 'u_μA', 
# 'u_μBq', 'u_μC', 'u_μF', 'u_μGy', 'u_μH', 'u_μHz', 'u_μJ', 'u_μK', 'u_μN', 'u_μPa', 'u_μS', 'u_μSv', 'u_μV', 'u_μW', 'u_μWb', 
# 'u_μcd', 'u_μkat', 'u_μlm', 'u_μlx', 'u_μm', 'u_μmol', 'u_μrad', 'u_μs', 'u_μsr', 'u_μΩ',