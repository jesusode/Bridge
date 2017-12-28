
import sys

import os

import time


#zxJDBC ya viene incluido en jython

if 'java' in sys.platform:

    from jarray import *

    import com #Sin esto no reconoce el driver del MySQL (por que?????????)

    from com.ziclix.python.sql import zxJDBC

    #driver SQLServer

    sys.path.append(os.getcwd() + "/javalib/jtds-1.2.5.jar")

    #driver SQLite

    sys.path.append(os.getcwd() + "/javalib/sqlitejdbc-v056.jar")

    #driver MySQL

    sys.path.append(os.getcwd() +  "/javalib/mysql-connector-java-5.1.18-bin.jar")
    #print sys.path

                    

    from com.ziclix.python.sql import zxJDBC

    import java.sql

    import org.sqlite.JDBC

    import net.sourceforge.jtds.jdbc.Driver


    ####Patch para cargar drivers JDBC-----------------------------------------

    class classPathHacker(object):

        """Original Author: SG Langer Jan 2007, conversion from Java to Jython

        Updated version (supports Jython 2.5.2) From http://glasblog.1durch0.de/?p=846

        

        Purpose: Allow runtime additions of new Class/jars either from

        local files or URL

        """

        import java.lang.reflect.Method

        import java.io.File

        import java.net.URL

        import java.net.URLClassLoader

        import jarray

     

        def addFile(self, s):

            """Purpose: If adding a file/jar call this first

            with s = path_to_jar"""

            # make a URL out of 's'

            f = self.java.io.File(s)

            u = f.toURL()

            a = self.addURL(u)

            return a

     

        def addURL(self, u):

            """Purpose: Call this with u= URL for

            the new Class/jar to be loaded"""

            sysloader = self.java.lang.ClassLoader.getSystemClassLoader()

            sysclass = self.java.net.URLClassLoader

            method = sysclass.getDeclaredMethod("addURL", [self.java.net.URL])

            a = method.setAccessible(1)

            jar_a = self.jarray.array([u], self.java.lang.Object)

            b = method.invoke(sysloader, [u])

            return u

        

    ##END-------------------------------------------------------------------------



    #JYTHON-JDBC--------------------------------------------------

    jarLoad = classPathHacker()

    resx = jarLoad.addFile('javalib/sqlitejdbc-v056.jar')

    resx = jarLoad.addFile('javalib/jtds-1.2.5.jar')

    resx=  jarLoad.addFile('javalib/mysql-connector-java-5.1.18-bin.jar')    
    
    sqlite_driver=None
    
    try:
        sqlite_driver=org.sqlite.JDBC()
        java.sql.DriverManager.registerDriver(sqlite_driver)
    except:
        pass
    try:
        mssql_driver=net.sourceforge.jtds.jdbc.Driver()
        java.sql.DriverManager.registerDriver(mssql_driver)
    except:
        pass
    try:
        mysql_driver=com.mysql.jdbc.Driver()
        java.sql.DriverManager.registerDriver(mysql_driver)    
    except:
        pass

    #-------------------------------------------------------------



    def connectJDBC(*args):

        '''
        Conectar a una BD usando JDBC 
        '''

        available_dbs=['sqlite','sqlserver','access','mysql','oracle','excel','text','postgres']

        if len(args)!=5:

            msg='''Numero incorrecto de argumentos para la funcion.
            La sintaxis correcta es connectJDBC(server_name,nombre_db,type,user,password)'''

            raise Exception(msg)



        if not args[2] in available_dbs:

            raise Exception('Error: El tipo de base de datos "%s" no es uno de los soportados'%args[2])



        server=args[0]

        dbname=args[1]

        dbtype=args[2]

        user=args[3]

        passw=args[4]

        driver=None

        url=None

        #Crear la conexion en funcion del tipo de base de datos

        if dbtype=='sqlserver':

            url='jdbc:jtds:sqlserver://' + server + '/' + dbname

            driver='net.sourceforge.jtds.jdbc.Driver'

            return zxJDBC.connect(url, user, passw, driver)

            

        elif dbtype=='excel':

            url='jdbc:odbc:Driver={Microsoft Excel Driver (*.xls)};DBQ=%s;READONLY=false'% dbname

            #print url

            driver='sun.jdbc.odbc.JdbcOdbcDriver'

            return zxJDBC.connect(url, user, passw, driver)

            

        elif dbtype=='access':

            #url='jdbc:odbc:Driver={Microsoft Access Driver (*.mdb)};DBQ=%s;DriverID=22;READONLY=false;UID=%s;Pwd=%s'% (dbname,user,passw)

            url='jdbc:odbc:Driver={Microsoft Access Driver (*.mdb)};DBQ=%s;UID=%s;Pwd=%s'% (dbname,user,passw)

            driver='sun.jdbc.odbc.JdbcOdbcDriver'

            return zxJDBC.connect(url, user, passw, driver)

        

        elif dbtype=='text':

            return None    

            

        elif dbtype=='mysql':

            #jdbc:mysql://localhost:3306/mysql

            url='jdbc:mysql:' + server + '/' + dbname

            #print url

            driver='com.mysql.jdbc.Driver'

            return zxJDBC.connect(url, user, passw, driver)



        elif dbtype=='sqlite':   

            jdbc_url    = "jdbc:sqlite:%s"  % dbname

            jdbc_driver = "org.sqlite.JDBC"

            return zxJDBC.connect(jdbc_url, None, None, jdbc_driver)

            

        elif dbtype=='oracle':

            return SYMTAB['__NULL__']



    def queryJDBCConnection(*args): #OK
        '''
        Hace una query y almacena el resultado en una lista
        '''

        if len(args)!=2:

            msg='''Numero incorrecto de argumentos para la funcion.
            La sintaxis correcta es queryJDBCConnection(connection,query)'''
            raise Exception(msg)

        results=[]

        conn = args[0]

        query=args[1]

        cursor=conn.cursor()

        cursor.execute(query)

        if cursor.rowcount not in [None,-1]:

            for item in cursor:

                #print item

                results.append(list(item))

        cursor.close()

        return results

else:

    raise Exception("Error: este modulo solo esta disponible en plataformas java")