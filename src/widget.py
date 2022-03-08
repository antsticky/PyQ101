import time

import pyqtgraph as pg
from PyQt5.QtWidgets import *

import yfinance as yf

from config import PERIOD, INTERVAL, MY_PORTFOLIO
from src.widget_elements import INPUT_FIELD_NAME, INPUT_BTN_NAME, LABEL_BUY_PRICE, LABEL_NOTIONAL, LABEL_CUR_VALUE, LABEL_BUY_VALUE, LABEL_CUR_PRICE, LABEL_PNL, LABEL_PNL_PERCENT


class Window(QMainWindow):
    def __init__(self, x_poz=500, y_poz=300, width=1000, height=500, window_title=f"Finance (Investments) - Period {PERIOD}"):
        super().__init__()

        self.is_open = True
        self.setWindowTitle(window_title)
        self.setGeometry(x_poz, y_poz, width, height)

        self.grid, self.widget = Window.create_layout()

        self.qlabels = None
        self.ledits = None
        self.buttons = None
        self.plot = None

        self.create_ui_components()
        self.show()

    @staticmethod
    def modify_dict(input_dict, key, value):
        ret_dict = input_dict
        if ret_dict is None:
            ret_dict = {key: value}
        else:
            ret_dict[key] = value
        return ret_dict

    @staticmethod
    def create_layout():
        layout = QGridLayout()
        widget = QWidget()
        widget.setLayout(layout)
        return layout, widget

    def plot_component(self):
        plot = pg.PlotWidget()
        plot.setObjectName("MyPlotGraph")
        return plot

    def get_ledit_value(self, name):
        checkbox = self.ledits.get(name)
        # return checkbox.text()
        return checkbox.currentText()

    def get_market_data(self, ticker, period=PERIOD, interval=INTERVAL):
        msft = yf.Ticker(ticker)
        return msft.history(period=period, interval=interval)

    def create_plot(self, ticker, title="", bottom="", left="", right=""):
        self.plot.clear()

        market_data = self.get_market_data(ticker=ticker)
        market_data.reset_index()

        market_data.reset_index()
        y = list(market_data["Close"])
        y1 = list(market_data["High"])
        y2 = list(market_data["Low"])

        x = [int(time.mktime(x.timetuple())) for x in list(market_data.index)]

        self.plot.setLabels(
            bottom=bottom,
            left=left,
            title=title,
            right=right
        )

        self.plot.plot(x, y, pen=pg.mkPen('b', width=3))
        self.plot.plot(x, y1, pen=pg.mkPen('r', width=1))
        self.plot.plot(x, y2, pen=pg.mkPen('g', width=1))

        return market_data.iloc[-1]

    def btn_action(self):
        # checkbox = self.findChild(QLineEdit, "MyEditLine")
        idx_name = self.get_ledit_value(name=INPUT_FIELD_NAME)

        buy_value = MY_PORTFOLIO.get(idx_name, {}).get("value", 0)
        buy_notional = MY_PORTFOLIO.get(idx_name, {}).get("notional", 0)

        try:
            last_date = self.create_plot(ticker=idx_name, title=idx_name, bottom="Time", left="Value")
            cur_value = int(last_date.Close)
        except Exception:
            cur_value = 0

        self.qlabels[LABEL_BUY_PRICE].setText(f'Price (buy): {buy_value:n}')
        self.qlabels[LABEL_CUR_PRICE].setText(f'Price (current): {cur_value:n}')

        self.qlabels[LABEL_NOTIONAL].setText(f'Notional: {buy_notional}')

        self.qlabels[LABEL_BUY_VALUE].setText(f'Value (buy): {buy_value*buy_notional:n}')
        self.qlabels[LABEL_CUR_VALUE].setText(f'Value (current): {cur_value*buy_notional:n}')

        pnl_value = cur_value*buy_notional-buy_value*buy_notional
        try:
            pnl_percent = round(100*(cur_value-buy_value)/buy_value, 2)
        except ZeroDivisionError:
            pnl_percent = 0
        self.qlabels[LABEL_PNL].setText(f'PnL: {pnl_value:n}')
        self.qlabels[LABEL_PNL_PERCENT].setText(f'PnL: {pnl_percent:n}%')

        return cur_value

    def closeEvent(self, _):
        self.is_open = False

    def create_ui_components(self):
        # self.ledits = Window.modify_dict(self.ledits, INPUT_FIELD_NAME, QLineEdit("<Index ID>"))
        self.ledits = Window.modify_dict(self.ledits, INPUT_FIELD_NAME, QComboBox())
        self.ledits.get(INPUT_FIELD_NAME).addItems(["OTP.BD", "HUFEUR=X"])
        self.buttons = Window.modify_dict(self.buttons, INPUT_BTN_NAME, QPushButton('Fetch market data'))
        self.buttons.get(INPUT_BTN_NAME).clicked.connect(self.btn_action)
        self.qlabels = Window.modify_dict(self.qlabels, LABEL_BUY_PRICE, QLabel('Price (buy): -'))
        self.qlabels = Window.modify_dict(self.qlabels, LABEL_NOTIONAL, QLabel('Notional: -'))
        self.qlabels = Window.modify_dict(self.qlabels, LABEL_BUY_VALUE, QLabel('Value (buy): -'))
        self.qlabels = Window.modify_dict(self.qlabels, LABEL_CUR_PRICE, QLabel('Price (current): -'))
        self.qlabels = Window.modify_dict(self.qlabels, LABEL_CUR_VALUE, QLabel('Value (current): -'))
        self.qlabels = Window.modify_dict(self.qlabels, LABEL_PNL, QLabel('PnL: -'))
        self.qlabels = Window.modify_dict(self.qlabels, LABEL_PNL_PERCENT, QLabel('PnL: -%'))
        self.plot = self.plot_component()

        self.grid.addWidget(self.ledits.get(INPUT_FIELD_NAME), 0, 0)
        self.grid.addWidget(self.buttons.get(INPUT_BTN_NAME), 1, 0)

        self.grid.addWidget(self.qlabels.get(LABEL_BUY_PRICE), 2, 0)
        self.grid.addWidget(self.qlabels.get(LABEL_CUR_PRICE), 3, 0)

        self.grid.addWidget(self.qlabels.get(LABEL_NOTIONAL), 4, 0)

        self.grid.addWidget(self.qlabels.get(LABEL_BUY_VALUE), 5, 0)
        self.grid.addWidget(self.qlabels.get(LABEL_CUR_VALUE), 6, 0)
        self.grid.addWidget(self.qlabels.get(LABEL_PNL), 7, 0)
        self.grid.addWidget(self.qlabels.get(LABEL_PNL_PERCENT), 8, 0)
        self.grid.addWidget(self.plot, 0, 1, 40, 1)

        self.setCentralWidget(self.widget)
