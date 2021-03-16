from .main import AuthBaseHandler
from .js import js_import, js_code_1
import tornado.web
from .MongoDB import *
# from bokeh.embed import server_document
# from jinja2 import Environment, FileSystemLoader


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
        sim_type = self.get_argument('sim_type')
        properties = self.get_argument('properties')

        print("sim type:",sim_type)
        print("property:",properties)

        self.write("success")


class Schematic_Handler(AuthBaseHandler):
    
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
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