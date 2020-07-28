from undetected_chromedriver import Chrome, ChromeOptions
from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app, title="WS Crawler API")

options = ChromeOptions()
options.headless = True
options.add_argument("--headless")
options.add_argument("--no-sandbox")
browser = Chrome(options=options)

import ws.controller
