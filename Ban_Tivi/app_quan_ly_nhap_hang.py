from flask import Markup, request, render_template, session, redirect
from Ban_Tivi import app
from Ban_Tivi.Xu_ly.Quan_ly_Nhap_hang.Xu_ly_3L import *
from datetime import datetime

@app.route("/qlnh/dang-nhap", methods=['GET','POST'])
def QLNH_Dang_nhap():
    if session.get("session_QLNH"):
        return redirect(url_for("QLNH"))
    Ten_dang_nhap = ""
    Mat_khau = ""
    Thong_bao = ""
    print('a')

    if request.form.get("Th_Ten_dang_nhap"):
        Ten_dang_nhap = request.form.get("Th_Ten_dang_nhap")
        Mat_khau = request.form.get("Th_Mat_khau")

        Cong_ty = Doc_Cong_ty()
        Nhan_vien = Dang_nhap_Nhan_vien(Cong_ty["Danh_sach_Quan_ly_Nhap_hang"], Ten_dang_nhap, Mat_khau)
        Hop_le = (Nhan_vien != None)
        if Hop_le:
            session["session_QLNH"] = Nhan_vien
            return redirect(url_for("QLNH"))
        else:
            Thong_bao = "Đăng nhập không hợp lệ."
        print('a')
    return render_template("Quan_ly_Nhap_hang/MH_Dang_nhap.html", Chuoi_Thong_bao=Thong_bao, Ten_dang_nhap=Ten_dang_nhap, Mat_khau=Mat_khau)

@app.route("/qlnh", methods=['GET','POST'])
def QLNH():
    if session.get("session_QLNH") == None:
        return redirect(url_for("QLNH_Dang_nhap"))

    Nhan_vien_Dang_nhap = session["session_QLNH"]
    Chuoi_HTML_Nhan_Vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)

    # Xử lý màn hình
    Dia_chi_Man_hinh = "/qlnh/danh-sach-tivi"
    
    if request.method == "POST":
        Ma_so = request.form.get("Th_Ma_so")
        if Ma_so == "DANH_SACH":
            Dia_chi_Man_hinh = "/qlnh/danh-sach-tivi"
        elif Ma_so == "SO_LUONG_TON":
            Dia_chi_Man_hinh = "/qlnh/so-luong-ton"
        elif Ma_so == "TIM_KIEM":
            Chuoi_tim_kiem = request.form.get("Th_Chuoi_Tra_cuu")
            Dia_chi_Man_hinh = "/qlnh/tim-kiem/" + Chuoi_tim_kiem 
        

    return render_template("Quan_ly_Nhap_hang/MH_Chinh.html", Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_Vien, Dia_chi_MH=Dia_chi_Man_hinh)

@app.route("/qlnh/dang-xuat", methods=['GET', 'POST'])
def QLNH_Dang_xuat():
    session.pop("session_QLNH", None)
    return redirect(url_for("QLNH_Dang_nhap"))

@app.route("/qlnh/danh-sach-tivi", methods=['GET','POST'])
def QLNH_Xem_DS_Tivi():
    if session.get("session_QLNH") == None:
        return redirect(url_for("QLNH_Dang_nhap"))
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    danh_sach_Tivi_Xem = Danh_sach_Tivi
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(danh_sach_Tivi_Xem)
    return render_template("Quan_ly_Nhap_hang/MH_Xem_Danh_sach_Tivi.html", Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)

@app.route("/qlnh/so-luong-ton")
def QLNH_Danh_sach_Phieu_nhap():
    if session.get("session_QLNH") == None:
        return redirect(url_for("QLNH_Dang_nhap"))
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Chuoi_HTML_Thong_ke_Tivi = Tao_Chuoi_HTML_So_luong_Ton(Danh_sach_Tivi)
    return render_template("Quan_ly_Nhap_hang/MH_Xem_SL_Ton.html", Chuoi_HTML_Thong_ke_Tivi=Chuoi_HTML_Thong_ke_Tivi)

@app.route("/qlnh/tim-kiem/<string:Chuoi_tim_kiem>")
def QLNH_Tim_kiem(Chuoi_tim_kiem):
    if session.get("session_QLNH") == None:
        return redirect(url_for("QLNH_Dang_nhap"))
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    danh_sach_Tivi_Xem = Tra_cuu_Tivi(Chuoi_tim_kiem, Danh_sach_Tivi)
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(danh_sach_Tivi_Xem)
    return render_template("Quan_ly_Nhap_hang/MH_Xem_Danh_sach_Tivi.html", Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)

@app.route("/qlnh/cap-nhat/<string:Ma_so>/", methods=['GET','POST'])
def QLNH_Cap_nhat_Tivi(Ma_so):
    if session.get("session_QLNH") == None:
        return redirect(url_for("QLNH_Dang_nhap"))

    Nhan_vien_Dang_nhap = session["session_QLNH"]
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Tivi_Chon = Lay_chi_tiet_Tivi(Danh_sach_Tivi, Ma_so)

    if Tivi_Chon != None:
        Thong_bao = ""
        if request.method == "POST":
            Tivi_Chon["Don_gia_Nhap"] = int(request.form.get("Th_So_luong"))
            Thong_bao =  "Vừa cập nhật " + Tivi_Chon["Don_gia_Nhap"] + " " + Tivi_Chon["Ten"] + " Thành công<br>"
            Ghi_Tivi(Tivi_Chon)
    Chuoi_HTML_Tivi = Tao_Chuoi_HTML_Tivi(Tivi_Chon, Thong_bao, Tivi_Chon["Don_gia_Nhap"])
    return render_template("Quan_ly_Nhap_hang/MH_Cap_nhap_Tivi.html", Chuoi_HTML_Tivi=Chuoi_HTML_Tivi)
