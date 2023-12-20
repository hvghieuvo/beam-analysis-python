import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import sys

hinhI = pd.read_excel('chu_I.xlsx',dtype=dict)
hinhC = pd.read_excel('chu_C.xlsx',dtype=dict)

print('Từ kết quả của bài tính toán trên, hãy nhập những dữ liệu sau để thực hiện bài toán tính bền cho mặt cắt thanh dầm')
Mmax = float(input('Hãy nhập giá trị moment uốn lớn nhất trên thanh:'))
Qmax = float(input('Hãy nhập giá trị lực cắt lớn nhất trên thanh:'))
Qy = float(input('Hãy nhập giá trị lực cắt tại vị trí có moment lớn nhất:'))
sigma = float(input('Hãy nhập ứng suất giới hạn kéo cho phép:'))
sigman = float(input('Hãy nhập ứng suất giới hạn nén cho phép:'))
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

            # PLOT CROSS-SECTION

        step_min, step_max = min(x, y), max(x, y)
        avg_step = (step_max + step_min) / 2
        plt.ylim(-1.1 * avg_step, 1.1 * avg_step)

        x_rec, y_rec = [0, x, x, 0, 0], [-.5 * y, -.5 * y, .5 * y, .5 * y, -.5 * y]
        plt.plot(x_rec, y_rec)
        # Rectangular Shape
        x_st = [1.2 * step_max, 1.2 * step_max + step_min, 1.2 * step_max + step_min, 1.2 * step_max + 2 * step_min,
                1.2 * step_max]
        y_st = [y / 2, y / 2, -y / 2, -y / 2, y / 2]

        if Qy > 0:
            plt.plot(x_st, y_st)
            plt.text(1.2 * step_max, 1.05 * y / 2, r"$\sigma_{min}$", fontsize=14)
            plt.text(1.2 * step_max + 1.4 * step_min, -1.15 * y / 2, r"$\sigma_{max}$", fontsize=14)
        else:
            mirrored_y_St = [-yi for yi in y_st]
            plt.plot(x_st, mirrored_y_St)
            plt.text(1.2 * step_max, -1.15 * y / 2, r"$\sigma_{min}$", fontsize=14)
            plt.text(1.2 * step_max + 1.4 * step_min, 1.05 * y / 2, r"$\sigma_{max}$", fontsize=14)

        # Calculate the center of the half circle
        x_circle_center = 1.20 * step_max + 3 * step_min
        y_circle_center = 0
        theta = np.linspace(-np.pi / 2, np.pi / 2, 100)  # Create theta values for the half circle
        radius = y / 2  # Radius of the half circle
        # Calculate x and y coordinates for the half circle
        x_circle = x_circle_center + radius * np.cos(theta)
        y_circle = y_circle_center + radius * np.sin(theta)

        plt.plot([x_circle_center, x_circle_center], [y / 2, -y / 2])
        plt.plot(x_circle, y_circle)
        plt.text(1.20 * step_max + 3 * step_min + 1.1 * radius, -.2 * y / 2, r"$\tau_{max}$", fontsize=14)
        plt.plot([x / 2, 1.20 * step_max + 3 * step_min + 2 * radius], [0, 0], linestyle="--", color='k')  # X-axis
        plt.plot([x / 2, x / 2], [-1.25 * y / 2, 0], linestyle="--", color='k')  # Y-axis
        plt.text(1.20 * step_max + 3 * step_min + 2 * radius, .05 * y / 2, "x", fontsize=14)
        plt.text(1.05 * x / 2, -1.25 * y / 2, "y", fontsize=14)

        plt.title(fr"RECTANGULAR CROSS SECTION (x = {x}, y = {y})")
        plt.axis("off")
        plt.show()

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
#PLOT
        radius = R
        figure, axes = plt.subplots()
        Circle = plt.Circle((0, 0), radius, fill=False, color="b")
        axes.set_aspect('equal', adjustable='box')
        axes.add_patch(Circle)

        x = [1.5 * R, 2.5 * R, 2.5 * R, 3.5 * R, 1.5 * R]
        y = [R, R, -R, -R, R]

        if Qy > 0:
            plt.plot(x, y)
            plt.text(1.85 * radius, .75 * radius, r"$\sigma_{min}$", fontsize=14)
            plt.text(2.6 * radius, -.85 * radius, r"$\sigma_{max}$", fontsize=14)
        else:
            mirrored_y = [-yi for yi in y]
            plt.plot(x, mirrored_y)
            plt.text(1.85 * radius, -.85 * radius, r"$\sigma_{min}$", fontsize=14)
            plt.text(2.6 * radius, .75 * radius, r"$\sigma_{max}$", fontsize=14)

        theta_tau = np.linspace(-np.pi / 2, np.pi / 2, 150)
        a_tau = radius * np.cos(theta_tau) + 4 * radius
        b_tau = radius * np.sin(theta_tau)
        plt.plot(a_tau, b_tau)
        plt.plot([4 * radius, 4 * radius], [-R, R])

        plt.plot([0, 0], [0, -1.2 * R], linestyle="--", color='k')  # Y-axis
        plt.plot([0, 5.2 * R], [0, 0], linestyle="--", color='k')  # X-axis
        plt.text(5.1 * R, .1 * R, "x", fontsize=14)
        plt.text(.1 * R, -1.2 * R, "y", fontsize=14)

        plt.title(fr"Circular Cross-Section with radius R = {R}")

        plt.show()

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
            # PLOT CROSS-SECTION AND STRESS DESCRIPTION

        n, radius = 50, [r1, r2]
        theta = np.linspace(0, 2 * np.pi, n, endpoint=True)
        xs = np.outer(radius, np.cos(theta))
        ys = np.outer(radius, np.sin(theta))
        # IN ORDER TO HAVE A CLOSED AREA, THE CIRCLES SHOULD BE TRAVERSED IN OPPOSITE DIRECTIONS
        xs[1, :] = xs[1, ::-1]
        ys[1, :] = ys[1, ::-1]
        plt.subplot(111, aspect='equal')
        plt.fill(np.ravel(xs), np.ravel(ys))

        plt.ylim(-1.2 * r2, 1.2 * r2)

        x = [1.5 * r2, 2.5 * r2, 2.5 * r2, 3.5 * r2, 1.5 * r2]
        y = [r2, r2, -r2, -r2, r2]

        if Qy > 0:
            plt.plot(x, y)
            plt.text(1.85 * r2, .75 * r2, r"$\sigma_{min}$", fontsize=14)
            plt.text(2.6 * r2, -.85 * r2, r"$\sigma_{max}$", fontsize=14)
        else:
            mirrored_y = [-yi for yi in y]
            plt.plot(x, mirrored_y)
            plt.text(1.85 * r2, -.85 * r2, r"$\sigma_{min}$", fontsize=14)
            plt.text(2.6 * r2, .75 * r2, r"$\sigma_{max}$", fontsize=14)

        theta_tau = np.linspace(-np.pi / 2, np.pi / 2, 150)
        a_tau = r2 * np.cos(theta_tau) + 4 * r2
        b_tau = r2 * np.sin(theta_tau)
        plt.plot(a_tau, b_tau)
        plt.plot([4 * r2, 4 * r2], [-r2, r2])
        plt.text(5 * r2, -0.09 * r2, r"$\tau_{max}$", fontsize=14)

        plt.plot([0, 0], [0, -1.2 * r2], linestyle="--", color='k')  # Y-axis
        plt.plot([0, 5.2 * r2], [0, 0], linestyle="--", color='k')  # X-axis
        plt.text(5.2 * r2, .1 * r2, "x", fontsize=14)
        plt.text(.1 * r2, -1.1 * r2, "y", fontsize=14)

        plt.title(f"ANNULAR CROSS-SECTION WITH $(r1, r2) = ({r1}, {r2})$")

        plt.show()
        return Jx, Wx, sigmamax, taumax
    hinhvanhkhan(Mmax, Qmax, r1, r2)
elif loaimatcat == 'hình I':
    I = input('Hãy nhập số hiệu mặt cắt I:')
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
    Jy = hinhI.iloc[hangchuagiatri, 13]
    d = (hinhI.iloc[hangchuagiatri, 4]) / 10
    b = (hinhI.iloc[hangchuagiatri, 3]) / 10
    Wx = hinhI.iloc[hangchuagiatri, 10]
    Wy = hinhI.iloc[hangchuagiatri, 14]
    h = (hinhI.iloc[hangchuagiatri, 2]) / 10
    t = (hinhI.iloc[hangchuagiatri, 5]) / 10
    thuyetben = input('Chọn thuyết bền muốn sử dụng cho bài toán (Von Mises hoặc Tresca):')
    if thuyetben == 'Von Mises':
        tau = sigma / math.sqrt(3)
    else:
        tau = sigma / 2
    def hinhI():
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
        return
    hinhI()
    # Tinh sigmatd
    print('Mặt cắt còn 1 lớp nguy hiểm -> tính trạng thái ứng suất phẳng đặc biệt qua lớp trung gian')
    def tinhsigmatd():
        sigmaN = (Mmax / Jx) * (h / 2 - t)
        Sd = Sx - (d / 2) * (h / 2 - t) ** 2
        tauN = (Qy * Sd) / (Jx * d)
        if thuyetben == 'Von Mises':
            sigmatd = math.sqrt((sigmaN ** 2) + (3 * tauN ** 2))
        else:
            sigmatd = math.sqrt((sigmaN ** 2) + (4 * tauN ** 2))
        print('Ứng suất pháp tương đương của mặt cắt có giá trị là:', sigmatd)
        return
    tinhsigmatd()
    print('Kiểm bền cho thanh khi thanh nằm ngang')
    def kiembenngang():
        sigmamin = abs(Mmax) / Wy
        print('sigmamin =', abs(sigmamin))
        if abs(sigmamin) > sigman:
            print('Thanh nằm ngang không bền')
        else:
            print('Thanh nằm ngang bền')
        return
        kiembenngang()
        # PLOT CROSS-SECTION AND STRESS DESCRIPTION

    plt.subplot(2, 1, 1)

    x_vertical = [0, h / 2, h / 2, d / 2, d / 2, h / 2, h / 2, 0]
    y_vertical = [-h / 2, -h / 2, -(h - 2 * t) / 2, -(h - 2 * t) / 2, (h - 2 * t) / 2, (h - 2 * t) / 2, h / 2,
                      h / 2]

        # Plot the original rectangular shape
    plt.plot(x_vertical, y_vertical, color="b")

        # Mirror the rectangular shape about the y-axis
    mirrored_x_vertical = [-xi for xi in x_vertical]  # Reverse the sign of each x-coordinate about y-axis
    plt.plot(mirrored_x_vertical, y_vertical, color="b")

    x_st = [1 * b, 2 * b, 2 * b, 3 * b, 1 * b]
    y_st = [h / 2, h / 2, -h / 2, -h / 2, h / 2]

    if Qy > 0:
        plt.plot(x_st, y_st)
        plt.text(1.35 * b, 0.35 * h, r"$\sigma_{min}$", fontsize=14)
        plt.text(2.1 * b, -0.45 * h, r"$\sigma_{max}$", fontsize=14)
    else:
        mirrored_y_st = [-yi for yi in y_st]
        plt.plot(x_st, mirrored_y_st)
        plt.text(1.35 * b, -0.45 * h, r"$\sigma_{min}$", fontsize=14)
        plt.text(2.05 * b, 0.35 * h, r"$\sigma_{max}$", fontsize=14)

    theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
    radius = h / 2
    x_t = 3.5 * b + radius * np.cos(theta)
    y_t = radius * np.sin(theta)
    plt.plot(x_t, y_t)
    plt.plot([3.5 * b, 3.5 * b], [-h / 2, h / 2])
    plt.text(3.5 * b + h / 2, -.1 * h, r"$\tau_{max}$", fontsize=14)

    plt.plot([0, 3.5 * b + 1.2 * h / 2], [0, 0], color="k", linestyle="--")
    plt.plot([0, 0], [0, -.6 * h], color="k", linestyle="--")
    plt.text(3.5 * b + 1.2 * h / 2, .02 * h, "x", fontsize=14)
    plt.text(.5 * d, -.6 * h, "y", fontsize=14)

        # Set aspect ratio to be equal
    plt.axis("off")
    plt.axis("equal")
    plt.title("I-SHAPE CROSS-SECTION IN CM AND ITS STRESS DESCRIPTION")

    plt.subplot(2, 1, 2)
    x_horizontal = [0, 0, t, t, h - t, h - t, h, h]
    y_horizontal = [0, b / 2, b / 2, d / 2, d / 2, b / 2, b / 2, 0]
    plt.plot(x_horizontal, y_horizontal, color='b')

    mirrored_y_horizontal = [-yi for yi in y_horizontal]
    plt.plot(x_horizontal, mirrored_y_horizontal, color='b')

    step = h + b
    x_st = [step, step + b, step + b, step + 2 * b, step]
    y_st = [b / 2, b / 2, -b / 2, -b / 2, b / 2]

    if Qy > 0:
        plt.plot(x_st, y_st)
        plt.text(step + .35 * b, 0.35 * b, r"$\sigma_{min}$", fontsize=14)
        plt.text(step + 1.15 * b, -0.45 * b, r"$\sigma_{max}$", fontsize=14)
    else:
        mirrored_y_st = [-yi for yi in y_st]
        plt.plot(x_st, mirrored_y_st)
        plt.text(step + .35 * b, -0.45 * b, r"$\sigma_{min}$", fontsize=14)
        plt.text(step + 1.05 * b, 0.35 * b, r"$\sigma_{max}$", fontsize=14)

    theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
    radius = b / 2
    x_t = step + 3 * b + radius * np.cos(theta)
    y_t = radius * np.sin(theta)
    plt.plot(x_t, y_t)
    plt.plot([step + 3 * b, step + 3 * b], [-b / 2, b / 2])
    plt.text(step + 3 * b + radius, -.1 * b, r"$\tau_{max}$", fontsize=14)

    plt.plot([h / 2, step + 3.7 * b], [0, 0], color="k", linestyle="--")
    plt.plot([h / 2, h / 2], [0, -.6 * b], color="k", linestyle="--")
    plt.text(step + 3.7 * b, .02 * b, "x", fontsize=14)
    plt.text(.52 * h, -.6 * b, "y", fontsize=14)

    plt.axis("off")
    plt.show()
    plt.show()
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
    Jy = hinhI.iloc[hangchuagiatri, 13]
    b = (hinhI.iloc[hangchuagiatri, 3]) / 10
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
        if abs(sigmamin) > sigman:
            print('Thanh nằm ngang không bền')
        else:
            print('Thanh nằm ngang bền')
        return sigmamin
    kiembenngang(Mmax, Wy)
    # PLOT CROSS-SECTION AND STRESS DESCRIPTION

    plt.subplot(2, 1, 1)
    x_vertical = [0, 0, b, b, d, d]
    y_vertical = [0, h / 2, h / 2, (h - 2 * t) / 2, (h - 2 * t) / 2, 0]

    # Plot the original shape
    plt.plot(x_vertical, y_vertical, color="b")

    # Mirror the rectangular shape about the y-axis
    mirrored_y_vertical = [-yi for yi in y_vertical]  # Reverse the sign of each y-coordinate
    plt.plot(x_vertical, mirrored_y_vertical, color="b")
    x_st = [2 * b, 3 * b, 3 * b, 4 * b, 2 * b]
    y_st = [h / 2, h / 2, -h / 2, -h / 2, h / 2]

    if Qy > 0:
        plt.plot(x_st, y_st)
        plt.text(2.35 * b, 0.35 * h, r"$\sigma_{min}$", fontsize=14)
        plt.text(3.1 * b, -0.45 * h, r"$\sigma_{max}$", fontsize=14)
    else:
        mirrored_y_st = [-yi for yi in y_st]
        plt.plot(x_st, mirrored_y_st)
        plt.text(2.35 * b, -0.45 * h, r"$\sigma_{min}$", fontsize=14)
        plt.text(3.05 * b, 0.35 * h, r"$\sigma_{max}$", fontsize=14)

    theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
    radius = h / 2
    x_t = 5 * b + radius * np.cos(theta)
    y_t = radius * np.sin(theta)
    plt.plot(x_t, y_t)
    plt.plot([5 * b, 5 * b], [-h / 2, h / 2])
    plt.text(5 * b + radius, -.1 * h, r"$\tau_{max}$", fontsize=14)

    plt.plot([b / 2, 5 * b + 1.2 * radius], [0, 0], color='k', linestyle='--')
    plt.plot([b / 2, b / 2], [0, -.6 * h], color='k', linestyle='--')
    plt.text(5 * b + 1.2 * radius, .05 * h, 'x', fontsize=14)
    plt.text(.6 * b, -.6 * h, 'y', fontsize=14)

    # Set aspect ratio to be equal
    plt.axis("off")
    plt.axis("equal")
    plt.title("C-SHAPE CROSS-SECTION IN MM AND ITS STRESS DESCRIPTION")

    plt.subplot(2, 1, 2)
    x_horizontal = [0, h, h, h - t, h - t, t, t, 0, 0]
    y_horizontal = [b / 2, b / 2, -b / 2, -b / 2, b / 2 - d, b / 2 - d, -b / 2, -b / 2, b / 2]
    plt.plot(x_horizontal, y_horizontal, color='b')

    step = h + b
    x_st = [step, step + b, step + b, step + 2 * b, step]
    y_st = [b / 2, b / 2, -b / 2, -b / 2, b / 2]

    if Qy > 0:
        plt.plot(x_st, y_st)
        plt.text(step + .35 * b, 0.35 * b, r"$\sigma_{min}$", fontsize=14)
        plt.text(step + 1.15 * b, -0.45 * b, r"$\sigma_{max}$", fontsize=14)
    else:
        mirrored_y_st = [-yi for yi in y_st]
        plt.plot(x_st, mirrored_y_st)
        plt.text(step + .35 * b, -0.45 * b, r"$\sigma_{min}$", fontsize=14)
        plt.text(step + 1.05 * b, 0.35 * b, r"$\sigma_{max}$", fontsize=14)

    theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
    radius = b / 2
    x_t = step + 3 * b + radius * np.cos(theta)
    y_t = radius * np.sin(theta)
    plt.plot(x_t, y_t)
    plt.plot([step + 3 * b, step + 3 * b], [-b / 2, b / 2])
    plt.text(step + 3 * b + radius, -.1 * b, r"$\tau_{max}$", fontsize=14)

    plt.plot([h / 2, step + 3.7 * b], [0, 0], color="k", linestyle="--")
    plt.plot([h / 2, h / 2], [0, -.6 * b], color="k", linestyle="--")
    plt.text(step + 3.7 * b, .02 * b, "x", fontsize=14)
    plt.text(.52 * h, -.6 * b, "y", fontsize=14)

    plt.axis("off")
    plt.show()
else:
    print('Hãy nhập đúng một trong các mặt cắt sau: hình chữ nhật, hình tròn, hình vành khăn, hình I, hình C')




