from flask import Markup, request, render_template, session, redirect
from Ban_Tivi import app
from Ban_Tivi.Xu_ly.Nhan_vien_Nhap_hang.Xu_ly_3L import *
from datetime import datetime

@app.route("/nvnh/dang-nhap", methods=['GET','POST'])
def NVNH_Dang_nhap():
    if session.get("session_NVNH"):
        return redirect(url_for("NVNH"))

    Ten_dang_nhap = ""
    Mat_khau = ""
    Thong_bao = ""

    if request.form.get("Th_Ten_dang_nhap"):
        Ten_dang_nhap = request.form.get("Th_Ten_dang_nhap")
        Mat_khau = request.form.get("Th_Mat_khau")

        Cong_ty = Doc_Cong_ty()
        Nhan_vien = Dang_nhap_Nhan_vien(Cong_ty["Danh_sach_Nhan_vien_Nhap_hang"], Ten_dang_nhap, Mat_khau)
        Hop_le = (Nhan_vien != None)
        if Hop_le:
            session["session_NVNH"] = Nhan_vien
            return redirect(url_for("NVNH"))
        else:
            Thong_bao = "Đăng nhập không hợp lệ."
    return render_template("Nhan_vien_Nhap_hang/MH_Dang_nhap.html", Chuoi_Thong_bao=Thong_bao, Ten_dang_nhap=Ten_dang_nhap, Mat_khau=Mat_khau)

@app.route("/nvnh", methods=['GET','POST'])
def NVNH():
    if session.get("session_NVNH") == None:
        return redirect(url_for("NVNH_Dang_nhap"))

    Nhan_vien_Dang_nhap = session["session_NVNH"]
    Chuoi_HTML_Nhan_Vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)

    # Xử lý màn hình
    Dia_chi_Man_hinh = "/nvnh/danh-sach-tivi"
    
    if request.method == "POST":
        Ma_so = request.form.get("Th_Ma_so")
        if Ma_so == "DANH_SACH":
            Dia_chi_Man_hinh = "/nvnh/danh-sach-tivi"
        elif Ma_so == "PHIEU_NHAP":
            Dia_chi_Man_hinh = "/nvnh/danh-sach-phieu-nhap"
        elif Ma_so == "TIM_KIEM":
            Chuoi_tim_kiem = request.form.get("Th_Chuoi_Tra_cuu")
            Dia_chi_Man_hinh = "/nvnh/tim-kiem/" + Chuoi_tim_kiem 
        

    return render_template("Nhan_vien_Nhap_hang/MH_Chinh.html", Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_Vien, Dia_chi_MH=Dia_chi_Man_hinh)

@app.route("/nvnh/dang-xuat", methods=['GET', 'POST'])
def NVNH_Dang_xuat():
    session.pop("session_NVNH", None)
    return redirect(url_for("NVNH_Dang_nhap"))

@app.route("/nvnh/danh-sach-tivi", methods=['GET','POST'])
def NVNH_Xem_DS_Tivi():
    if session.get("session_NVNH") == None:
        return redirect(url_for("NVNH_Dang_nhap"))
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    danh_sach_Tivi_Xem = Danh_sach_Tivi
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(danh_sach_Tivi_Xem)
    return render_template("Nhan_vien_nhap_hang/MH_Xem_Danh_sach_Tivi.html", Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)

@app.route("/nvnh/danh-sach-phieu-nhap")
def NVNH_Danh_sach_Phieu_nhap():
    if session.get("session_NVNH") == None:
        return redirect(url_for("NVNH_Dang_nhap"))
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Ngay = datetime.now().strftime("%d-%m-%Y")
    Danh_sach_Tivi_nhap = Danh_sach_Tivi_Nhap_Theo_ngay(Danh_sach_Tivi, Ngay)
    Danh_sach_Thong_ke = Tong_ket_Danh_sach_Tivi(Danh_sach_Tivi_nhap, Ngay)
    Chuoi_HTML_Thong_ke_Tivi = Tao_Chuoi_HTML_Thong_ke_Tivi(Danh_sach_Thong_ke)
    return render_template("Nhan_vien_nhap_hang/MH_Xem_Phieu_nhap.html", Chuoi_HTML_Thong_ke_Tivi=Chuoi_HTML_Thong_ke_Tivi)

@app.route("/nvnh/tim-kiem/<string:Chuoi_tim_kiem>")
def NVNH_Tim_kiem(Chuoi_tim_kiem):
    if session.get("session_NVNH") == None:
        return redirect(url_for("NVNH_Dang_nhap"))
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    danh_sach_Tivi_Xem = Tra_cuu_Tivi(Chuoi_tim_kiem, Danh_sach_Tivi)
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(danh_sach_Tivi_Xem)
    return render_template("Nhan_vien_nhap_hang/MH_Xem_Danh_sach_Tivi.html", Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)

@app.route("/nvnh/nhap/<string:Ma_so>/", methods=['GET','POST'])
def NVNH_Nhap_Tivi(Ma_so):
    if session.get("session_NVNH") == None:
        return redirect(url_for("NVNH_Dang_nhap"))

    Nhan_vien_Dang_nhap = session["session_NVNH"]
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Tivi_Chon = Lay_chi_tiet_Tivi(Danh_sach_Tivi, Ma_so)

    if Tivi_Chon != None:
        So_luong = 1
        Thong_bao = ""
        if request.method == "POST":
            So_luong = int(request.form.get("Th_So_luong"))
            Thanh_tien = Nhap_Tivi(Nhan_vien_Dang_nhap, Tivi_Chon, So_luong)
            Thong_bao =  "Vừa nhập " + str(So_luong) + " " + Tivi_Chon["Ten"] + "<br>"
            Thong_bao = 'Tiền phải trả là: {:,}'.format(Thanh_tien)
            Ghi_Tivi(Tivi_Chon)
    Chuoi_HTML_Tivi = Tao_Chuoi_HTML_Tivi(Tivi_Chon, Thong_bao, So_luong)
    return render_template("Nhan_vien_nhap_hang/MH_Nhap_Tivi.html", Chuoi_HTML_Tivi=Chuoi_HTML_Tivi)

