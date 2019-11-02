from flask import Markup, request, render_template
from Ban_Tivi import app
from Ban_Tivi.Xu_ly.Khach_tham_quan.Xu_ly_3L import *

@app.route("/", methods=['GET','POST'])
def index():
    danh_sach_tivi = Doc_Danh_sach_Tivi()

    danh_sach_tivi_xem = danh_sach_tivi

    if request.form.get("Th_Chuoi_Tra_cuu") != None:
        chuoi_tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")
        danh_sach_tivi_xem = Tra_cuu_Tivi(chuoi_tra_cuu, danh_sach_tivi)

    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(danh_sach_tivi_xem)

    return  render_template('Khach_tham_quan/MH_Chinh.html', 
            Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)
 
