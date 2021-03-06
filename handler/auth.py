from .main import AuthBaseHandler
from .account import authenticate, add_user, check_register
from .MongoDB import *

DEBUG = False

class LoginHandler(AuthBaseHandler):
    def get(self,*args,**kwargs):
        self.render('auth/login.html')

    def post(self,*args,**kwargs):
        username = self.get_argument('username',None)
        password = self.get_argument('password',None)

        # check the password
        passed = authenticate(username,password)

        if passed:
            # 保存cookie信息到redis数据库
            self.session.set('username',username) #将前面设置的cookie设置为username，保存用户登录信息
            if DEBUG:
                print(self.session.get('username')+' login success !!!')
            next_url = self.get_argument('next', '')  # 获取之前页面的路由
            if next_url:
                Mongo.connect(DataBase='example',Collection=username)
                Mongo.update(behavior='login',tags='auth')
                self.redirect(next_url) #跳转主页路由
            else:
                Mongo.connect(DataBase='example',Collection=username)
                Mongo.update(behavior='login',tags='auth')
                self.redirect('/index')
        else:
            self.write({'msg':'login fail'}) #不通过，有问题        



class LogoutHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        Mongo.connect(DataBase='example',Collection=self.get_current_user())
        Mongo.update(behavior='logout',tags='auth')
        #self.session.set('username','') #将用户的cookie清除
        self.session.delete('username')
        self.redirect('/login')

    # def post(self,*args,**kwargs):
    #     self.session.delete('username')
    #     self.redirect('/login')

class RegisterHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        if DEBUG:
            print('register')
        self.render('auth/register.html')

    def post(self, *args, **kwargs):
        if DEBUG:
            print('registerpost')

        username = self.get_argument('username','')
        email = self.get_argument('email','')
        password1 = self.get_argument('password1','')
        password2 = self.get_argument('password2','')

        if username and password1 and (password1 == password2):
            flag_checck = check_register(username,password1,email)
            if flag_checck == 0:
                success = add_user(username,password1,email)
                if success:
                    Mongo.connect(DataBase='example',Collection=username)
                    Mongo.update(behavior='register',tags='auth')
                    self.redirect('/login')
                else:
                    self.write({'msg':'register fail'})
            elif flag_checck == 1:
                self.write({'msg':'the username is not avaliable!'})
            elif flag_checck == 2:
                self.write({'msg':'the email is not avaliable!'})
            elif flag_checck == 3:
                self.write({'msg':'the password is too shor!'})                        
                
        else:
            if DEBUG:
                print('register again')
            self.render('auth/register.html')