import numpy as np
from numpy import sin, cos, arctan2
from itertools import cycle
from sys import argv, exit
import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui

class InvertedPendulum(QtGui.QWidget):
    '''Inicjalizacja stałych:
    M - masa wózka
    m - masa kulki
    l - długość ramienia wahadła

    Warunków początkowych:
    x0 - początkowe położenie wózka
    dx0 - początkowa prędkość wózka
    theta0 - początkowe położenie wahadla
    dtheta0 - początkowa prędkość wahadła

    Zakłócenia zewnętrznego:
    dis_cyc - zmienna odpowiada za to, czy zakłócenie jest zapętlone
    disruption - wartości zakłócenia w kolejnych chwilach czasowych

    Parametry planszy/obrazka:
    iw, ih - szerokość i wysokość obrazka
    x_max - maksymalna współrzędna pozioma (oś x jest symetryczna, więc minimalna wynosi -x_max)
    h_min - minialna współrzędna pionowa
    h_max - maksymalna współrzędna pionowa

    Powyższe dane są pobierane z pliku jeśli zmienna f_name nie jest pusta'''
    def __init__(self, M=10, m=5, l=50, x0=0, theta0=0, dx0=0, dtheta0=0, dis_cyc=True, disruption=[0], iw=1000, ih=500, x_max=100, h_min=0, h_max=100, f_name=None):
        if f_name:
            with open(f_name) as f_handle:
                lines = f_handle.readlines()
                init_cond = lines[0].split(' ')
                self.M, self.m, self.l, self.x0, self.theta0, self.dx0, self.dtheta0 = [float(el) for el in init_cond[:7]]
                self.image_w, self.image_h, self.x_max, self.h_min, self.h_max = [int(el) for el in init_cond[-5:]]
                if lines[1]:
                    self.disruption = cycle([float(el) for el in lines[2].split(' ')])
                else:
                    self.disruption = iter([float(el) for el in lines[2].split(' ')])
        else:
            self.M, self.m, self.l, self.x0, self.theta0, self.dx0, self.dtheta0 = M, m, l, x0, theta0, dx0, dtheta0
            self.image_w, self.image_h, self.x_max, self.h_min, self.h_max = iw, ih, x_max, h_min, h_max
            if dis_cyc:
                self.disruption = cycle(disruption)
            else:
                self.disruption = iter(disruption)
        super(InvertedPendulum, self).__init__(parent=None)

    # Inicjalizacja obrazka
    def init_image(self):
        self.h_scale = self.image_h/(self.h_max-self.h_min)
        self.x_scale = self.image_w/(2*self.x_max)
        self.hor = (self.h_max-10)*self.h_scale
        self.c_w = 16*self.x_scale
        self.c_h = 8*self.h_scale
        self.r = 8
        self.x = self.x0
        self.theta = self.theta0
        self.dx = self.dx0
        self.dtheta = self.dtheta0
        self.setFixedSize(self.image_w, self.image_h)
        self.show()
        self.setWindowTitle("Inverted Pendulum")
        self.update()

    # Rysowanie wahadła i miarki
    def paintEvent(self, e):
        x, x_max, x_scale, theta = self.x, self.x_max, self.x_scale, self.theta
        hor, l, h_scale = self.hor, self.l, self.h_scale
        image_w, c_w, c_h, r, image_h, h_max, h_min = self.image_w, self.c_w, self.c_h, self.r, self.image_h, self.h_max, self.h_min
        painter = QtGui.QPainter(self)
        painter.setPen(pg.mkPen('k', width=2.0*self.h_scale))
        painter.drawLine(0, hor, image_w, hor)
        painter.setPen(pg.mkPen((165, 42, 42), width=2.0*self.x_scale))
        painter.drawLine(x_scale*(x+x_max), hor, x_scale*(x+x_max-l*sin(theta)), hor-h_scale*(l*cos(theta)))
        painter.setPen(pg.mkPen('b'))
        painter.setBrush(pg.mkBrush('b'))
        painter.drawRect(x_scale*(x+x_max)-c_w/2, hor-c_h/2, c_w, c_h)
        painter.setPen(pg.mkPen('r'))
        painter.setBrush(pg.mkBrush('r'))
        painter.drawEllipse(x_scale*(x+x_max-l*sin(theta)-r/2), hor-h_scale*(l*cos(theta)+r/2), r*x_scale, r*h_scale)
        painter.setPen(pg.mkPen('k'))
        for i in np.arange(-x_max, x_max, x_max/10):
            painter.drawText((i+x_max)*x_scale, image_h-10, str(int(i)))
        for i in np.arange(h_min, h_max, (h_max-h_min)/10):
            painter.drawText(0, image_h-(int(i)-h_min)*h_scale, str(int(i)))

    # Rozwiązanie równań mechaniki wahadła
    def solve_equation(self, F):
        l, m, M = self.l, self.m, self.M
        g = 9.81
        a11 = M+m
        a12 = -m*l*cos(self.theta)
        b1 = F-m*l*self.dtheta**2*sin(self.theta)
        a21 = -cos(self.theta)
        a22 = l
        b2 = g*sin(self.theta)
        a = np.array([[a11, a12], [a21, a22]])
        b = np.array([b1, b2])
        sol = np.linalg.solve(a, b)
        return sol[0], sol[1]

    # Scałkowanie numeryczne przyśpieszenia, żeby uzyskać pozostałe parametry układu
    def count_state_params(self, F, dt=0.001):
        ddx, ddtheta = self.solve_equation(F)
        self.dx += ddx*dt
        self.x += self.dx*dt
        self.dtheta += ddtheta*dt
        self.theta += self.dtheta*dt
        self.theta = arctan2(sin(self.theta), cos(self.theta))

    # Uruchomienie symulacji
    # Zmienna sandbox mówi o tym, czy symulacja ma zostać przerwana w przypadku nieudanego sterowania -
    # - to znaczy takiego, które pozwoliło na zbyt duże wychylenia iksa lub na zbyt poziomo położenie wahadła
    def run(self, sandbox, frameskip=20):
        self.sandbox = sandbox
        self.frameskip = frameskip
        self.init_image()
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.single_loop_run)
        timer.start(1)

    # n - krotne obliczenie następnego stanu układu
    # Gdzie n - to frameskip
    def single_loop_run(self):
        for i in range(self.frameskip+1):
            dis=next(self.disruption, 0)
            control = self.fuzzy_control(self.x, self.theta, self.dx, self.dtheta)
            F = dis+control
            self.count_state_params(F)
            if not self.sandbox:
                if self.x < -self.x_max or self.x > self.x_max or np.abs(self.theta) > np.pi/3:
                    exit(1)
        self.update()
        
     # Regulator rozmyty, który trzeba zaimplementować
    #funckje AND OR NOT
    def AND(self, mu1,mu2):
        return(min(mu1,mu2))
    def NOT(self,mu):
        return(1-mu)
    def OR(self,mu1,mu2 ):
        return(max(mu1,mu2))
    #rozmywanie
    def TN(self, theta,thetamax=np.pi/90): #Rozmycie theta negative (odchylanie w prawo)
        mu=0.000000000001
        if theta < 0 and theta>-thetamax: 
            mu=-1/thetamax*theta #opis wykresu (mu jest równe spadkowi liniowemu w tym obszarze)
        if theta<-thetamax: #dla zakresu mniejszego od thetamax mamy mu=1
            mu=1
        return(mu)
    def TP(self, theta,thetamax=np.pi/90): #Rozmycie theta positive (odchylanie w lewo)
        mu=0.0000000000001
        if theta > 0 and theta<thetamax:
            mu=1/thetamax*theta
        if theta>thetamax:
            mu=1
        return(mu)    
    def DTN(self, dtheta,dthetamax=10000): #Rozmycie dtheta negative (odchylanie w prawo)
        mu=0.0000000000001
        if dtheta < 0 and dtheta>-dthetamax:
            mu=-1/dthetamax*dtheta
        if dtheta<-dthetamax:
            mu=1
        return(mu)
    def DTP(self, dtheta,dthetamax=10000): #Rozmycie dtheta positive (odchylanie w lewo)
        mu=0.000000000001
        if dtheta > 0 and dtheta<dthetamax:
            mu=1/dthetamax*dtheta
        if dtheta>dthetamax:
            mu=1
        return(mu)    
    def XP(self, x,xmax=20): #Rozmycie x positive (odjazd w prawo) ##to jest aktualnie zbędne ale zostawiłam, żeby bylo widac ze kiedys probowalam wiecej :)
        mu=0.00000000001
        if x < xmax and x>0:
            mu=1/xmax*x
        if x>xmax:
            mu=1
        return(mu)
    def XN(self, x,xmax=20): #Rozmycie x negative (odjazd w lewo)
        mu=0.000000001
        if x > -xmax and x<0:
            mu=-1/xmax*x
        if x<-xmax:
            mu=1
        return(mu) 
    def FP(self,f,fmax=100): #rozmycie FP
        mu=0.0000000001
        if f < fmax and f>0:
            mu=1/fmax*f
        if f>fmax:
            mu=1
        return(mu)        
    def FN(self,f,fmax=100):#rozmycie FN
        mu=0
        if f > -fmax and f<0:
            mu=-1/fmax*f
        if f<-fmax:
            mu=1
        return(mu)  
    #reguły
    def R1(self, theta, dtheta):#obcina negatywną siłę
       return(self.OR(self.TP(theta), self.DTP(dtheta)) )
    def R2(self, theta, dtheta):#obcina pozytywna siłe 
       return(self.OR(self.TN(theta),self.DTN(dtheta)))  
   #wyostrzanie
    def FPW(self,f,fmax,mumax): #zmiana granic mu siły positive na te które wynikają z reguł
        mu=0
        if f < fmax and f>0:
            mu=mumax/fmax*f
        if f>fmax:
            mu=mumax
        return(mu)        
    def FNW(self,f,fmax,mumax):#zmiana granic mu siły negative na te które wynikają z reguł
        mu=0
        if f > -fmax and f<0:
            mu=-mumax/fmax*f
        if f<-fmax:
            mu=mumax
        return(mu)  
   
    def combine(self,F,fmax,mumax1,mumax2): #przeniesienie obu wykresów siły na jeden
        return(self.FPW(F,fmax,mumax2)+self.FNW(F,fmax,mumax1))
    
    def FMassCenter(self,fmax,mumax1,mumax2): #obliczenie mass center na zasadzie metody srodka obszaru 
        F=np.arange(start=-300, stop=300, step=10) #okreslenie granic przedzialu sumy (rownoczesnie granic wielkosci sily)
        M=np.zeros(60)
        for i in range(60):
            M[i]=self.combine(F[i],fmax,mumax1,mumax2) #polaczenie dwoch wykresow sil
        return(np.sum(F*np.abs(M))/np.sum(np.abs(M))) #zwraca srodek masy
    
    def fuzzy_control(self, x, theta, dx, dtheta, fmax=100): 
        return(self.FMassCenter(fmax,self.R1( dtheta,theta),self.R2(  dtheta,theta)))#sila

if __name__ == '__main__':
    app = QtGui.QApplication(argv)
    if len(argv)>1:
        ip = InvertedPendulum(f_name=argv[1])
    else:
        ip = InvertedPendulum(x0=90, dx0=0, theta0=0, dtheta0=0.1, ih=800, iw=1000, h_min=-80, h_max=80)
    ip.run(sandbox=False)
    exit(app.exec_())
