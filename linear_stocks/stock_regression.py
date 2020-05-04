import pandas as pd
import numpy as np
import pickle
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import datetime
import matplotlib.pyplot as plt
from random import randint, uniform
class StockReg:
    def __init__(self, csv=r"C:\Users\KamilB\Downloads\GOOGL.csv", pickle_file=""):
        self.df_data = pd.read_csv(csv)
        df =  np.array([self.df_data['Date']])
        # describe time as integer
        self.df_data['Date_time'] = pd.to_datetime(self.df_data['Date'])
        self.df_data['Date_delta'] = (self.df_data['Date_time'] - self.df_data['Date_time'].min()) / np.timedelta64(1, 'D')
        self.df_data.drop(['Volume'], axis=1, inplace=True)
        self.df_data.set_index('Date', inplace=True)
        self.df_data.dropna(inplace=True)
        self.delta = 0
        self.count = 0
    def learn(self, start=0, stop=10, b=False):
        if b:
            x = np.array(self.df_data['Date_delta'][start:stop])
            y = np.array(self.df_data['Close'][start:stop])
        else:
            x = np.array(self.df_data['Date_delta'])
            y = np.array(self.df_data['Close'])
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
        X_train = np.reshape(X_train, (-1, 1))
        X_test = np.reshape(X_test, (-1, 1))
        self.clf = LinearRegression(n_jobs=-1)
        self.clf.fit(X_train, y_train)
        self.accuracy = self.clf.score(X_test, y_test)
        i = 0
        self.hesitation = 0.0
        for date in self.df_data['Date_delta']:
            date = np.reshape(date, (-1, 1))
            self.hesitation += abs(self.df_data['Close'][i]-self.clf.predict(date))/self.df_data['Close'][i]
            i+=1

        self.hesitation /= i

    def save(self, file_name="regression.pickle"):
       with open(file_name, 'wb') as f:
           pickle.dump(self.clf, f)
    def predict(self, year=2019, month=11, day=15):
        date = datetime.datetime(year, month, day)
        date = (date-self.df_data['Date_time'].min())/np.timedelta64(1, 'D')
        date = np.reshape(date, (-1, 1))
        return self.clf.predict(date)[0]
    def predict_period(self,  year_stop=2020, month_stop=12, day_stop=20, time_spand=8):
        date_start = self.df_data['Date_time'][-1]
        date_stop = datetime.datetime(year_stop, month_stop, day_stop)
        day = datetime.timedelta(days=1)
        time_spand = int(len(self.df_data)/time_spand)
        predictions = np.array([], dtype=np.uint64)
        k = 0
        j = 0
        self.learn(time_spand * k, time_spand * (k + 1), True)
        for date in self.df_data['Date_delta']:
            if j == time_spand:
                k += 1
                if time_spand*k<=(len(self.df_data)-time_spand):
                    self.learn(time_spand * k, time_spand * (k + 1), True)

                j = 0
            date = np.reshape(date, (-1, 1))
            pred = self.clf.predict(date)[0]
            predictions = np.append(predictions, pred)
            j+=1
        self.df_data['Trend'] = predictions

        self.learn()
        i = 0
        for date in self.df_data['Date_delta']:
            date = np.reshape(date, (-1, 1))
            predictions[i] = self.clf.predict(date)[0]
            i+=1
        period = np.array([], dtype=np.datetime64)
        self.df_data['Forecast'] = predictions
        while date_start <= date_stop:
            period = np.append(period, date_start)
            date = (date_start-self.df_data['Date_time'].min())/np.timedelta64(1, 'D')
            date = np.reshape(date, (-1, 1))
            pred = self.clf.predict(date)[0]
            hesitation = 1- self.accuracy
            diff = uniform(0, self.hesitation*pred)
            self.df_data.loc[date_start]= [np.nan for i in range(len(self.df_data.columns)-1)] + [pred]
            date_start += day
        period_delta = np.array(
            [(period[i] - self.df_data['Date_time'].min()) / np.timedelta64(1, 'D') for i in range(len(period))],
            dtype=np.float64)
        period_delta = np.reshape(period_delta, (-1, 1))
        return period
    def show_graph(self):
        self.df_data['Forecast'] = self.df_data['Forecast'].astype(float)
        self.df_data['Trend'] = self.df_data['Trend'].astype(float)
        self.df_data['Forecast'].plot()
        self.df_data['Close'].plot()
        self.df_data['Trend'].plot()
        plt.legend(loc=4)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()
if __name__ == '__main__':
    Sg = StockReg()
    Sg.predict_period(month_stop=4, day_stop=25, year_stop=2020)
    Sg.show_graph()
