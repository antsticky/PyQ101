
import sys
import time
from datetime import datetime

from PyQt5.QtWidgets import *

from src.widget import Window
from src.slack_handler import SlackHandler
from src.widget_elements import INPUT_FIELD_NAME


class FinanceApplication:
    def __init__(self, is_looping=False, is_alerting=False, upward_limit=None, downward_limit=None):
        self.is_looping = is_looping
        self.is_alerting = is_alerting

        if is_alerting and (None in [upward_limit, downward_limit]):
            raise ValueError("Limits cannot be none if alerting is enabled")

        self.upward_limit = upward_limit
        self.downward_limit = downward_limit

    @classmethod
    def base_window(cls):
        return cls()

    @classmethod
    def monitoring(cls, upward_limit, downward_limit):
        return cls(is_looping=True, is_alerting=True, upward_limit=upward_limit, downward_limit=downward_limit)

    def send_alers(self, cur_value, slack_bot):
        if cur_value > self.upward_limit:
            slack_bot.send(direction="up", price=cur_value)
        elif cur_value < self.downward_limit:
            slack_bot.send(direction="down", price=cur_value)

    @staticmethod
    def value_logging(index, cur_value):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"[{current_time}] {index} = {cur_value}")

    def unpack_market_info(self, window):
        cur_value = window.btn_action()
        index = window.get_ledit_value(INPUT_FIELD_NAME)

        FinanceApplication.value_logging(index=index, cur_value=cur_value)

        return cur_value

    def market_monitoring(self, window):
        counter = 0
        slack_bot = SlackHandler()
        while window.is_open:
            try:
                QApplication.processEvents()

                cur_value = self.unpack_market_info(window=window)
                if self.is_alerting:
                    self.send_alers(cur_value, slack_bot)

                time.sleep(1)
                counter += 1

            except KeyboardInterrupt:
                break

        window.close()

    def run(self):
        App = QApplication(sys.argv)
        window = Window()

        if self.is_looping:
            self.market_monitoring(window=window)
        else:
            sys.exit(App.exec_())
