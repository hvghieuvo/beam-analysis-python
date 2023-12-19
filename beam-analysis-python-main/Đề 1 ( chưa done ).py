import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
P1 = float(input('Nhap luc cat P1 ='))
P2 = float(input('Nhap luc cat P2 ='))
P3 = float(input('Nhap luc cat P3 ='))
P4 = float(input('Nhap luc doc truc P4 ='))
q1 = float(input('Nhap luc phan bo deu q1 ='))
q2 = float(input('Nhap luc phan bo deu q2 ='))
q3 = float(input('Nhap luc phan bo deu q3 ='))
M1 = float(input('Nhap moment tap trung M1 = '))
M2 = float(input('Nhap moment tap trung M2 = '))
M3 = float(input('Nhap moment tap trung M3 = '))
AB = float(input('Nhap chieu dai doan AB = '))
BC = float(input('Nhap chieu dai doan BC = '))
CD = float(input('Nhap chieu dai doan CD = '))

print('Quy Ước Chiều (+) từ dưới lên trên, từ trái sang phải, CCW')

#P2 mac dinh huong ra ngoai


def console():
    AD=AB+BC+CD
    Q1 = q1*AB
    Q2 = q2*BC
    Q3 = q3*CD
    Py_total = P1+P2+P3
    Qy_total = Q1+Q2+Q3
    M_total = M1+M2+M3

    #CAL REACTIONS:
    # P4 duong (trai->phai)
    Ax = -P4 #Ax am (phai->trai)/ Ax duong(trai->phai)
    print('Ax =', Ax)
    Ay = -Qy_total - Py_total #Duong huong len / Am huong xuong
    print('Ay = ', Ay)

    #CAL MOMENT:
    Ma = -( (Q1*AB/2)+(P1*AB)+(Q2*(AB+BC/2))+P2*(AB+BC)+Q3*(AB+BC+CD/2)+(P3*AD)+M1+M2+M3 )
    MD = M3
    MC = M3+P3*CD+Q3*CD/2+M2
    MB = M3+P3*(BC+CD)+Q3*(BC+CD/2)+P2*BC+Q2*BC/2+M1
    MA = M3+P3*AD+Q3*(AB+BC+CD/2)+M2+P2*(AB+BC)+Q2*(AB+BC/2)+M1+P1*AB+Q1*AB/2+Ma
    print('Ma,MD,MC,MB,MA = ',Ma,MD,MC,MB,MA)

    #CREATE A QUADRATIC EQUATION ACCORDING M AND L
    L1 = np.linspace(0,AB,1000)
    Mx1 = q1/2*(L1**2) +Ay*L1 -Ma
    L2 = np.linspace(0,BC,1000)
    Mx2 = q2/2*(L2**2) +(Ay+P1+Q1)*L2 + Q1*AB/2 +Ay*AB -Ma-M1
    L3 = np.linspace(0,CD,1000)
    Mx3 = q3/2*(L3**2) + (Q1+Q2+Ay+P1+P2)*L3 + (Q2/2 +Q1+Ay+P1)*BC + (Q1/2 +Ay)*AB -M1-M2-Ma


    #PLOT AXIAL FORCES NZ:
    plt.subplot(3, 1, 1)
    plt.plot([0, 0, AD, AD, 0], [0, P4, P4, 0, 0])
    plt.title('Axial Forces')
    distance = np.arange(0, AD, 0.01)
    plt.fill_between(distance,P4,color='red', alpha=0.5, hatch='//')
    plt.text(AD, P4, f"{float(P4)}", fontsize=14)
    plt.text(0, P4, f"{float(P4)}", fontsize=14)
    plt.text(0, 0, f"{0}", fontsize=14), plt.text(AD, 0, f"{0}", fontsize=14)
    plt.axis('off')

    #PLOT SHEAR FORCES QY:
    plt.subplot(3, 1, 2)
    plt.plot([0, 0, AB, AB, AB + BC, AB + BC, AD, AD, 0],
             [0, Ay, Ay + Q1, Ay + Q1 + P1, Ay + Q1 + P1 + Q2, Ay + Q1 + P1 + Q2 + P2, Ay + Q1 + P1 + Q2 + P2 + Q3,
              Ay + Q1 + P1 + Q2 + P2 + Q3 + P3, 0])
    plt.xlim([-.1, AD + .1])
    plt.title('Shear Forces')
    plt.text(0, 0, "0", fontsize=14)
    plt.text(0, Ay, f"{float(Ay)}", fontsize=14)
    plt.text(AB, Ay+Q1, f"{float(Ay+Q1)}", fontsize=14)
    plt.text(AB, Ay+Q1+P1, f"{float(Ay+Q1+P1)}", fontsize=14)
    plt.text(AB+BC, Ay+Q1+P1+Q2, f"{float(Ay+Q1+P1+Q2)}", fontsize=14)
    plt.text(AB+BC, Ay+Q1+P1+Q2+P2, f"{float(Ay+Q1+P1+Q2+P2)}", fontsize=14)
    plt.text(AD, Ay+Q1+P1+Q2+P2+Q3, f"{float(Ay+Q1+P1+Q2+P2+Q3)}", fontsize=14)
    plt.text(AD, Ay+Q1+P1+Q2+P2+Q3+P3, f"{float(Ay+Q1+P1+Q2+P2+Q3+P3)}", fontsize=14)
    plt.axis('off')

    #PLOT BENDING MOMENT MZ:
    plt.subplot(3,1,3)
    plt.plot([0,0,AD,AD], [-Ma,0,0,MD])
    plt.plot(L1, Mx1)
    plt.plot(L2 + AB, Mx2)
    plt.plot(L3+AB+BC, Mx3)
    plt.xlim([-.1, AD + .1])
    plt.title('Bending Moment')
    plt.text(0, 0, "0", fontsize=14)
    plt.text(0, -Ma, f"{float(-Ma)}", fontsize=14)
    plt.text(AB, MB, f"{float(MB)}", fontsize=14)
    plt.text(AB+BC, MC, f"{float(MC)}", fontsize=14)
    plt.text(AD, MD, f"{float(MD)}", fontsize=14)
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.show()
console()
