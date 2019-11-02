from flask import Flask

# app = Flask(__name__, static_folder="", template_folder="")
app = Flask(__name__)
app.secret_key = "2019"

import Ban_Tivi.app_khach_tham_quan