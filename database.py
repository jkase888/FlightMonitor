import psycopg2
import os
import traceback

class DatabaseGateway():

    def __init__(self, env):
            self.DATABASE_URL = os.environ['DATABASE_URL']

    def connect(self):
        self.connection = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        self.cursor = self.connection.cursor()
        self.isClosed = False

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
        self.isClosed = True

    def fetchall(self):
        return self.cursor.fetchall()

    def getCursor(self):
        return self.cursor

    def insertAirlinePrice(self, from_code, return_code, date_depature, date_return, total_price, logged_at_datetime):
        try:
            if (self.isClosed is True):
                self.connect()
            self.cursor.execute("INSERT INTO airfare_prices (origination_fnum, return_fnum, date_depature, date_return, total_price, logged_at_datetime) VALUES (%s, %s, %s, %s, %s, %s)", (from_code, return_code, date_depature, date_return, total_price, logged_at_datetime))
            self.commit()
            return 0
        except Exception as e:
            #print(e.pgcode + "\n" + e.pgerror)
            print(traceback.format_exc())
            self.close()
            return -1

    def executeSQL(self, statement):
        try:
            if(self.isClosed is True):
                self.connect()
            self.cursor.execute(statement)
            self.commit()
            return 0
        except Exception as e:
            print(traceback.format_exc())
            self.close()
            return -1
