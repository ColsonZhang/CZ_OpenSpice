
# 切换 simulation source
# from .sim_xyce import *
from .sim_ngspice import *


from bokeh.plotting import figure
from bokeh import events
from bokeh.server.server import Server
from bokeh.themes import Theme
from bokeh.models import (AutocompleteInput, Button, CheckboxButtonGroup, CheckboxGroup,
                          ColorPicker, Column, ColumnDataSource, DataTable, DatePicker,
                          DateRangeSlider, DateSlider, Div, Dropdown, IntEditor,
                          MultiSelect, NumberEditor, NumberFormatter, Panel, Paragraph,
                          PreText, RadioButtonGroup, RadioGroup, RangeSlider, Row,
                          Select, SelectEditor, Slider, Spinner, StringEditor,
                          StringFormatter, TableColumn, Tabs, TextInput, Toggle,TextAreaInput)
from bokeh.layouts import column, row
from bokeh.models import CustomJS,CustomJSTransform


def bkapp(doc):

    def Callback_Button_Submit():
        circuit = str(Spice_Input.value)
        waveform = Simulation_Spice(circuit)
        if waveform != False:
            waveform_keys = Waveform_Keys(waveform)
            keys = '<p>' + str(waveform_keys) + '</p>'
        else:
            keys = '<p>Simulation Error !</p>'
            keys += '<p>'+ circuit +'</p>'
        Div_Result.text = keys 

    Spice_Input = TextAreaInput(title='SPICE',placeholder="Enter value ...",height=400, width=400,max_length=4000)

    Button_Submit = Button(label='Submit', button_type = "success")
    Button_Submit.on_click(Callback_Button_Submit)

    # Paragraph_Result = Paragraph(text="Waiting for the sim !")
    Div_Result = Div(text="<p>Waiting for the sim</p>")

    layout_1 = column(Spice_Input,Button_Submit,Div_Result)
    layout_top = column(layout_1)
    doc.add_root(layout_top)

server = Server({'/bkapp': bkapp},allow_websocket_origin=['localhost:8000','localhost:5006'])

def app_spice_begin():
    server.start()

def app_spice_start():
    # server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()