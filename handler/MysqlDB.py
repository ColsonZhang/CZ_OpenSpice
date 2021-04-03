import pymysql

# 数据库定义参数
database_ip = "localhost"
database_user = "guest"
database_passwd = "guest1234"
database_name = "GUESTDB"
table_name = "user_info"

DEBUG = False


class Mysql_DB():

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect()
    
    def connect(self):
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password,  database=self.database )
        print('connect mysql success !!!')

    def query(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except pymysql.OperationalError:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
        return cursor
    
    def __commit(self):
        try:
            self.conn.commit()
        except  pymysql.OperationalError:
            self.connect()
            self.conn.commit()
    
    def __rollback(self):
        try:
            self.conn.rollback()
        except  pymysql.OperationalError:
            self.connect()
            self.conn.rollback()        

    def DB_Check_byName(self,user_name):
        sql = "SELECT * FROM %s WHERE user_name='%s' " % (table_name,user_name)
        try:
            # 执行SQL语句
            cursor = self.query(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            if(results != tuple()):
                passwd = results[0][2]
                return passwd
            else:
                return False
        except:
            print("MYSQL ERROR 01 !")
            return False
    

    def DB_Check_byEmail(self,email):
        sql = "SELECT * FROM %s WHERE user_email='%s' " % (table_name,email)
        try:
            # 执行SQL语句
            cursor = self.query(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            if(results != tuple()):
                passwd = results[0][2]
                return passwd
            else:
                return False
        except:    
            print("MYSQL ERROR 02 !")
            return False        

    def DB_Insert_User(self,user_info):
        user_name = user_info["username"]
        user_passwd = user_info["password"]
        user_email = user_info["email"]
        user_date = user_info["date"]
        sql = "INSERT INTO user_info(user_name,user_passwd,user_email,user_register_date) VALUES('%s', '%s',  '%s', '%s' )"% (user_name, user_passwd, user_email, user_date)
        try:
            # 执行sql语句
            cursor = self.query(sql)
            # 执行sql语句
            self.__commit()
            if DEBUG:
                print("Insert %s successfully!"%(user_name))
            return True
        except:
            # 发生错误时回滚
            self.__rollback()    
            print("Mysql ERROR 03")
            return False

Mysql = Mysql_DB(host=database_ip,user=database_user, password=database_passwd,  database=database_name )
