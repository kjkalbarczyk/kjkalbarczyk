#Karolina Kalbarczyk 283853
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
xls_file = pd.ExcelFile('pd4.xlsx')
xls_file
print(xls_file.sheet_names)#sprawdzenie nazw arkuszy w pli xls
df= xls_file.parse('Arkusz1')#załadowanie danych z Arkusza 1 do dataframe
L0=[]#dodatkowe listy
L1=[]
L2=[]
L3=[]
L4=[]
L5=[]
L6=[]
L7=[]
for i in range(0,11):
    df = xls_file.parse('Arkusz1')
    df=df[df.p1!=-1]#usunięcie wartosci -1 z pierwszej kolumny
    chorzy=df[df.wynik==1] #stworzenie nowych dataframe z podziałem na zdrowych i chorych
    zdrowi=df[df.wynik!=1]  
    chorzy=chorzy[chorzy['p'+str(i+1)]!=-1]#usunięcie wartosci -1 z pozostałych kolumny
    zdrowi=zdrowi[zdrowi['p'+str(i+1)]!=-1]
    plt.scatter(chorzy['p1'],chorzy['p'+str(i+1)],color='red', label='chorzy')#stworzenie wykresów z odpowiednio chorymi na czerwono i zdrowymi na niebiesko
    plt.scatter(zdrowi['p1'],zdrowi['p'+str(i+1)],color='blue',label='zdrowi')
    plt.grid(True)#kratka za wykresem
    plt.xlabel('p1')#opisanie osi
    plt.ylabel('p'+str(i+1))
    plt.legend()#wyswietlenie legendy
    plt.title('wykres p'+str(i+1)+'(p1)')#dodanie tytułu do wykresu
    plt.savefig('p'+str(i+1)+'.png')#zapisanie wykresów jako png
    plt.show()#wyswietlenie wykresów w konsoli
    L0.append('p'+str(i+1)) #tworzenie list z wariancjami i wartosciami oczekiwanymi
    L1.append(df.loc[:,'p'+str(i+1)].var())
    L2.append(df.loc[:,'p'+str(i+1)].mean())
    L3.append(zdrowi.loc[:,'p'+str(i+1)].var())
    L4.append(chorzy.loc[:,'p'+str(i+1)].var())
    L5.append(zdrowi.loc[:,'p'+str(i+1)].mean())
    L6.append(chorzy.loc[:,'p'+str(i+1)].mean())
data=[L0,L1,L2,L3,L4,L5,L6] #wpisanie wszystkich list w jeden dataframe
wyniki=pd.DataFrame(data,columns=['p1','p2','p3','p4','p5','p6','p7','p8','p9','p10','p11'],index=['Parametr/Obliczenia','Var(p)','Wartosc oczekiwana(p)','Var(zdrowi)','Var(chorzy', 'Wartosc oczekiwana(zdrowi)','Wartosc oczekiwana(chorzy)'])
wyniki=wyniki.T #macierz transponowana

for i in range(1,11):
    df=df[df.p1!=-1]
    df=df[df['p'+str(i+1)]!=-1]
pearsoncorr=df.corr(method='pearson')#pearson method
sb.heatmap(pearsoncorr,xticklabels=pearsoncorr.columns, yticklabels=pearsoncorr.columns,cmap='RdBu_r',annot=True,linewidth=0.5)

with pd.ExcelWriter('Wyniki.xlsx') as writer:   #zapisanie wyników do excela
    pearsoncorr.to_excel(writer, sheet_name='Pearson')
    wyniki.to_excel(writer, sheet_name='Statystyka')


