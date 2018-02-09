import sqlite3
import pandas as pd

class Spot:
    def __init__(self):
        # server start
        #sf database
        sfConn = sqlite3.connect("D:\MyRepository\Futures\Sfdata.db")  # server name and location.
        sfC = sfConn.cursor()
        #Commodity database
        prodConn = sqlite3.connect("D:\MyRepository\Futures\Commodity.db")  # server name and location.
        prodC = prodConn.cursor()
        prodTbName = 'spot'
        #------------------------------------------------------------------------------------------
        sfTbList = self.table_list(sfC)  # table name list from sf database
        tbName = sfTbList[-1] # last table of sf
        spotList = self.get_spot_name(sfC, tbName)
        self.create_spot_tb(prodC, prodTbName, spotList, sfTbList)  # create the commodity db
        self.insert_commodity(sfC, prodC, prodTbName, spotList, sfTbList)
        self.storage_spot_to_excel(prodTbName, prodConn)  #read spot db and to excel
        #------------------------------------------------------------------------------------------
        #close server
        sfConn.commit()
        sfConn.close()
        prodConn.commit()
        prodConn.close()
        print("Spot table created!")

    #return table name string in list
    def table_list(self, sfc):
        tbList = sfc.execute("SELECT name FROM sqlite_master WHERE type='table'order by name;").fetchall()
        for i in range(len(tbList)):
            tbList[i] = tbList[i][0]
        return tbList

    def create_spot_tb(self, prodC, prodTbName, spotList, sfTbList):
        tbName = prodTbName # name of the table with all commodity.
        #check if table existed than delete the table
        if self.check_table(prodC, tbName):
            sqlDrop = "DROP TABLE {0};".format(tbName)
            prodC.execute(sqlDrop)
        # create an empty table only with id and date in string
        sqlCreate = "CREATE TABLE {0} ('日期' text primary key);".format(tbName)
        prodC.execute(sqlCreate)
        # use loop to add all spot into the table as field
        for s in spotList:
            sqlAddSpot = "ALTER table {0} add '{1}' real;".format(tbName, s)
            prodC.execute(sqlAddSpot)
        # insert the dateTime to the spot table as index, later for updating the table data with sql update wording
        for sf in sfTbList:
            # get table date time as string, in order to store into the spot list as index
            dateTime = sf.replace("sf", "")
            sqlDate = "INSERT INTO {0} ('日期') VALUES ({1});".format(tbName, dateTime)
            prodC.execute(sqlDate)

    def get_spot_name(self, sfc, tbName):
        #read the lastest database and return the name list of spot
        sql = "SELECT 商品 from {0};".format(tbName)
        spotList = sfc.execute(sql).fetchall()
        for i in range(len(spotList)):
            spotList[i] = spotList[i][0]
        return spotList

    #check table existed
    def check_table(self, prodC, tbName):
        sqlCheck = "SELECT COUNT(*) from sqlite_master WHERE type= 'table' and name = '{0}';".format(tbName)
        prodC.execute(sqlCheck)
        #if table existed, than true.
        res = prodC.fetchone()
        if res == (1,):
            return True
        else:
            return False

    def insert_commodity(self, sfC, prodC, prodTbName, spotList, sfTbList):
        # loop for all sf tables
        for sf in sfTbList:
            # get table date time as string, in order to store into the spot list
            dateTime = sf.replace("sf", "")
            # loop for all spot in one table
            for sp in spotList:
                # get spot price from sf table
                # select 现货价格 from table sf in upper loop where 商品 = sp in lower loop
                sqlGet = "SELECT 现货价格 FROM {0} WHERE 商品  = '{1}'".format(sf, sp)
                spotPrice = sfC.execute(sqlGet).fetchall()
                spotPrice = spotPrice[0][0]
                # insert price to spot table
                # inser into table spot (商品名称) values (商品价格) by update
                sqlInsert = "UPDATE {0} SET '{1}' = {2} WHERE 日期 = '{3}';".format(prodTbName, sp, spotPrice, dateTime)
                prodC.execute(sqlInsert)

    def storage_spot_to_excel(self, prodTbName, prodConn):
        sqlReadSpot = "SELECT * FROM spot"
        dfContent = pd.read_sql(sqlReadSpot, prodConn)
        dfContent.to_excel(r"C:\Users\Mike\Documents\Com_Ex\SpotData.xlsx")

if __name__ == '__main__':
    a = Spot()
