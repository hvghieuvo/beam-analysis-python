import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import sys

#============================= Func hình chữ nhật #=============================
def hinhchunhat(x, y, Mmax, Qmax):
    Sx = x*y*(y/2)
    Sy = x*y*(x/2)
    Jx = (x*(y**3))/12
    Jy = (y*(x**3))/12
    Wx = (x*(y**2))/6
    Wy = (y*(x**2))/6
    # print('Moment tĩnh Sx có giá trị là:', Sx)
    # print('Moment tĩnh Sy có giá trị là:', Sy)
    # print('Moment quán tính Jx có giá trị là:', Jx)
    # print('Moment quán tính Jy có giá trị là:', Jy)
    # moment of inertia
    # print('Moment chống uốn Wx có giá trị là:', Wx)
    # print('Moment chống uốn Wy có giá trị là:', Wy)
    # print('Xét lớp biên, ta có:')
    
    sigmamax = (abs(Mmax)) / Wx
    sigmamin = -sigmamax
    # print('Ứng suất pháp lớn nhất trên mặt cắt là:', sigmamax)
    # if sigmamax <= sigma:
    #     print('Lớp biên thỏa bền')
    # else:
    #     print('Lớp biên không thỏa bền')
        
    # print('Xét lớp trung hòa, ta có:')
    
    taumax = (3*Qmax)/(2*x*y)
    # print('Ứng suất tiếp lớn nhất trên mặt cắt là:', taumax)
    # if taumax <= tau:
    #     print('Lớp trung hòa thỏa bền')
    # else:
    #     print('Lớp trung hòa không thỏa bền')
    return Sx, Sy, Jx, Jy, Wx, Wy, sigmamax, taumax

def plot_rec(x, y, Qy):
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
        plt.text(1.2 * step_max, 1.05 * y / 2, fr"$\sigma_{{min}}$={sigmamin}", fontsize=14)
        plt.text(1.2 * step_max + 1.4 * step_min, -1.15 * y / 2, fr"$\sigma_{{max}}$={sigmamax}", fontsize=14)
    else:
        mirrored_y_St = [-yi for yi in y_st]
        plt.plot(x_st, mirrored_y_St)
        plt.text(1.2 * step_max, -1.15 * y / 2, fr"$\sigma_{{min}}$={sigmamin}", fontsize=14)
        plt.text(1.2 * step_max + 1.4 * step_min, 1.05 * y / 2, fr"$\sigma_{{max}}$={sigmamax}", fontsize=14)

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
    plt.text(1.20 * step_max + 3 * step_min + 1.1 * radius, -.2 * y / 2, fr"$\tau_{{max}}$={abs(taumax)}", fontsize=14)
    plt.plot([x / 2, 1.20 * step_max + 3 * step_min + 2 * radius], [0, 0], linestyle="--", color='k')  # X-axis
    plt.plot([x / 2, x / 2], [-1.25 * y / 2, 0], linestyle="--", color='k')  # Y-axis
    plt.text(1.20 * step_max + 3 * step_min + 2 * radius, .05 * y / 2, "x", fontsize=14)
    plt.text(1.05 * x / 2, -1.25 * y / 2, "y", fontsize=14)

    plt.title(fr"RECTANGULAR CROSS SECTION ")
    plt.text(0, (1.05 * y / 2), fr"$x$={x}", fontsize=14)
    plt.text(-x/2, -.2 * y / 2, f"$y$={y}", fontsize=14)
    plt.axis("off")
    
    plt.savefig("./images/plot_rec", bbox_inches='tight', pad_inches=0.1)
    plt.close()

#============================= Func hình tròn #=============================
def hinhtron(Mmax, Qmax, R):
    Jx = (3.14 * R ** 4) / 4
    Wx = (3.14 * R ** 3) / 4
    # print('Moment quán tính Jx = Jy có giá trị là:', Jx)
    # print('Moment chống uốn Wx = Wy có giá trị là:', Wx)
    # print('Xét lớp biên, ta có:')
    sigmamax = (abs(Mmax)) / Wx
    sigmamin = -sigmamax
    # # print('Ứng suất pháp lớn nhất trên mặt cắt là:', sigmamax)
    # if sigmamax <= sigma:
    #     print('Lớp biên thỏa bền')
    # else:
    #     print('Lớp biên không thỏa bền')
    # print('Xét lớp trung hòa, ta có:')
    taumax = (4 * Qmax) / (3 * 3.14 * R ** 2)
    # print('Ứng suất tiếp lớn nhất trên mặt cắt là:', taumax)
    # if taumax <= tau:
    #     print('Lớp trung hòa thỏa bền')
    # else:
    #     print('Lớp trung hòa không thỏa bền')
    return Jx, Wx, sigmamax, taumax

def plot_circle(R, Qy):
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
        plt.text(1.85 * radius, .75 * radius, fr"$\sigma_{{min}}$={sigmamin}", fontsize=14)
        plt.text(2.6 * radius, -.85 * radius, fr"$\sigma_{{max}}$={sigmamax}", fontsize=14)
    else:
        mirrored_y = [-yi for yi in y]
        plt.plot(x, mirrored_y)
        plt.text(1.85 * radius, -.85 * radius, fr"$\sigma_{{min}}$={sigmamin}", fontsize=14)
        plt.text(2.6 * radius, .75 * radius, fr"$\sigma_{{max}}$={sigmamax}", fontsize=14)

    theta_tau = np.linspace(-np.pi / 2, np.pi / 2, 150)
    a_tau = radius * np.cos(theta_tau) + 4 * radius
    b_tau = radius * np.sin(theta_tau)
    plt.plot(a_tau, b_tau)
    plt.plot([4 * radius, 4 * radius], [-R, R])
    
    plt.text(5*R,-R/3, fr"$\tau_{{max}}$={abs(taumax)}",fontsize=14)

    plt.plot([0, 0], [0, -1.2 * R], linestyle="--", color='k')  # Y-axis
    plt.plot([0, 5.2 * R], [0, 0], linestyle="--", color='k')  # X-axis
    plt.text(5.1 * R, .1 * R, "x", fontsize=14)
    plt.text(.1 * R, -1.2 * R, "y", fontsize=14)
    

    plt.title(fr"Circular Cross-Section")
    plt.axis("off")
    plt.text(-R, R/3, f"$R$={R}", fontsize=14)

    plt.savefig("./images/plot_circle", bbox_inches='tight', pad_inches=0.1)
    plt.close()

#============================= Func hình vành khăn #=============================
def hinhvanhkhan(Mmax, Qmax, r1, r2):
    Jx = (3.14 * r2 ** 4) / 4 - (3.14 * r1 ** 4) / 4
    a = r1 / r2
    Wx = (3.14 * r2 ** 3) / 4 * (1 - a ** 4)
    # print('Moment quán tính Jx = Jy có giá trị là:', Jx)
    # print('Moment chống uốn Wx = Wy có giá trị là:', Wx)
    # print('Xét lớp biên, ta có:')
    sigmamax = (abs(Mmax)) / Wx
    sigmamin = -sigmamax
    # print('Ứng suất pháp lớn nhất trên mặt cắt là:', sigmamax)
    # if sigmamax <= sigma:
    #     print('Lớp biên thỏa bền')
    # else:
    #     print('Lớp biên không thỏa bền')
    # print('Xét lớp trung hòa, ta có:')
    taumax = (4*Qmax)/(3*3.14*r2**2)- (4*Qmax)/(3*3.14*r1**2)
    # print('Ứng suất tiếp lớn nhất trên mặt cắt là:', taumax)
    # if taumax <= tau:
    #     print('Lớp trung hòa thỏa bền')
    # else:
    #     print('Lớp trung hòa không thỏa bền')
    return Jx, Wx, sigmamax, taumax

def plot_annulus(r1, r2, Qy):
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
        plt.text(1.85 * r2, .75 * r2, fr"$\sigma_{{min}}$={sigmamin}", fontsize=14)
        plt.text(2.6 * r2, -.85 * r2, fr"$\sigma_{{max}}$={sigmamax}", fontsize=14)
    else:
        mirrored_y = [-yi for yi in y]
        plt.plot(x, mirrored_y)
        plt.text(1.85 * r2, -.85 * r2, fr"$\sigma_{{min}}$={sigmamin}", fontsize=14)
        plt.text(2.6 * r2, .75 * r2, fr"$\sigma_{{max}}$={sigmamax}", fontsize=14)

    theta_tau = np.linspace(-np.pi / 2, np.pi / 2, 150)
    a_tau = r2 * np.cos(theta_tau) + 4 * r2
    b_tau = r2 * np.sin(theta_tau)
    plt.plot(a_tau, b_tau)
    plt.plot([4 * r2, 4 * r2], [-r2, r2])
    plt.text(5 * r2, -0.09 * r2, fr"$\tau_{{max}}$={abs(taumax)}", fontsize=14)

    plt.plot([0, 0], [0, -1.2 * r2], linestyle="--", color='k')  # Y-axis
    plt.plot([0, 5.2 * r2], [0, 0], linestyle="--", color='k')  # X-axis
    plt.text(5.2 * r2, .1 * r2, "x", fontsize=14)
    plt.text(.1 * r2, -1.1 * r2, "y", fontsize=14)

    plt.title(f"ANNULAR CROSS-SECTION")
    plt.text(-r1, r2 / 3, f"$R1$={r1}", fontsize=14)
    plt.text(r2, r2 / 3, f"$R2$={r2}", fontsize=14)
    plt.axis("off")

    plt.savefig("./images/plot_annulus", bbox_inches='tight', pad_inches=0.1)
    plt.close()

#============================= Func hình I C #=============================
def hinh_I_C(thuyetben, Qy, Qmax, Mmax, Sx, Jx, d, h, t, Wx, Wy, sigma):
    #Đổi đon vị:
    h = float(h)/10
    d = float(d)/10
    t = float(t)/10
    Sx, Jx, Wx, Wy = float(Sx), float(Jx), float(Wx), float(Wy)
    if thuyetben == 'Von Mises':
        tau = sigma / math.sqrt(3)
    else:
        tau = sigma / 2
    sigmamax = (abs(Mmax)) / Wx
    taumax = (Qmax * Sx) / (Jx * d)
    sigmaN = (Mmax / Jx) * (h / 2 - t)
    Sd = Sx - (d / 2) * (h / 2 - t) ** 2
    tauN = (Qy * Sd) / (Jx * d)
    if thuyetben == 'von Mises':
        sigmatd = math.sqrt((sigmaN ** 2) + (3 * tauN ** 2))
        
    elif thuyetben == "Tresca":
        sigmatd = math.sqrt((sigmaN ** 2) + (4 * tauN ** 2))
    
    sigmamin = abs(Mmax) / Wy
        
    return sigmamax, sigmatd, sigmamin, tau, taumax, sigmaN

# def tinhsigmatd(Mmax, Jx, h, t, Qy, Sx, d):
#     sigmaN = (Mmax / Jx) * (h / 2 - t)
#     Sd = Sx - (d / 2) * (h / 2 - t) ** 2
#     tauN = (Qy * Sd) / (Jx * d)
#     if thuyetben == 'Von Mises':
#         sigmatd = math.sqrt((sigmaN ** 2) + (3 * tauN ** 2))
#     else:
#         sigmatd = math.sqrt((sigmaN ** 2) + (4 * tauN ** 2))
#     print('Ứng suất pháp tương đương của mặt cắt có giá trị là:', sigmatd)
#     return sigmaN, Sd, tauN, sigmatd
    
# def kiembenngang(Mmax, Wy):
#     sigmamin = abs(Mmax) / Wy
#     print('sigmamin =', abs(sigmamin))
#     if abs(sigmamin) > sigma:
#         print('Thanh nằm ngang không bền')
#     else:
#         print('Thanh nằm ngang bền')
#     return sigmamin
    
#============================= Func plot hình I #=============================

def plot_I(Qy, h, b, d, t):
        
    # PLOT CROSS-SECTION AND STRESS DESCRIPTION
    h = float(h)/10
    b = float(b)/10
    d = float(d)/10
    t = float(t)/10
    
    plt.subplot(2, 1, 1)

    x_vertical = [0, h / 2, h / 2, d / 2, d / 2, h / 2, h / 2, 0]
    y_vertical = [-h / 2, -h / 2, -(h - 2 * t) / 2, -(h - 2 * t) / 2, (h - 2 * t) / 2, (h - 2 * t) / 2, h / 2,
                      h / 2]

        # Plot the original rectangular shape
    plt.plot(x_vertical, y_vertical, color="black")

        # Mirror the rectangular shape about the y-axis
    mirrored_x_vertical = [-xi for xi in x_vertical]  # Reverse the sign of each x-coordinate about y-axis
    plt.plot(mirrored_x_vertical, y_vertical, color="black")

    x_st = [1 * b, 2 * b, 2 * b, 3 * b, 1 * b]
    y_st = [h / 2, h / 2, -h / 2, -h / 2, h / 2]

    if Qy > 0:
        plt.plot(x_st, y_st)
        plt.text(1.35 * b, 0.35 * h, fr"$\sigma_{{min}}$={-sigmamax}", fontsize=14)
        plt.text(2.1 * b, -0.45 * h, fr"$\sigma_{{max}}$={sigmamax}", fontsize=14)
    else:
        mirrored_y_st = [-yi for yi in y_st]
        plt.plot(x_st, mirrored_y_st)
        plt.text(1.35 * b, -0.45 * h, fr"$\sigma_{{min}}$={-sigmamax}", fontsize=14)
        plt.text(2.05 * b, 0.35 * h, fr"$\sigma_{{max}}$={sigmamax}", fontsize=14)

    theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
    radius = h / 2
    x_t = 3.5 * b + radius * np.cos(theta)
    y_t = radius * np.sin(theta)
    plt.plot(x_t, y_t)
    plt.plot([3.5 * b, 3.5 * b], [-h / 2, h / 2])
    plt.text(3.5 * b + h / 2, -.1 * h, fr"$\tau_{{max}}$={abs(taumax)}", fontsize=14)

    plt.plot([0, 3.5 * b + 1.2 * h / 2], [0, 0], color="black", linestyle="-")
    plt.plot([0, 0], [0, -.6 * h], color="black", linestyle="-")
    plt.text(3.5 * b + 1.2 * h / 2, .02 * h, "x", fontsize=14)
    plt.text(.5 * d, -.6 * h, "y", fontsize=14)

        # Set aspect ratio to be equal
    plt.axis("off")
    plt.axis("equal")
    plt.title("I-SHAPE CROSS-SECTION ")

    plt.subplot(2, 1, 2)
    x_horizontal = [0, 0, t, t, h - t, h - t, h, h]
    y_horizontal = [0, b / 2, b / 2, d / 2, d / 2, b / 2, b / 2, 0]
    plt.plot(x_horizontal, y_horizontal, color='black')

    mirrored_y_horizontal = [-yi for yi in y_horizontal]
    plt.plot(x_horizontal, mirrored_y_horizontal, color='black')

    step = h + b
    x_st = [step, step + b, step + b, step + 2 * b, step]
    y_st = [b / 2, b / 2, -b / 2, -b / 2, b / 2]

    if Qy > 0:
        plt.plot(x_st, y_st)
        plt.text(step + .35 * b, 0.35 * b, fr"$\sigma_{{min}}$={-sigmatd}", fontsize=14)
        plt.text(step + 1.15 * b, -0.45 * b, fr"$\sigma_{{max}}$={sigmatd}", fontsize=14)
    else:
        mirrored_y_st = [-yi for yi in y_st]
        plt.plot(x_st, mirrored_y_st)
        plt.text(step + .35 * b, -0.45 * b, fr"$\sigma_{{min}}$={-sigmatd}", fontsize=14)
        plt.text(step + 1.05 * b, 0.35 * b, fr"$\sigma_{{max}}$={sigmatd}", fontsize=14)

    theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
    radius = b / 2
    x_t = step + 3 * b + radius * np.cos(theta)
    y_t = radius * np.sin(theta)
    plt.plot(x_t, y_t)
    plt.plot([step + 3 * b, step + 3 * b], [-b / 2, b / 2])
    plt.text(step + 3 * b + radius, -.1 * b, fr"$\tau_{{max}}$={abs(taumax)}", fontsize=14)

    plt.plot([h / 2, step + 3.7 * b], [0, 0], color="black", linestyle="-")
    plt.plot([h / 2, h / 2], [0, -.6 * b], color="black", linestyle="-")
    plt.text(step + 3.7 * b, .02 * b, "x", fontsize=14)
    plt.text(.52 * h, -.6 * b, "y", fontsize=14)

    plt.axis("off")
    plt.savefig("./images/plot_I", bbox_inches='tight', pad_inches=0.1)
    plt.close()
    
#============================= Func plot hình C #=============================

def plot_C(Qy, h, b, d, t):
    # PLOT CROSS-SECTION AND STRESS DESCRIPTION
    h, b, d, t = float(h)/10, float(b)/10, float(d)/10, float(t)/10
    
    plt.subplot(2, 1, 1)
    x_vertical = [0, 0, b, b, d, d]
    y_vertical = [0, h / 2, h / 2, (h - 2 * t) / 2, (h - 2 * t) / 2, 0]

    # Plot the original shape
    plt.plot(x_vertical, y_vertical, color="black")

    # Mirror the rectangular shape about the y-axis
    mirrored_y_vertical = [-yi for yi in y_vertical]  # Reverse the sign of each y-coordinate
    plt.plot(x_vertical, mirrored_y_vertical, color="black")
    x_st = [2 * b, 3 * b, 3 * b, 4 * b, 2 * b]
    y_st = [h / 2, h / 2, -h / 2, -h / 2, h / 2]

    if Qy > 0:
        plt.plot(x_st, y_st)
        plt.text(2.35 * b, 0.35 * h, fr"$\sigma_{{min}}$={-sigmamax}", fontsize=14)
        plt.text(3.1 * b, -0.45 * h, fr"$\sigma_{{max}}$={sigmamax}", fontsize=14)
    else:
        mirrored_y_st = [-yi for yi in y_st]
        plt.plot(x_st, mirrored_y_st)
        plt.text(2.35 * b, -0.45 * h, fr"$\sigma_{{min}}$={-sigmamax}", fontsize=14)
        plt.text(3.05 * b, 0.35 * h, fr"$\sigma_{{max}}$={sigmamax}", fontsize=14)

    theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
    radius = h / 2
    x_t = 5 * b + radius * np.cos(theta)
    y_t = radius * np.sin(theta)
    plt.plot(x_t, y_t)
    plt.plot([5 * b, 5 * b], [-h / 2, h / 2])
    plt.text(5 * b + radius, -.1 * h, fr"$\tau_{{max}}$={abs(taumax)}", fontsize=14)

    plt.plot([b / 2, 5 * b + 1.2 * radius], [0, 0], color='black', linestyle='-')
    plt.plot([b / 2, b / 2], [0, -.6 * h], color='black', linestyle='-')
    plt.text(5 * b + 1.2 * radius, .05 * h, 'x', fontsize=14)
    plt.text(.6 * b, -.6 * h, 'y', fontsize=14)

    # Set aspect ratio to be equal
    plt.axis("off")
    plt.axis("equal")
    plt.title("C-SHAPE CROSS-SECTION")

    plt.subplot(2, 1, 2)
    x_horizontal = [0, h, h, h - t, h - t, t, t, 0, 0]
    y_horizontal = [b / 2, b / 2, -b / 2, -b / 2, b / 2 - d, b / 2 - d, -b / 2, -b / 2, b / 2]
    plt.plot(x_horizontal, y_horizontal, color='black')

    step = h + b
    x_st = [step, step + b, step + b, step + 2 * b, step]
    y_st = [b / 2, b / 2, -b / 2, -b / 2, b / 2]

    if Qy > 0:
        plt.plot(x_st, y_st)
        plt.text(step + .35 * b, 0.35 * b, fr"$\sigma_{{min}}$={-sigmatd}", fontsize=14)
        plt.text(step + 1.15 * b, -0.45 * b, fr"$\sigma_{{max}}$={sigmatd}", fontsize=14)
    else:
        mirrored_y_st = [-yi for yi in y_st]
        plt.plot(x_st, mirrored_y_st)
        plt.text(step + .35 * b, -0.45 * b, fr"$\sigma_{{min}}$={-sigmatd}", fontsize=14)
        plt.text(step + 1.05 * b, 0.35 * b, fr"$\sigma_{{max}}$={sigmatd}", fontsize=14)

    theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
    radius = b / 2
    x_t = step + 3 * b + radius * np.cos(theta)
    y_t = radius * np.sin(theta)
    plt.plot(x_t, y_t)
    plt.plot([step + 3 * b, step + 3 * b], [-b / 2, b / 2])
    plt.text(step + 3 * b + radius, -.1 * b, fr"$\tau_{{max}}$={abs(taumax)}", fontsize=14)

    plt.plot([h / 2, step + 3.7 * b], [0, 0], color="black", linestyle="-")
    plt.plot([h / 2, h / 2], [0, -.6 * b], color="black", linestyle="-")
    plt.text(step + 3.7 * b, .02 * b, "x", fontsize=14)
    plt.text(.52 * h, -.6 * b, "y", fontsize=14)

    plt.axis("off")
    plt.savefig("./images/plot_C", bbox_inches='tight', pad_inches=0.1)
    plt.close()
