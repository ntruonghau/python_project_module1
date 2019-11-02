from flask import Markup, request, render_template, session, redirect
from Ban_Tivi import app
from Ban_Tivi.Xu_ly.Nhan_vien_Nhap_hang.Xu_ly_3L import *

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
        if Ma_so == "DANH_SACH"
            Dia_chi_Man_hinh = "/nvnh/danh-sach-tivi"
        elif Ma_so == "PHIEU_NHAP"
            pass
            
    return render_template("Nhan_vien_Nhap_hang/MH_Chinh.html", Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_Vien, Dia_chi_MH=Dia_chi_Man_hinh)

@app.route("/nvnh/dang-xuat", methods=['GET', 'POST'])
def NVNH_Dang_xuat():
    session.pop("session_NVNH", None)
    return redirect(url_for("NVNH_Dang_nhap"))

@app.route("/nvnh/danh-sach-tivi", methods=['GET','POST'])
def NVNH_Xem_DS_Tivi():
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    danh_sach_Tivi_Xem = Danh_sach_Tivi
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(danh_sach_Tivi_Xem)
    return render_template("Nhan_vien_nhap_hang/MH_Xem_Danh_sach_Tivi.html", Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)

# def NVNH_Thong_tin():
#     Nhan_vien_Dang_nhap = session["session_NVNH"]
#     Chuoi_HTML_Nhan_Vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)
