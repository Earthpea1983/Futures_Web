import sqlite3
import pandas as pd


class ThirtyThree:
    def __init__(self):
        day = 33 # to get the 33day for calculation
        #sql start
        prodConn = sqlite3.connect("D:\MyRepository\Futures\Commodity.db")  # server name and location.
        prodC = prodConn.cursor()
        #----------------------------------------------------------------------------------------------------------
        spot = self.get_spot(prodConn)
        res = self.judge_spot(spot, day)  # -1 for going down, 1 for up, 0 for ignore
        res = pd.DataFrame.from_dict(res, orient='index')
        res = res[res.iloc[:, 0] != 0]
        self.storage_to_excel(res)
        #-----------------------------------------------------------------------------------------------------------
        #sql stop
        prodConn.close() # not modified the db, so no commit
        print("Suggestion has been made!")


    def get_spot(self, prodConn):
        sql = "SELECT * FROM spot"
        spot = pd.read_sql(sql, prodConn)
        return spot

    def judge_spot(self, spot, day):
        spot = spot.tail(day)  # 33 days dataframe since today
        columns = [column for column in spot][1::]  # name of column in df, excluding "日期"
        res = {}
        for colName in columns:  # loop for each spot
            singleSpot = spot.loc[:, colName]
            dayMinus = list(singleSpot.iloc[0:day-1]) #0 to 32 days (day -1)
            dayMinusMin = min(dayMinus)   # minimum in 32 days
            dayMinusMax = max(dayMinus)   # maximum in 32 days
            # if spot 0:32 minimum is No.32, and 33 more than 32 then the lowest and return 1
            if singleSpot.iloc[day-2] <= dayMinusMin and singleSpot.iloc[day-1] > singleSpot.iloc[day-2]:
                #percent of increasing of spot
                res[colName] = (singleSpot.iloc[day-1]-singleSpot.iloc[day-2])/singleSpot.iloc[day-2]*100
            # if spot 0:32 maximum is No.32, and 33 less than 32 then the highest and return -1
            elif singleSpot.iloc[day-2] >= dayMinusMax and singleSpot.iloc[day-1] < singleSpot.iloc[day-2]:
                # percent of increasing of spot
                res[colName] = (singleSpot.iloc[day-1]-singleSpot.iloc[day-2])/singleSpot.iloc[day-2]*100
            else:
                res[colName] = 0
        return res

    def storage_to_excel(self,res):
        res.to_excel(r"C:\Users\Mike\Documents\Com_Ex\spot.xlsx")


if __name__ == '__main__':
    a = ThirtyThree()