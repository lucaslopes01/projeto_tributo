# -*- coding: utf-8 -*-
"""
Classe para chamadas simples
"""
import pymysql
#import pymysql as MySQLdb
from datetime import datetime
import os
 
 
class BDMySQL:
    def __init__(self, pDatabase):
        vHost = os.getenv('MYSQL_HOST')
        vUser = os.getenv('MYSQL_USR')
        vPass = os.getenv('MYSQL_PWD')
        vPort = os.getenv('MYSQL_PORT')
        vDb = pDatabase
        self.conn = pymysql.connect(host=vHost, port=int(vPort), user=vUser, passwd=vPass, db=vDb, charset='utf8', use_unicode=True, cursorclass=pymysql.cursors.DictCursor)
 
    def __del__(self):
        self.conn.close()
 
    def retorna_query(self, pSQL):
        return self.__returnQuery(pSQL)
 
    def processa_comando(self, pSQL):
        self.__ExecQuery(pSQL)
 
    def __returnQuery(self, pSQL):
        #Retorna o resultado da query
        c = self.conn.cursor()
        c.execute(pSQL)
        ret = c.fetchall()
        c.close()
        return ret
 
    def returnNow(self):
        #Retorna a data atual no formato de MySQL
        current = datetime.now()
        return "{0}-{1}-{2}".format(current.year, current.month, current.day)
 
    #Exec updates and inserts
    def __ExecQuery(self, query):
        """
        Executa queryes de insert, update e delete
        """
        if query:
            ex = self.conn.cursor()
            ex.execute(query)
            self.conn.commit()