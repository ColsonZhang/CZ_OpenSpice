from PySpice.Spice.Xyce.Server import XyceServer

Xyce_Path = 'D:\\Program Files\\Xyce 7.1 OPENSOURCE\\bin\\Xyce.exe'

spice_server = XyceServer( xyce_command = Xyce_Path )

def Simulation_Spice(spice_str):
    try:
        raw_file = spice_server(spice_str)

        waveforms = raw_file.nodes()
    
        return waveforms
    
    except:
        return False    

def Waveform_Keys(waveforms):
    waveform_keys = []
    for i in waveforms:
        waveform_keys.append(i.name)
    
    return waveform_keys

