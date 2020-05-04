from tkinter import *
from tkcalendar import Calendar
from datetime import date
from get_csv import StockCSV
from stock_regression import StockReg
class MainGui():
    def __init__(self, master):
        self.master = master
        master.title("Linear YahooStocks")
        master.geometry("{}x{}".format(300, 300))
        self.link = Entry()
        self.link_text = Label(text="Entry link: ")
        self.cal_but = Button(text="choose date", command=self.date_select)
        self.cal_lab = Label()
        self.start_but = Button(text="start", command=self.start_regression)
        self.link.grid(row=0, column=1)
        self.link_text.grid(row=0, column=0)
        self.cal_but.grid(row=1, column=0)
        self.cal_lab.grid(row=1, column=1)
        self.start_but.grid(row=2, columnspan=2)
        self.date2 = date.today()
        f = open("config.txt", "r")
        lines = f.readlines()
        self.driver_path = str(lines[0])
        self.download_path = str(lines[1])
        f.close()
    def calendar(self, root):
        self.top = Toplevel(root)
        self.date = date.today()
        self.cal = Calendar(self.top, font="Arial 14", selectmode="day", cursor="hand1", year=self.date.year,
                            month=self.date.month, day=self.date.day)
        self.cal.pack(fill="both", expand=True)
        Button(self.top, text="select", command=self.print_sel).pack()
        self.top.grab_set()
    def print_sel(self):
        self.date2 = self.cal.selection_get()
        self.cal_lab.configure(text=str(self.date2))
        self.top.destroy()
    def date_select(self):
        self.calendar(self.master)
    def start_regression(self):

        link =self.link.get()
        S = StockCSV(driver=self.driver_path)
        S.download_stock_diagram(url=link)
        folder = S.get_stock_diagram(dir=self.download_path)
        Sr = StockReg(csv=folder)
        Sr.predict_period(self.date2.year, self.date2.month, self.date2.day)
        Sr.show_graph()
if __name__ == '__main__':
    root = Tk()
    M = MainGui(root)

    root.mainloop()