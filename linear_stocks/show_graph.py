import matplotlib.pyplot as plt
from matplotlib import style
from stock_regression import StockReg
import pandas as pd

#just some test code for myself
def show_graph(data_y, data_x):

    data = pd.DataFrame({"Price": data_y}, index=data_x)
    data.plot()

    plt.legend(loc=4)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()




if __name__ == '__main__':
    S = StockReg()
    S.learn()
    x, y = S.predict_period()
    show_graph(x, y)