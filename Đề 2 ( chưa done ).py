import pandas as pd
import math

#============================Input============================
print('Từ kết quả của bài tính toán trên, hãy nhập những dữ liệu sau để thực hiện bài toán tính bền cho mặt cắt thanh dầm')
Mmax = float(input('Hãy nhập giá trị moment uốn lớn nhất trên thanh:'))
Qmax = float(input('Hãy nhập giá trị lực cắt lớn nhất trên thanh:'))
Qy = float(input('Hãy nhập giá trị lực cắt tại vị trí có moment lớn nhất:'))
sigma = float(input('Hãy nhập ứng suất cho phép (giới hạn bền):'))
loaimatcat = str(input('Hãy nhập loại mặt cắt:'))

#============================Define function============================
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
     taumax = (4*Qmax)/(3*3.14*(r2**2-r1**2))
     print('Ứng suất tiếp lớn nhất trên mặt cắt là:', taumax)
     if taumax <= tau:
         print('Lớp trung hòa thỏa bền')
     else:
         print('Lớp trung hòa không thỏa bền')
     return Jx, Wx, sigmamax, taumax
    
    
#============================  Core ============================
if loaimatcat == 'hình chữ nhật':
    x,y = map(float,input('Hãy nhập kích thước dài x rộng:').split())
    print('Kích thước của hình chữ nhật:',x,y)
    thuyetben = input('Chọn thuyết bền muốn sử dụng cho bài toán (Von Mises hoặc Tresca):')
    if thuyetben == 'Von Mises':
        tau = sigma/math.sqrt(3)
    else:
        tau = sigma/2
    hinhchunhat(x, y, Mmax, Qmax)
    
elif loaimatcat == 'hình tròn':
    R = float(input('Hãy nhập vào bán kính hình tròn:'))
    print('Hình tròn có bán kính:',R)
    thuyetben = input('Chọn thuyết bền muốn sử dụng cho bài toán (Von Mises hoặc Tresca):')
    if thuyetben == 'Von Mises':
        tau = sigma/math.sqrt(3)
    else:
        tau = sigma/2
    hinhtron(Mmax, Qmax, R)
    
elif loaimatcat == 'hình vành khăn':
    r1,r2 = map(float,input('Hãy nhập lần lượt kích thước bán kính trong và bán kính ngoài:').split())
    print('Hình vành khăn có kích thước:',r1,r2)
    thuyetben = input('Chọn thuyết bền muốn sử dụng cho bài toán (Von Mises hoặc Tresca):')
    if thuyetben == 'Von Mises':
        tau = sigma / math.sqrt(3)
    else:
        tau = sigma / 2
    hinhvanhkhan(Mmax, Qmax, r1, r2)
elif loaimatcat == 'hình I':
    I = input('Hãy nhập số hiệu mặt cắt I:')
    print('Mã số hiệu mặt cắt I:',I)



