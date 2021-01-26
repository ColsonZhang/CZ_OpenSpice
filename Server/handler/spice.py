from .main import AuthBaseHandler
from .js import js_import, js_code_1
import tornado.web
# from bokeh.embed import server_document
# from jinja2 import Environment, FileSystemLoader




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