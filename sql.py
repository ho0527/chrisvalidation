import datetime
import MySQLdb
import mysql.connector as mysql
import psycopg2
from psycopg2.extras import RealDictCursor
from MySQLdb.cursors import DictCursor
from mysql.connector import Error
from django.http import JsonResponse

# 自創
from .thing import *

DBSETTING={
    "host": "localhost",
    "username": "root",
    "password": "",
    "port": 3306,
    "defaulttable": "tablename",
    "sqltype": "mysql"
}

# main START
def createdb(dbname,host="localhost",username="root",password="",port="3306"):
    return MySQLdb.connect(host=host,db=dbname,user=username,passwd=password,port=port)

def query(dbname,query,data=None,setting=DBSETTING):
    if setting["sqltype"]=="pgsql":
        response=None
        try:
            db=psycopg2.connect(
                host=setting["host"],
                dbname=dbname,
                user=setting["username"],
                password=setting["password"],
                port=setting["port"]
            )
            cursor=db.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query,data)
            response=cursor.fetchall()
            db.commit()
            printcolorhaveline("green","use query function SUCCESS","")
        except Exception as error:
            printcolorhaveline("fail","[ERROR] use query function error " + str(error),"")
            db=psycopg2.connect(
                host=setting["host"],
                dbname=dbname,
                user=setting["username"],
                password=setting["password"],
                port=setting["port"]
            )
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
        return response
    else:
        response=None  # 修正拼寫錯誤 from respone to response
        try:
            db=MySQLdb.connect(
                host=setting["host"],
                db=dbname,
                user=setting["username"],
                passwd=setting["password"],
                port=setting["port"]
            )
            cursor=db.cursor(DictCursor)
            cursor.execute(query,data)
            response=cursor.fetchall()
            db.commit()
            printcolorhaveline("green","use query function SUCCESS","")
        except Exception as error:
            printcolorhaveline("fail","[ERROR] use query function error " + str(error),"")
            db=MySQLdb.connect(
                host=setting["host"],
                db=dbname,
                user=setting["username"],
                passwd=setting["password"],
                port=setting["port"]
            )
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
        return response