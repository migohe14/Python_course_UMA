def datos_por_pais(coleccion, pais):
    x=[] #Dias
    y=[] #Casos cada dia
    acumulado=[] #Suma de todos los dias en ese periodo
    suma=0
    dia=1
    datos=coleccion.find({"geoId":pais,"month":{"$gte": 3, "$lte": 12}},
        {"_id":0,"cases":1,"day":1,"month":1,"dateRep":1}).sort([("month",1),("day",1)])
    
    for p in datos:
        y.append(p["cases"])
        x.append(dia)
        suma+=p["cases"]
        acumulado.append(suma)
        dia+=1

    return x,y,acumulado