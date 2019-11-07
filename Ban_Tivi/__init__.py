from flask import Flask

# app = Flask(__name__, static_folder="", template_folder="")
app = Flask(__name__)
app.secret_key = "2019"

import Ban_Tivi.app_khach_tham_quan
import Ban_Tivi.app_nhan_vien_nhap_hang
import Ban_Tivi.app_nhan_vien_ban_hang
import Ban_Tivi.app_quan_ly_nhap_hang