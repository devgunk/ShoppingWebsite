from pymysql import *

class connection:
    def connection(self):
        conn = Connect('127.0.0.1',"root",'','demoproject')
        return conn