import pymysql
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

class MySQL:

    def __init__(self, IP_DNS, USER, PASSWORD, BD_NAME, PORT):
        self.IP_DNS = IP_DNS
        self.USER = USER
        self.PASSWORD = PASSWORD
        self.BD_NAME = BD_NAME
        self.PORT = PORT
        self.SQL_ALCHEMY = 'mysql+pymysql://' + self.USER + ':' + self.PASSWORD + '@' + self.IP_DNS + ':' + str(self.PORT) + '/' + self.BD_NAME


    def create_engine(self):
        engine = create_engine(self.SQL_ALCHEMY, poolclass=NullPool)
        conn = engine.connect()
        print("Connected to MySQL server [" + self.BD_NAME + "]")
        return conn, engine


    def execute_engine(self, conn, sql, args=None):
        result = 0
        if args:
            try:
                result = conn.execute(sql, args).fetchall()
                print("Executed \n\n" + str(sql) + "\n\n successfully")
            except Exception as error:
                print(error)
        else:
            try:
                result = conn.execute(sql).fetchall()
                print("Executed \n\n" + str(sql) + "\n\n successfully")
            except Exception as error:
                print(error)
        return result


    def close_engine(self, conn, engine):
        conn.close()
        engine.dispose()
        print("Close connection with MySQL server [" + self.BD_NAME + "]")



    def connect(self):
        # Open database connection
        self.db = pymysql.connect(host=self.IP_DNS,
                                user=self.USER, 
                                password=self.PASSWORD, 
                                database=self.BD_NAME, 
                                port=self.PORT)
        # prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()
        print("Connected to MySQL server [" + self.BD_NAME + "]")
        return self.db



    def close(self):
        # disconnect from server
        self.db.close()
        print("Close connection with MySQL server [" + self.BD_NAME + "]")



    def execute_interactive_sql(self, sql, delete=False):
        result = 0
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.db.commit()
            print("Executed \n\n" + str(sql) + "\n\n successfully")
            result = 1
        except Exception as error:
            print(error)
            # Rollback in case there is any error
            self.db.rollback()
        return result



    def execute_get_sql(self, sql):
        """SELECT"""
        results = None
        print("Executing:\n", sql)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = self.cursor.fetchall()
        except Exception as error:
            print(error)
            print ("Error: unable to fetch data")
        
        return results



    def generate_insert_into_people_sql(self, to_insert):
        """
        This must be modified according to the table structure
        """
        nombre = to_insert[0]
        apellidos = to_insert[1]
        direccion = to_insert[2]
        edad = to_insert[3]
        nota = to_insert[4]
        
        sql = """INSERT INTO people
            (MOMENTO, NOMBRE, APELLIDOS, DIRECCION, EDAD, NOTA)
            VALUES
            (NOW(), '""" + nombre + """', '""" + apellidos + """', '""" + direccion + """', '""" + edad + """', '""" + nota + """')"""

        sql = sql.replace("\n", "").replace("            ", " ")
        return sql