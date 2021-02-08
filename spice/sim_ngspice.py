import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.NgSpice.Shared import NgSpiceShared

def Simulation_Spice(spice_str):
    ngspice = NgSpiceShared.new_instance()
    try:
        ngspice.load_circuit(spice_str)
        ngspice.run()
        plot_names =  ngspice.plot_names
        return plot_names
    except:
        return False    

def Waveform_Keys(waveforms):
    
    return waveforms