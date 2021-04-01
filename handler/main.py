import tornado.web
from pycket.session import SessionMixin
from .MongoDB import *


class AuthBaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self): #重写get_current_user()方法
        return self.session.get('username',None) #session是一种会话状态，跟数据库的session可能不一样

#添加装饰器,装饰需要验证的请求
class IndexHandler(AuthBaseHandler):
    @tornado.web.authenticated   #@tornado.web.authenticated装饰器包裹get方法时，表示这个方法只有在用户合法时才会调用，authenticated装饰器会调用get_current_user()方法获取current_user的值，若值为False，则重定向到登录url装饰器判断有没有登录，如果没有则跳转到配置的路由下去，但是要在app.py里面设置login_url
    def get(self,*args,**kwargs):
        # self.render('main/index_Zh.html')
        username = self.get_current_user()
        self.render('index.html',user=username)

class TestHandler(AuthBaseHandler):
    
    @tornado.web.authenticated   #@tornado.web.authenticated装饰器包裹get方法时，表示这个方法只有在用户合法时才会调用，authenticated装饰器会调用get_current_user()方法获取current_user的值，若值为False，则重定向到登录url装饰器判断有没有登录，如果没有则跳转到配置的路由下去，但是要在app.py里面设置login_url
    def post(self,*args,**kwargs):
        username = self.get_current_user()
        message = self.get_argument('message')

        print('TestHandler: '+username+'   '+message)
        Mongo.connect(DataBase='example',Collection=username)
        Mongo.update(behavior=message,tags='test')

        self.write("success")

#添加装饰器,装饰需要验证的请求
class Index_Zh_Handler(AuthBaseHandler):
    
    @tornado.web.authenticated   
    def get(self,*args,**kwargs):
        self.render('main/index_Zh.html')

#添加装饰器,装饰需要验证的请求
class Index_En_Handler(AuthBaseHandler):
    
    @tornado.web.authenticated   
    def get(self,*args,**kwargs):
        self.render('main/index_En.html')

#添加装饰器,装饰需要验证的请求
class Open_Index_Zh_Handler(AuthBaseHandler):
    
    def get(self,*args,**kwargs):
        username = self.get_current_user()
        if username == None:
            self.render('main/open_index_Zh.html')
        else:
            self.render('main/index_Zh.html')

#添加装饰器,装饰需要验证的请求
class Open_Index_En_Handler(AuthBaseHandler):
    
    def get(self,*args,**kwargs):
        username = self.get_current_user()
        if username == None:
            self.render('main/open_index_En.html')
        else:
            self.render('main/index_En.html')