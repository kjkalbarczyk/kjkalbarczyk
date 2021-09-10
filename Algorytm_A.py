
import numpy as np
import matplotlib.pyplot as plt
import sys

def ploting(): #dodatkowa funkcja do rysowania wykresu dla łatwej wizualizacji problemu
    plt.scatter(xw,yw)
    for i in range(len(wagiwagi[0])):
        for j in range(len(wagiwagi[0])):
            if (wagiwagi[i][j])!=0:
                plt.plot([xw[i],xw[j]],[yw[i],yw[j]],color="blue", linewidth=2)
                plt.annotate(i+1, # podpisywanie punktów ich numerami
                 (xw[i],yw[i]), 
                 textcoords="offset points", # 
                 xytext=(10,10), # sprawienie żeby etykiety były w offsecie, żeby były lepiej widoczne
                 ha='center') # od czego offset
    #return(plt.show())
                
def heurystyka(wierzcholki,y1,x2,y2): #funckja do liczenia długosci odcinka
    return(np.sqrt((x2-wierzcholki)**2+(y2-y1)**2))

def heurystykalista(): #funkcja wyznaczajaca heurystyke dla kazdego punktu
    heur=[]
    for i in range(len(xw)):
        heur.append(heurystyka(xw[i],yw[i],xw[meta-1],yw[meta-1]))
    return heur

def sasiedzi(numer): #funkcja znajdująca wszystkich sasiadow dla danego punktu
    n=[]
    for i in range(len(xw)):
        if (wagiwagi[numer-1][i])!=0: #jesli istnieje value, to znaczy ze mamy sasiada)
            n.append(i+1)
    return(n)

def OddajTrase():      #funcja wypisujaca znaleziona trase 
    global keys
    b=''    
    a=meta
    values = [ v for v in Poprzedniki.values() ]
    keys = [ v for v in Poprzedniki.keys() ]    
    if not (meta in keys):
        b='brak trasy'
    else:
        for i in keys:
            if a==start:break
            trasa.append(a) 
            a=values[keys.index(a)]
        trasa.append(start)        
        trasa.reverse()
        for item in trasa:    
            b=b+str(item)+' '
    return(print(b))

def Algorytm(): #algorytm
    global Poprzedniki
    KosztRozpatrywane={} #jest to dodatkowy slownik ktory pomaga znalezc minimum KosztuTrasy (czyli minimalne f)
    heur=heurystykalista() #lista heurystyk dla wszystkich punktow
    aktualnypkt=start #to bedzie punkt ktory rozpatrujemy w programie - na poczatku start
    Poprzedniki={} #slownik poprzednikow
    Rozpatrywane=[start] #lista rozpatrywanych punktow (do rozpatrzenia tak naprawde, rozpatrujemy aktualnypkt ktory ma najmniejsze f z nich)
    PrzebytaDroga={} #zapis drogi w slowniku czyli g
    KosztTrasy={}   #zapis kosztu trasy czyli f
    TymczasowaPrzebytaDroga=0 #pomocna zmienna do sprawdzenia czy gtemp<g
    for  i in range(len(xw)): #odpowiednie przygotowanie slownikow (zapelnienie infinity)
        PrzebytaDroga[i+1]=inf
        KosztTrasy[i+1]=inf
    PrzebytaDroga[start]=0
    KosztTrasy[start]=heur[start-1]
    
    while Rozpatrywane!=[]: #zewnetrzna petla algorytmu
        for i in Rozpatrywane: 
            KosztRozpatrywane[i]=KosztTrasy[i]
        klucze_KR=list(KosztRozpatrywane.keys()) #lista kluczy ze slownika KosztRozpatrywane
        wartosci_KR=list(KosztRozpatrywane.values()) #lista wartosci ze slownika KosztRozpatrywane
        p=min(KosztRozpatrywane.values()) #znalezienie minimalnej wartosci
        aktualnypkt=klucze_KR[wartosci_KR.index(p)] #przypisanie do aktualny punkt klucza ktory opisuje minimalna wartosc
        KosztRozpatrywane={}
        Rozpatrywane.remove(aktualnypkt)
        if aktualnypkt==meta:  #koniec programu
           # OddajTrase()
            Rozpatrywane=[]
            break
        else:   #jesli jeszcze nie doszlismy do mety to sprawdz sasiadow naszego pkt
            for i in sasiedzi(aktualnypkt): 
                TymczasowaPrzebytaDroga=PrzebytaDroga[aktualnypkt]+wagiwagi[aktualnypkt-1][i-1] #zapisz tymczasowe g
                if TymczasowaPrzebytaDroga<PrzebytaDroga[i]: #jesli tymczasowe g<g to
                    PrzebytaDroga[i]=TymczasowaPrzebytaDroga
                    Poprzedniki[i]=aktualnypkt
                    KosztTrasy[i]=PrzebytaDroga[i]+heur[i-1]
                    if not i in Rozpatrywane:
                        Rozpatrywane.append(i)
    OddajTrase()
    return()

trasa=[]
wierzcholki=[] #lista wierzcholkow
xw=[] #lista wspolrzednych x wierzcholkow
yw=[] #lista wspolrzednych y wierzcholkow
k='' #pomocne zmienne string
o=''
m=''
q=[] #pomocne listy
wagi=[]
path=[]
wagiwagi=[]  #macierz sasiedztwa
inf=2**20
if len(sys.argv)>1 and sys.argv[1]!='':
    file=open(sys.argv[1])
else:
    file=open("1.txt", "r") #otwieram plik
content=file.readlines() #ładuje zawartosc pliku do content wierszami

temp_wierzch=str(content[0]) #obrabiam pierwszy wers pliku wejsciowego tak aby nie mial innych znakow niz spacje i liczby
temp_wierzch=temp_wierzch.rstrip()
temp_wierzch=temp_wierzch.replace('(','')
temp_wierzch=temp_wierzch.replace(')','')
temp_wierzch=temp_wierzch.replace(',','')

for i in temp_wierzch: #tworzenie listy oddzielajacej spacja kolejne wierzcholki ale bez spacji
    if i!= ' ':
        k+=i
    else:
        wierzcholki.append(k)
        k=''
wierzcholki.append(k)

pres=str(content[1].rstrip())  #pomocnicza lista zawartosci drugiego wiersza - drogi
for i in pres: #wartosc mety i startu jak dla wierzcholkow
    if i!= ' ':
        m+=i
    else:
        path.append(m)
        m=''
path.append(m)
meta=int(path[1])
start=int(path[0])

for i in range(int(len(wierzcholki)/2)):  #tworzę listy oddzielnych współrzędnych x i y
   xw.append(int(wierzcholki[2*i]))
   yw.append(int(wierzcholki[2*i+1]))

for j in range(len(xw)): #tak jak dla wierzcholkow obrabiam macierz sasiedztwa
    temp_wagi=(str(content[j+2]).rstrip())
    for i in temp_wagi:
        if i!= ' ':
            o+=i
        else:
            
            if o!='':
                q.append(o)
                o=''
    q.append(o)
    o=''
    wagi.append(q)
    q=[]

for row in wagi:    
    wagiwagi.append([float(i) for i in row])

ploting()
Algorytm()
