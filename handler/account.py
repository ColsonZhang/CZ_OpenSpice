import datetime
from .MysqlDB import *

#用户密码匹配判断函数
def authenticate(username,password):
    passwd_db = DB_Check_byName(username)
    if passwd_db:
        if password == passwd_db:
            return True
    return False

# 数据库中增加新用户
def add_user(username,password,email=''):
    create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = DB_Insert_User({'username':username,'password':password,'email':email,'date':create_time})
    return result

def check_register(username,password,email):
    check_name = DB_Check_byName(username)
    check_email = DB_Check_byEmail(email)
    check_pw = check_password(password)

    if check_name != False:
        return 1
    if check_email != False:
        return 2
    if check_pw == False:
        return 3
    
    return 0

    
def check_password(password):
    if(len(password)<4):
        return False
    
    return True

# USER_DATA = {
#     'name':'user1',
#     'password':'1234'
# }

# USER_DB = [USER_DATA]

# def authenticate(username,password):#用户密码匹配判断函数
#     if username and password:
#         for i in USER_DB:            
#             if username == i['name'] and password == i['password']: #是否与保存的一致
#                 return True
#     return False

# def add_user(username,password):
#     USER_DB.append({'name':username,'password':password})