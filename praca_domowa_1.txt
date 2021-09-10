# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Karolina Kalbarczyk 283853
par=0 #parzyste
x=1 #warunek na wpisywanie aż do wpisania 0
X=[] #lista X
while (x!=0): #warunek na wpisywanie aż do wpisania 0
    x=float(input("podaj liczbe: "))
    X.append(x) #dodawanie do listy nowego elementu (wpisywanego x)
    if(x%2==0): 
        par=par+x #naliczanie sumy liczb parzystych
print(X,'suma liczb parzystych:',par) 

