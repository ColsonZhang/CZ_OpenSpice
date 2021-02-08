import pymysql

# 数据库定义参数
database_ip = "localhost"
database_user = "guest"
database_passwd = "guest1234"
database_name = "GUESTDB"
table_name = "user_info"


# 打开数据库连接
db = pymysql.connect( database_ip, database_user, database_passwd, database_name )
print('open mysql success !!!')
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

def DB_Check_byName(user_name):
    sql = "SELECT * FROM %s WHERE user_name='%s' " % (table_name,user_name)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        passwd = results[0][2]
        return passwd
    except:
        print("There is no the user's info !")
        return False

def DB_Insert_User(user_info):
    user_name = user_info["username"]
    user_passwd = user_info["password"]
    user_email = user_info["email"]
    user_date = user_info["date"]
    sql = "INSERT INTO user_info(user_name,user_passwd,user_email,user_register_date) VALUES('%s', '%s',  '%s', '%s' )"% (user_name, user_passwd, user_email, user_date)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        print("Insert user_info successfully!")
        return True
    except:
        # 发生错误时回滚
        db.rollback()
        print("Insert user_info error!")
        return False


# if __name__ == "__main__":
#     res = authenticate('user5','1234')
#     print("authenticate result: ",res)
#     for i in range(10):
#         s = str(i)
#         res = add_user('user'+s,'1234','user'+s+'@qq.com')
#         print("add user", s ," res: ",res)
#     res = authenticate('user5','1234')
#     print("authenticate result: ",res)