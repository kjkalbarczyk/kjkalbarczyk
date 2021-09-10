# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:32:11 2020

@author: Lenovo
"""
#Karolina Kalbarczyk 283853
X=[4,5,6,18,16,20,28, 8128, 33550336, 44,6] #podaję listę liczb
def doskonala(X): #definiuję funkcję sprawdzającą czy liczba jest doskonała
    suma=0 
    true=[]
    for j in X: #nazywam liczbę w liscie "j"
        for i in range(j-1):
            if(j%(i+1)==0): #jesli liczba wpisana j dzieli się przez i+1 bez reszty, to mamy dzielnik i dopisujemy go do sumy
                suma=suma+i+1       
        if (suma==j): #jesli suma dzielnikow jest rowna j to jest liczba doskonala
                true.append(True) #dla liczb doskonałych przyjmuę wartosc True
        else:
                true.append(False) #dla liczb niedoskonałych przyjmuję wartosc False
                
        suma=0
    return(true)
t=doskonala(X)
print(t) #drukuje liste


