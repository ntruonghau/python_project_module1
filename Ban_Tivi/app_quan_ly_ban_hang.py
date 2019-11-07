from flask import Markup, request, render_template, session, redirect
from Ban_Tivi import app
from Ban_Tivi.Xu_ly.Quan_ly_Ban_hang.Xu_ly_3L import *
from datetime import datetime

@app.route("/qlbh/dang-nhap", methods=['GET','POST'])
def QLBH_Dang_nhap():
    if session.get("session_QLBH"):
        return redirect(url_for("QLBH"))
    Ten_dang_nhap = ""
    Mat_khau = ""
    Thong_bao = ""
    
    if request.form.get("Th_Ten_dang_nhap"):
        Ten_dang_nhap = request.form.get("Th_Ten_dang_nhap")
        Mat_khau = request.form.get("Th_Mat_khau")

        Cong_ty = Doc_Cong_ty()
        Nhan_vien = Dang_nhap_Nhan_vien(Cong_ty["Danh_sach_Quan_ly_Ban_hang"], Ten_dang_nhap, Mat_khau)
        print(Nhan_vien)
        Hop_le = (Nhan_vien != None)
        if Hop_le:
            session["session_QLBH"] = Nhan_vien
            return redirect(url_for("QLBH"))
        else:
            Thong_bao = "Đăng nhập không hợp lệ."
    return render_template("Quan_ly_Ban_hang/MH_Dang_nhap.html", Chuoi_Thong_bao=Thong_bao, Ten_dang_nhap=Ten_dang_nhap, Mat_khau=Mat_khau)

@app.route("/qlbh", methods=['GET','POST'])
def QLBH():
    if session.get("session_QLBH") == None:
        return redirect(url_for("QLBH_Dang_nhap"))

    Nhan_vien_Dang_nhap = session["session_QLBH"]
    Chuoi_HTML_Nhan_Vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)

    # Xử lý màn hình
    Dia_chi_Man_hinh = "/qlbh/danh-sach-tivi"
    
    if request.method == "POST":
        Ma_so = request.form.get("Th_Ma_so")
        if Ma_so == "DANH_SACH":
            Dia_chi_Man_hinh = "/qlbh/danh-sach-tivi"
        elif Ma_so == "SO_LUONG_TON":
            Dia_chi_Man_hinh = "/qlbh/so-luong-ton"
        elif Ma_so == "DOANH_THU_TIVI":
            Dia_chi_Man_hinh = "/qlbh/danh-sach-phieu-thu"
        elif Ma_so == "DOANH_THU_NHAN_VIEN":
            Dia_chi_Man_hinh = "/qlbh/doanh-thu-nhan-vien"
        elif Ma_so == "TIM_KIEM":
            Chuoi_tim_kiem = request.form.get("Th_Chuoi_Tra_cuu")
            Dia_chi_Man_hinh = "/qlbh/tim-kiem/" + Chuoi_tim_kiem 
        

    return render_template("Quan_ly_Ban_hang/MH_Chinh.html", Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_Vien, Dia_chi_MH=Dia_chi_Man_hinh)

@app.route("/qlbh/dang-xuat", methods=['GET', 'POST'])
def QLBH_Dang_xuat():
    session.pop("session_QLBH", None)
    return redirect(url_for("QLBH_Dang_nhap"))

@app.route("/qlbh/danh-sach-tivi", methods=['GET','POST'])
def QLBH_Xem_DS_Tivi():
    if session.get("session_QLBH") == None:
        return redirect(url_for("QLBH_Dang_nhap"))
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    danh_sach_Tivi_Xem = Danh_sach_Tivi
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(danh_sach_Tivi_Xem)
    return render_template("Quan_ly_Ban_hang/MH_Xem_Danh_sach_Tivi.html", Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)


@app.route("/qlbh/so-luong-ton")
def QLBH_Danh_sach_Phieu_nhap():
    if session.get("session_QLBH") == None:
        return redirect(url_for("QLBH_Dang_nhap"))
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Chuoi_HTML_Thong_ke_Tivi = Tao_Chuoi_HTML_So_luong_Ton(Danh_sach_Tivi)
    return render_template("Quan_ly_Ban_hang/MH_Xem_SL_Ton.html", Chuoi_HTML_Thong_ke_Tivi=Chuoi_HTML_Thong_ke_Tivi)

@app.route("/qlbh/danh-sach-phieu-thu")
def QLBH_Danh_sach_Phieu_thu():
    if session.get("session_QLBH") == None:
        return redirect(url_for("QLBH_Dang_nhap"))
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Ngay = datetime.now().strftime("%d-%m-%Y")
    Danh_sach_Tivi_ban = Danh_sach_Tivi_Da_ban_Theo_ngay(Danh_sach_Tivi, Ngay)
    Danh_sach_Thong_ke = Tong_ket_Danh_sach_Tivi(Danh_sach_Tivi_ban, Ngay)
    Chuoi_HTML_Thong_ke_Tivi = Tao_Chuoi_HTML_Thong_ke_Tivi(Danh_sach_Thong_ke)
    return render_template("Quan_ly_Ban_hang/MH_Xem_Doanh_thu_Tivi.html", Chuoi_HTML_Thong_ke_Tivi=Chuoi_HTML_Thong_ke_Tivi)

@app.route("/qlbh/doanh-thu-nhan-vien")
def QLBH_Doanh_thu_Nhan_vien():
    if session.get("session_QLBH") == None:
        return redirect(url_for("QLBH_Dang_nhap"))
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Ngay = datetime.now().strftime("%d-%m-%Y")
    Danh_sach_Tivi_ban = Danh_sach_Tivi_Da_ban_Theo_ngay(Danh_sach_Tivi, Ngay)
    Chuoi_HTML_Thong_ke_Nhan_vien = Tao_Chuoi_HTML_Doanh_thu_Nhan_vien(Danh_sach_Tivi_ban)
    return render_template("Quan_ly_Ban_hang/MH_Xem_Doanh_thu_Nhan_vien.html", Chuoi_HTML_Thong_ke_Nhan_vien=Chuoi_HTML_Thong_ke_Nhan_vien)

@app.route("/qlbh/tim-kiem/<string:Chuoi_tim_kiem>")
def QLBH_Tim_kiem(Chuoi_tim_kiem):
    if session.get("session_QLBH") == None:
        return redirect(url_for("QLBH_Dang_nhap"))
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    danh_sach_Tivi_Xem = Tra_cuu_Tivi(Chuoi_tim_kiem, Danh_sach_Tivi)
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(danh_sach_Tivi_Xem)
    return render_template("Quan_ly_Ban_hang/MH_Xem_Danh_sach_Tivi.html", Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)

@app.route("/qlbh/cap-nhat/<string:Ma_so>/", methods=['GET','POST'])
def QLBH_Cap_nhat_Tivi(Ma_so):
    if session.get("session_QLBH") == None:
        return redirect(url_for("QLBH_Dang_nhap"))

    Nhan_vien_Dang_nhap = session["session_QLBH"]
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Tivi_Chon = Lay_chi_tiet_Tivi(Danh_sach_Tivi, Ma_so)

    if Tivi_Chon != None:
        Thong_bao = ""
        if request.method == "POST":
            Tivi_Chon["Don_gia_Ban"] = int(request.form.get("Th_So_luong"))
            Thong_bao =  "Vừa cập nhật " + str(Tivi_Chon["Don_gia_Ban"]) + " " + Tivi_Chon["Ten"] + " Thành công<br>"
            Ghi_Tivi(Tivi_Chon)
    Chuoi_HTML_Tivi = Tao_Chuoi_HTML_Tivi(Tivi_Chon, Thong_bao, Tivi_Chon["Don_gia_Ban"])
    return render_template("Quan_ly_Ban_hang/MH_Cap_nhap_Tivi.html", Chuoi_HTML_Tivi=Chuoi_HTML_Tivi)