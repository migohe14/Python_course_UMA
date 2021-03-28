from pymongo import MongoClient
import pymongo
import matplotlib.pyplot as plt 
from datos_pais import *



cliente=MongoClient()
db=cliente.Corona
todo=db.paises.find()

#Ejercicio 1
#for dato in todo:
#    print(dato)

#Ejercicio 2:
print("Datos de España en Marzo")
datosespana=db.paises.find({"geoId": "ES", "month": 3}, {"_id": 0})

for dia in datosespana:
    print(dia)

#Ejercicio 3:
x,y,a=datos_por_pais(db.paises, "ES")
plt.plot(x,y,'r',x,a,'r--')

#Ejercicio 4:
x1,y1,a1=datos_por_pais(db.paises, "IT")
plt.plot(x1,y1,'b',x1,a1,'b--')
x1,y1,a1=datos_por_pais(db.paises, "DE")
plt.plot(x1,y1,'y',x1,a1,'y--')
x1,y1,a1=datos_por_pais(db.paises, "FR")
plt.plot(x1,y1,'o',x1,a1,'o--')
plt.show()

#Ejercicio 5:

print("Ejercicio 5")
grupo=db.paises.aggregate([{"$group": {"_id": "$geoId", "cuantos": {"$sum": 1}}}])

for g in grupo:
    print(g)

#Ejercicio 6:
print("Ejercicio 6")
grupo=db.paises.aggregate([{"$group":{"_id":"$geoId", "total":{"$sum":"$cases"}}},{"$sort":{"total":1}}])

for g in grupo:
    print(g)

#Ejercicio 7:
print("Ejercicio 7")
grupo=db.paises.aggregate([{"$match":{"geoId":{"$in": ["ES","IT","FR","DE"]}}},
    {"$group":{"_id": "$geoId", "total": {"$sum": "$cases"}}},
    {"$sort": {"total":1}}])

for g in grupo:
    print(g)