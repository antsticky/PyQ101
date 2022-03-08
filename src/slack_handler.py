import json
import sys
import requests


class SlackHandler:
    def __init__(self):
        self.url = "<webhook_url>"

    def create_msg(self, direction, price):
        title = ("Upwards breach :point_up:") if direction == "up" else ("Downwards breach :point_down:")
        message = (f"Index price {price}")
        icon = ":chart_with_upwards_trend:" if direction == "up" else ":chart_with_downwards_trend:"
        color = "#32EE5E" if direction == "up" else "#EE3232"

        slack_data = {
            "username": "Python App",
            "icon_emoji": icon,
            "attachments": [
                {
                    "color": color,  # "#9733EE"
                    "fields": [
                        {
                            "title": title,
                            "value": message,
                            "short": "false",
                        }
                    ]
                }
            ]
        }

        return slack_data

    def send(self, direction, price):
        msg = self.create_msg(direction, price)
        byte_length = str(sys.getsizeof(msg))
        headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
        response = requests.post(self.url, data=json.dumps(msg), headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
