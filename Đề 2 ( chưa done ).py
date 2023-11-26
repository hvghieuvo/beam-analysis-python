import pandas as pd
import math

hinhI = pd.read_excel('chu_I.xlsx',dtype=dict)
hinhC = pd.read_excel('chu_C.xlsx',dtype=dict)

print('Từ kết quả của bài tính toán trên, hãy nhập những dữ liệu sau để thực hiện bài toán tính bền cho mặt cắt thanh dầm')
Mmax = float(input('Hãy nhập giá trị moment uốn lớn nhất trên thanh:'))
Qmax = float(input('Hãy nhập giá trị lực cắt lớn nhất trên thanh:'))
Qy = float(input('Hãy nhập giá trị lực cắt tại vị trí có moment lớn nhất:'))
sigma = float(input('Hãy nhập ứng suất cho phép (giới hạn bền):'))
loaimatcat = str(input('Hãy nhập loại mặt cắt:'))
if loaimatcat == 'hình chữ nhật':
    x,y = map(float,input('Hãy nhập kích thước dài x rộng:').split())
    print('Kích thước của hình chữ nhật:',x,y)
    thuyetben = input('Chọn thuyết bền muốn sử dụng cho bài toán (Von Mises hoặc Tresca):')
    if thuyetben == 'Von Mises':
        tau = sigma/math.sqrt(3)
    else:
        tau = sigma/2
    def hinhchunhat(x, y, Mmax, Qmax):
        Sx = x*y*(y/2)
        Sy = x*y*(x/2)
        Jx = (x*(y**3))/12
        Jy = (y*(x**3))/12
        Wx = (x*(y**2))/6
        Wy = (y*(x**2))/6
        print('Moment tĩnh Sx có giá trị là:', Sx)
        print('Moment tĩnh Sy có giá trị là:', Sy)
        print('Moment quán tính Jx có giá trị là:', Jx)
        print('Moment quán tính Jy có giá trị là:', Jy)
        print('Moment chống uốn Wx có giá trị là:', Wx)
        print('Moment chống uốn Wy có giá trị là:', Wy)
        print('Xét lớp biên, ta có:')
        sigmamax = (abs(Mmax)) / Wx
        print('Ứng suất pháp lớn nhất trên mặt cắt là:', sigmamax)
        if sigmamax <= sigma:
            print('Lớp biên thỏa bền')
        else:
            print('Lớp biên không thỏa bền')
        print('Xét lớp trung hòa, ta có:')
        taumax = (3*Qmax)/(2*x*y)
        print('Ứng suất tiếp lớn nhất trên mặt cắt là:', taumax)
        if taumax <= tau:
            print('Lớp trung hòa thỏa bền')
        else:
            print('Lớp trung hòa không thỏa bền')
        return Sx, Sy, Jx, Jy, Wx, Wy, sigmamax, taumax
    hinhchunhat(x, y, Mmax, Qmax)
elif loaimatcat == 'hình tròn':
    R = float(input('Hãy nhập vào bán kính hình tròn:'))
    print('Hình tròn có bán kính:',R)
    thuyetben = input('Chọn thuyết bền muốn sử dụng cho bài toán (Von Mises hoặc Tresca):')
    if thuyetben == 'Von Mises':
        tau = sigma/math.sqrt(3)
    else:
        tau = sigma/2
    def hinhtron(Mmax, Qmax, R):
        Jx = (3.14 * R ** 4) / 4
        Wx = (3.14 * R ** 3) / 4
        print('Moment quán tính Jx = Jy có giá trị là:', Jx)
        print('Moment chống uốn Wx = Wy có giá trị là:', Wx)
        print('Xét lớp biên, ta có:')
        sigmamax = (abs(Mmax)) / Wx
        print('Ứng suất pháp lớn nhất trên mặt cắt là:', sigmamax)
        if sigmamax <= sigma:
            print('Lớp biên thỏa bền')
        else:
            print('Lớp biên không thỏa bền')
        print('Xét lớp trung hòa, ta có:')
        taumax = (4 * Qmax) / (3 * 3.14 * R ** 2)
        print('Ứng suất tiếp lớn nhất trên mặt cắt là:', taumax)
        if taumax <= tau:
            print('Lớp trung hòa thỏa bền')
        else:
            print('Lớp trung hòa không thỏa bền')
        return Jx, Wx, sigmamax, taumax
    hinhtron(Mmax, Qmax, R)
elif loaimatcat == 'hình vành khăn':
    r1,r2 = map(float,input('Hãy nhập lần lượt kích thước bán kính trong và bán kính ngoài:').split())
    print('Hình vành khăn có kích thước:',r1,r2)
    thuyetben = input('Chọn thuyết bền muốn sử dụng cho bài toán (Von Mises hoặc Tresca):')
    if thuyetben == 'Von Mises':
        tau = sigma / math.sqrt(3)
    else:
        tau = sigma / 2
    def hinhvanhkhan(Mmax, Qmax, r1, r2):
        Jx = (3.14 * r2 ** 4) / 4 - (3.14 * r1 ** 4) / 4
        a = r1 / r2
        Wx = (3.14 * r2 ** 3) / 4 * (1 - a ** 4)
        print('Moment quán tính Jx = Jy có giá trị là:', Jx)
        print('Moment chống uốn Wx = Wy có giá trị là:', Wx)
        print('Xét lớp biên, ta có:')
        sigmamax = (abs(Mmax)) / Wx
        print('Ứng suất pháp lớn nhất trên mặt cắt là:', sigmamax)
        if sigmamax <= sigma:
            print('Lớp biên thỏa bền')
        else:
            print('Lớp biên không thỏa bền')
        print('Xét lớp trung hòa, ta có:')
        taumax = (4*Qmax)/(3*3.14*r2**2)- (4*Qmax)/(3*3.14*r1**2)
        print('Ứng suất tiếp lớn nhất trên mặt cắt là:', taumax)
        if taumax <= tau:
            print('Lớp trung hòa thỏa bền')
        else:
            print('Lớp trung hòa không thỏa bền')
        return Jx, Wx, sigmamax, taumax
    hinhvanhkhan(Mmax, Qmax, r1, r2)
elif loaimatcat == 'hình I':
    I = int(input('Hãy nhập số hiệu mặt cắt I:'))
    print('Mã số hiệu mặt cắt I:',I)
    # Tên cột cần chọn dữ liệu
    column_name = "N0"  # Thay bằng tên cột cần chọn
    # Chọn dữ liệu từ cột cụ thể
    selected_column = hinhI[hinhI[column_name] == I]
    # Hiển thị dữ liệu được chọn
    print(selected_column)
    for index, row in hinhI.iterrows():
        if I in row.values:
            hangchuagiatri = index  # Lưu ý: Index của hàng trong Excel bắt đầu từ 1, trong Python bắt đầu từ 0
            print(f"Giá trị '{I}' được tìm thấy ở hàng {hangchuagiatri}")
            break
    else:
        print(f"Giá trị '{I}' không được tìm thấy trong tệp Excel.")
    Sx = hinhI.iloc[hangchuagiatri, 12]
    Jx = hinhI.iloc[hangchuagiatri, 9]
    d = (hinhI.iloc[hangchuagiatri, 4]) / 10
    Wx = hinhI.iloc[hangchuagiatri, 10]
    Wy = hinhI.iloc[hangchuagiatri, 14]
    h = (hinhI.iloc[hangchuagiatri, 2]) / 10
    t = (hinhI.iloc[hangchuagiatri, 5]) / 10
    thuyetben = input('Chọn thuyết bền muốn sử dụng cho bài toán (Von Mises hoặc Tresca):')
    if thuyetben == 'Von Mises':
        tau = sigma / math.sqrt(3)
    else:
        tau = sigma / 2
    def hinhI(Qmax, Sx, Jx, d, Mmax, Wx):
        print('Xét lớp biên, ta có:')
        sigmamax = (abs(Mmax)) / Wx
        print('Ứng suất pháp lớn nhất trên mặt cắt là:', sigmamax)
        if sigmamax <= sigma:
            print('Lớp biên thỏa bền')
        else:
            print('Lớp biên không thỏa bền')
        taumax = (Qmax * Sx) / (Jx * d)
        print('Ứng suất tiếp lớn nhất trên mặt cắt là:', taumax)
        if taumax <= tau:
            print('Lớp trung hòa thỏa bền')
        else:
            print('Lớp trung hòa không thỏa bền')
        return sigmamax, taumax
    hinhI(Qmax, Sx, Jx, d, Mmax, Wx)
    # Tinh sigmatd
    print('Mặt cắt còn 1 lớp nguy hiểm -> tính trạng thái ứng suất phẳng đặc biệt qua lớp trung gian')
    def tinhsigmatd(Mmax, Jx, h, t, Qy, Sx, d):
        sigmaN = (Mmax / Jx) * (h / 2 - t)
        Sd = Sx - (d / 2) * (h / 2 - t) ** 2
        tauN = (Qy * Sd) / (Jx * d)
        if thuyetben == 'Von Mises':
            sigmatd = math.sqrt((sigmaN ** 2) + (3 * tauN ** 2))
        else:
            sigmatd = math.sqrt((sigmaN ** 2) + (4 * tauN ** 2))
        print('Ứng suất pháp tương đương của mặt cắt có giá trị là:', sigmatd)
        return sigmaN, Sd, tauN, sigmatd
    tinhsigmatd(Mmax, Jx, h, t, Qy, Sx, d)
    print('Kiểm bền cho thanh khi thanh nằm ngang')
    def kiembenngang(Mmax, Wy):
        sigmamin = abs(Mmax) / Wy
        print('sigmamin =', abs(sigmamin))
        if abs(sigmamin) > sigma:
            print('Thanh nằm ngang không bền')
        else:
            print('Thanh nằm ngang bền')
        return sigmamin
    kiembenngang(Mmax, Wy)
elif loaimatcat == 'hình C':
    C = input('Hãy nhập số hiệu mặt cắt C:')
    print('Mã số hiệu mặt cắt C:',C)
    # Tên cột cần chọn dữ liệu
    column_name = "N0"  # Thay bằng tên cột cần chọn
    # Chọn dữ liệu từ cột cụ thể
    selected_column = hinhC[hinhC[column_name] == C]
    # Hiển thị dữ liệu được chọn
    print(selected_column)
    for index, row in hinhC.iterrows():
        if C in row.values:
            hangchuagiatri = index  # Lưu ý: Index của hàng trong Excel bắt đầu từ 1, trong Python bắt đầu từ 0
            print(f"Giá trị '{C}' được tìm thấy ở hàng {hangchuagiatri}")
            break
    else:
        print(f"Giá trị '{C}' không được tìm thấy trong tệp Excel.")
    Sx = hinhC.iloc[hangchuagiatri, 12]
    Jx = hinhC.iloc[hangchuagiatri, 9]
    d = (hinhC.iloc[hangchuagiatri, 4]) / 10
    Wx = hinhC.iloc[hangchuagiatri, 10]
    Wy = hinhC.iloc[hangchuagiatri, 14]
    h = (hinhC.iloc[hangchuagiatri, 2]) / 10
    t = (hinhC.iloc[hangchuagiatri, 5]) / 10
    thuyetben = input('Chọn thuyết bền muốn sử dụng cho bài toán (Von Mises hoặc Tresca):')
    if thuyetben == 'Von Mises':
        tau = sigma / math.sqrt(3)
    else:
        tau = sigma / 2
    def hinhI(Qmax, Sx, Jx, d, Mmax, Wx):
        print('Xét lớp biên, ta có:')
        sigmamax = (abs(Mmax)) / Wx
        print('Ứng suất pháp lớn nhất trên mặt cắt là:', sigmamax)
        if sigmamax <= sigma:
            print('Lớp biên thỏa bền')
        else:
            print('Lớp biên không thỏa bền')
        taumax = (Qmax * Sx) / (Jx * d)
        print('Ứng suất tiếp lớn nhất trên mặt cắt là:', taumax)
        if taumax <= tau:
            print('Lớp trung hòa thỏa bền')
        else:
            print('Lớp trung hòa không thỏa bền')
        return sigmamax, taumax
    hinhI(Qmax, Sx, Jx, d, Mmax, Wx)
    # Tinh sigmatd
    print('Mặt cắt còn 1 lớp nguy hiểm -> tính trạng thái ứng suất phẳng đặc biệt qua lớp trung gian')
    def tinhsigmatd(Mmax, Jx, h, t, Qy, Sx, d):
        sigmaN = (Mmax / Jx) * (h / 2 - t)
        Sd = Sx - (d / 2) * (h / 2 - t) ** 2
        tauN = (Qy * Sd) / (Jx * d)
        if thuyetben == 'Von Mises':
            sigmatd = math.sqrt((sigmaN ** 2) + (3 * tauN ** 2))
        else:
            sigmatd = math.sqrt((sigmaN ** 2) + (4 * tauN ** 2))
        print('Ứng suất pháp tương đương của mặt cắt có giá trị là:', sigmatd)
        return sigmaN, Sd, tauN, sigmatd
    tinhsigmatd(Mmax, Jx, h, t, Qy, Sx, d)
    print('Kiểm bền cho thanh khi thanh nằm ngang')
    def kiembenngang(Mmax, Wy):
        sigmamin = abs(Mmax) / Wy
        print('sigmamin =', abs(sigmamin))
        if abs(sigmamin) > sigma:
            print('Thanh nằm ngang không bền')
        else:
            print('Thanh nằm ngang bền')
        return sigmamin
    kiembenngang(Mmax, Wy)
else:
    print('Hãy nhập đúng một trong các mặt cắt sau: hình chữ nhật, hình tròn, hình vành khăn, hình I, hình C')




