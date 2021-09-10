#Karolina Kalbarczyk 283853
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import tree
xls_file = pd.ExcelFile('pd4.xlsx')
test_target=pd.DataFrame()
xls_file
print(xls_file.sheet_names)#sprawdzenie nazw arkuszy w pli xls
df= xls_file.parse('Arkusz1')#załadowanie danych z Arkusza 1 do dataframe
df=df[['p7','p9','wynik']]#stworzenie dataframe z korzystnymi parametrami
df=df[df.p7!=-1]
df=df[df.p9!=-1]#usunięcie wartosci -1
print(df)
data=df[['p7','p9']]#tworzene df potrzebnych do uczenia
target=df[['wynik']]
train_target=target.drop([target.index[1], target.index[6], target.index[17]])
train_data = data.drop([data.index[1],data.index[6],data.index[17]])
test_target=[target.wynik[1],target.wynik[6],target.wynik[17]]
test_data = [[data.p7[1],data.p9[1]],[data.p7[6],data.p9[6]],[data.p7[17],data.p9[17]]]
drzewo = tree.DecisionTreeClassifier()
drzewo.fit(train_data,train_target)

print('dokładnosc drzewa wynosi:')
print('{} %'.format((accuracy_score(test_target,drzewo.predict(test_data)))*100))
print('Macierz bledu tej metody:')
print(confusion_matrix(test_target, drzewo.predict(test_data)))

d= data
t= target
d_train, d_test, t_train, t_test = train_test_split(d, t, test_size = .5)
neighbor = KNeighborsClassifier()
neighbor.fit(d_train,t_train)
przewidywania = neighbor.predict(d_test)
print('Dokladnosc KNeighborsClassifier:')
print('{:.2f} %'.format((accuracy_score(t_test,przewidywania))*100))
print('Macierz bledu tej metody:')
print(confusion_matrix(t_test, przewidywania))


randomf = RandomForestClassifier(max_depth=2, random_state=0)
randomf.fit(d_train,t_train)
przewidywania = randomf.predict(d_test)
print('Dokladnosc RandomForestClassifier:')
print('{:.2f} %'.format((accuracy_score(t_test,przewidywania))*100))
print('Macierz bledu tej metody:')
print(confusion_matrix(t_test, przewidywania))