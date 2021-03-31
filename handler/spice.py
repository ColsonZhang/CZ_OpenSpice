from .main import AuthBaseHandler
from .js import js_import, js_code_1
import tornado.web
from .MongoDB import *
from .simulation import Simulator_CZ
from .sim_data_container import Sim_Data_Container
from tornado.escape import json_decode, json_encode, utf8
import json


# from bokeh.embed import server_document
# from jinja2 import Environment, FileSystemLoader

Container_SimResult = Sim_Data_Container()

class SpiceHandler(AuthBaseHandler):
    
    @tornado.web.authenticated   #@tornado.web.authenticated装饰器包裹get方法时，表示这个方法只有在用户合法时才会调用，authenticated装饰器会调用get_current_user()方法获取current_user的值，若值为False，则重定向到登录url装饰器判断有没有登录，如果没有则跳转到配置的路由下去，但是要在app.py里面设置login_url
    def post(self,*args,**kwargs):
        username = self.get_current_user()
        message = self.get_argument('spice')

        print('SpiceHandler: '+username+' \n'+message)
        Mongo.connect(DataBase='example',Collection=username)
        Mongo.update(behavior=message,tags='spice')

        self.write("success")


class SimulationHandler(AuthBaseHandler):

    @tornado.web.authenticated
    def post(self,*args,**kwargs):
        username = self.get_current_user()

        sim_type = self.get_argument('sim_type')
        properties_str = self.get_argument('properties')
        spice = self.get_argument('spice')

        properties = properties_transform(properties_str)

        # print("sim type:",sim_type)
        # print("property:",properties_str)
        # print("spice   :\n",spice)

        simulator = Simulator_CZ()
        simulator.Get_Spice(spice)
        analysis = simulator.Sim(sim_type,properties)
        print('properties:\n',properties)
        print('simulation finished !')         

        Container_SimResult.load_analysis(sim_type,analysis)
        print('data container load data successfully!! ')

        message = "Sim_Type="+ sim_type + "\n Properties=" +properties_str 
        Mongo.connect(DataBase='example',Collection=username)
        Mongo.update(behavior=message,tags='simulation',spice=spice)

        self.write("success")


# 将properties 从字符串类型解析出来
# todo: 转换为json解析
def properties_transform(properties_str):
    properties = {}
    attributes = properties_str.split(";")
    # print(attributes)
    for attr in attributes:
        if(attr != ''):
            term = attr.split("=")
            properties[term[0]] = term[1]
    return properties 


class SimulationInfoRequest_Handler(AuthBaseHandler):
    @tornado.web.authenticated
    def post(self,*args,**kwargs):
        username = self.get_current_user()

        sim_type = self.get_argument('sim_type')

        print(sim_type)

        sim_info = Container_SimResult.simulation_info_request(sim_type)

        # print(sim_info)

        sim_info_json = json.dumps( sim_info )
        # print('json transform ok !!')

        message = "Sim_Type="+ sim_type 
        Mongo.connect(DataBase='example',Collection=username)
        Mongo.update(behavior=message,tags='show_result')

        self.write( sim_info_json )
        # print("send the simulation info request successfully!!!")

        # self.write(json_decode(sim_info))
        # self.write("successful")



class Schematic_Handler(AuthBaseHandler):
    
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        username = self.get_current_user()
        message = 'Open the Schematic'
        Mongo.connect(DataBase='example',Collection=username)
        Mongo.update(behavior=message,tags='schematic')

        self.render('schematic/schematic.html')


class Spice_1_Handler(AuthBaseHandler):

    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        self.render('spice/spice1.html')
        # script = server_document('http://localhost:5006/bkapp')
        # self.render('spice/spice1.html',script=script)

class Spice_2_Handler(AuthBaseHandler):
    
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        self.render('spice/spice2.html',js_import=js_import,js_code=js_code_1)


class Spice_3_Handler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        self.render('spice/spice3.html')


class Spice_4_Handler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        self.render('spice/spice4.html')