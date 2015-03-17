# coding: utf-8

import sys
sys.path.append("../")

import mysql.connector
from mysql.connector import (connection)
from Master import Master

class DAO:
    
    config = {
        'user': 'root',
        'password': 'ifpbinfo',
        'host': '127.0.0.1',
        'database': 'suniscoming'
    }
    
    @staticmethod
    def getConnection():
        try:
            cnx = mysql.connector.connect(**DAO.config)
            return cnx
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            raise Exception
    
    @staticmethod
    def closeConnection(cnx):
        if cnx != None:
            cnx.close()
    
    @staticmethod
    def closeConnection(cnx, cursor):
        if cursor != None:
            cursor.close()
        if cnx != None:
            cnx.close()
    
    @staticmethod
    def executeInsert(sql, parameters_tuple):
        try:
            cnx = DAO.getConnection()
            cursor = cnx.cursor(buffered=True)
            cursor.execute(sql, parameters_tuple)
            _id = cursor.lastrowid
            cnx.commit()
        except mysql.connector.Error as err:
            print (err)
            return False
        else:
            return _id
        finally:
            DAO.closeConnection(cnx, cursor)
    
    @staticmethod
    def executeUpdate(sql, parameters_tuple):
        try:
            cnx = DAO.getConnection()
            cursor = cnx.cursor(buffered=True)
            cursor.execute(sql, parameters_tuple)
            cnx.commit()
        except mysql.connector.Error as err:
            print (err)
            return False
        else:
            return True
        finally:
            DAO.closeConnection(cnx, cursor)
    
    @staticmethod
    def executeQuery(sql, parameters_tuple):
        try:
            cnx = DAO.getConnection()
            cursor = cnx.cursor(buffered=True)
            cursor.execute(sql, parameters_tuple)
        except mysql.connector.Error as err:
            print (err)
        finally:
            # why not work with one argument?
            DAO.closeConnection(cnx, None)
            return cursor

class MasterCRUD:
    
    @ staticmethod
    def insertMaster(master):
        sql = ("INSERT INTO tb_master (nm_email, nm_password) " \
                             "VALUES ( %s, %s )")
        parameters_tuple = (master.email, master.password)
        _id = DAO.executeInsert(sql, parameters_tuple)
        return _id
    
    @ staticmethod
    def updateMaster(master):
        sql = ("UPDATE tb_master SET " \
               " nm_email = %s, " \
               " nm_password = %s, " \
               " nr_killed = %s, " \
               " nr_life = %s " \
               " WHERE id_master = %s ")
        parameters_tuple = (master.email, master.password, master.killed, master.life, master.idMaster)
        return DAO.executeUpdate(sql, parameters_tuple)
    
    @ staticmethod
    def getMasterByLogin(master):
        sql = ("SELECT id_master, nm_email, nm_password, nr_killed, nr_life, dt_record " \
               " FROM tb_master " \
               " WHERE nm_email = '%s'" % master.email)
        cursor = DAO.executeQuery(sql, None)
        masters = MasterCRUD.getListMaster(cursor)
        if masters != []:
            _master = None
            _master = masters[0]
            if _master != None:
                if _master.password == master.password:
                    _master.password = None
                    return _master
                else:
                    return "Senha Incorreta!"
        else:
            return "Email incorreto!"
    
    @ staticmethod
    def getMasterByEmail(master):
        sql = ("SELECT id_master, nm_email, nm_password, nr_killed, nr_life, dt_record " \
               " FROM tb_master " \
               " WHERE nm_email = '%s'" % master.email)
        cursor = DAO.executeQuery(sql, None)
        masters = MasterCRUD.getListMaster(cursor)
        if masters != []:
            _master = None
            _master = masters[0]
            if _master != None:
                return _master
    
    @ staticmethod
    def getAll():
        sql = ("SELECT id_master, nm_email, nm_password, nr_killed, nr_life, dt_record " \
               " FROM tb_master ")
        cursor = DAO.executeQuery(sql, None)
        masters = MasterCRUD.getListMaster(cursor)
        return masters
    
    @ staticmethod
    def getListMaster(cursor):
        
        masters = []
        
        for (id_master, nm_email, nm_password, nr_killed, nr_life, dt_record) in cursor:
            master = Master()
            master.idMaster = id_master
            master.email = nm_email
            master.password = nm_password
            master.killed = nr_killed
            master.life = nr_life
            master.dateRecord = dt_record
            
            masters.append(master)
        
        return masters

if __name__ == '__main__':
    
    from Master import Master
    
    # INSERT done!
    """master = Master(email='erijonhson.os@gmail.com', password='ABC123')
    _id = MasterCRUD.insertMaster(master)
    print _id, "\o/" """
    
    # UPDATE done!
    """master = Master(idMaster= 1, email='eri.os@gmail.com', password='ABC', killed=100, life=100)
    MasterCRUD.updateMaster(master)"""
    
    # LOGIN done!
    """master = Master(idMaster= 1, email='eri.os@gmail.com', password='ABC')
    m = MasterCRUD.getMasterByLogin(master)
    if isinstance(m, Master):
        print m.toString()"""
    
    # INSERT done
    """master = Master(email='citycold.ordan@gmail.com', password='ABC123')
    _id = MasterCRUD.insertMaster(master)"""
    
    # INSERT done
    """master = Master(email='abcdf.ghij@outlook.com', password='ABC123')
    _id = MasterCRUD.insertMaster(master)"""
 
    # SELECT done!
    """master = Master(idMaster= 1, email='eri.os@gmail.com')
    m = MasterCRUD.getMasterByEmail(master)
    if isinstance(m, Master):
        print m.toString()"""

    # SELECT done!
    """ms = MasterCRUD.getAll()
    if ms != []:
        for m in ms:
            print m.toString()
            print "--------------------" """
    
    