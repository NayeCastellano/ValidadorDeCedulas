


import csv #libreria para manejar archivos csv
import os
from itertools import groupby # Funcion para agrupar una lista segun un criterio 
from operator import itemgetter # Para acceder a elementos de una lista 
from django.conf import settings


provincias = [  # Creo un diccionario del numero con su provincia 
        { "codigo":"01" , "nombre":"Azuay", 'region':"Sierra" },
        { "codigo":"02" , "nombre":"Bolivar", 'region':"Sierra" },
        { "codigo":"03" , "nombre":"Cañar", 'region':"Sierra" },
        { "codigo":"04" , "nombre":"Carchi", "region":"Sierra" },
        { "codigo":"04" , "nombre":"Carchi", 'region':"Sierra" },
        { "codigo":"05" , "nombre":"Cotopaxi", 'region':"Sierra" },
        { "codigo":"06" , "nombre":"Chimborazo", 'region':"Sierra" },
        { "codigo":"07" , "nombre":"El Oro", 'region':"Costa" },
        { "codigo":"08" , "nombre":"Esmeraldas", 'region':"Costa" },
        { "codigo":"09" , "nombre":"Galapagos", 'region':"Insular" },
        { "codigo":"10" , "nombre":"Guayas", 'region':"Costa" },
        { "codigo":"11" , "nombre":"Imbabura", 'region':"Sierra" },
        { "codigo":"12" , "nombre"  :"Loja", 'region':"Sierra" },
        { "codigo":"13" , "nombre":"Los Rios", 'region':"Costa" },
        { "codigo":"14" , "nombre":"Manabi", 'region':"Costa" },
        { "codigo":"15" , "nombre":"Morona Santiago", 'region':"Amazonia" },
        { "codigo":"16" , "nombre":"Napo", 'region':"Amazonia" },
        { "codigo":"17" , "nombre":"Pichincha", 'region':"Sierra" },
        { "codigo":"18" , "nombre":"Santa Elena", 'region':"Costa" },
        { "codigo":"19" , "nombre":"Santo Domingo de los Tsachilas", 'region':"Costa" },
        { "codigo":"20" , "nombre":"Sucumbios", "region":"Amazonia" },
        { "codigo":"21" , "nombre":"Tungurahua", 'region':"Sierra" },
        { "codigo":"22" , "nombre":"Zamora Chinchipe", 'region':"Amazonia" },
        { "codigo":"23" , "nombre":"Pastaza", 'region':"Amazonia" },
        { "codigo":"24" , "nombre":"Orellana", 'region':"Amazonia" },
        { "codigo":"30" , "nombre":"Ecuatorianos en el Exterior", 'region':"Exterior" }

    ]
#Recibe la direccion del archivo y el caracter delimitador 
def importarCSV(direccionArchivo, delimiter): 
    try: #intenta capturar errores que puedan surgir durante el llamado del archivo
        ruta_archivo = os.path.join(settings.STATIC_ROOT, 'static', direccionArchivo) # Añadimos 'data' a la ruta
        print(f"Intentando abrir archivo en: {ruta_archivo}")
        with open(ruta_archivo, 'r', encoding = 'utf-8') as archivo:
            datos = [] #Matriz donde voy almacenar los datos 
            lector = csv.reader(archivo, delimiter=delimiter) #Lee la informacion como una lista
            for lista in lector: #Recorre el iterable e ingresa en la lista de datos
                datos.append(lista)
            return datos 
        
    except FileNotFoundError: # tipo de error cuando no se encuentre el archivo
        print('El archivo no existe')   
        return [] # En el caso que falle, retorna un array vacio      
                        
#Recibe el numero de la provincia y retorna el nombre como un string                  
def obtenerProvincia(numeroProvincia): 
    provinciaEncontrada= None 
    for provincia in provincias:
        if numeroProvincia == provincia["codigo"]:
            provinciaEncontrada = provincia
    return provinciaEncontrada # Retorna el nombre de la provincia

#Recibe la cedula y le valida
def validarCedula(cedula):
 #1. El número de dígitos debe tener 10 dígitos
    if(len(cedula) != 10 ):
        print("Debe contener 10 dígitos")
        return False
    
    #2. dígito provincia
    digitoProvincia = (cedula[:2])
    if (int(digitoProvincia)>24):
        if(int(digitoProvincia)!=30):
            print("Dígito provincia incorrecto")
            return False
    
    #3. Dígito persona
    digitoPersona = int(cedula[2])
    if(digitoPersona)>6:
        print("Tercer dígito no valido para cédulas ecuatorianas")
        return False
    
    #validacion digito verficador
    sumaPar = 0
    sumaImpar = 0 
    for indice, digito in enumerate(cedula):
        if indice < 9:
            if indice % 2 != 0: # IMPAR
                sumaImpar=sumaImpar+int(digito)
                  
            else: # PAR
                mult = int(digito)*2
                restar=0
                if mult >= 10:
                    restar= mult-9
                else:
                    restar = mult
                sumaPar = sumaPar+restar
 
    # 4. Redondea al multiplo de 10 mas cercano 
    sumaTotal=sumaImpar+sumaPar
    redondeo=(sumaTotal + 9 )//10 *10
    
    # 5. Resta el resultado al multiplo de 10 mas cercano
    restaMultiplo = redondeo - sumaTotal  
    
    # 6. Verificar el ultimo digito de la cedula coincida con la cedula 
    ultimoDigito = int(cedula[-1]) #Transformo a int por que la cedula esta como un string
    if ultimoDigito != restaMultiplo:
        #print ("el digito verificador es incorrecto")
        return False    
    return True

#MA;ANA
def convertirACSV(data, nombre_archivo):
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
                
def procesarCedulas(datos):
     #print('Informacion: ', datos)
    #['0504016205', 'Gabriel Alexis', 'Pinta Guanoluisa']
    cedulas = []
    for index,registro in enumerate(datos):
        if(index>0):
            nombre=registro[1]  +" "+ registro[2]
            cedula=registro[0]
            esValido = validarCedula(cedula)
            provincia= None
            if esValido:
                digitoProvincia = (cedula[:2])
                provincia = obtenerProvincia(digitoProvincia)
                
            persona = {
                "cedula": cedula,
                "nombres": nombre,
                "valido": esValido,
                "provincia": provincia["nombre"] if provincia else "",
                "region" : provincia ["region"] 
                
            }
            cedulas.append(persona)
    # FILTRAR VALIDAS
    #print(cedulas)
    cedulasValidas = []
    for cedula in cedulas:
        if cedula["valido"]==True:
            cedulasValidas.append(cedula)
            
    #print(cedulasValidas)
    
    #clasificar por provincias
    cedulasValidas.sort(key=itemgetter('provincia'))
    # print(cedulasValidas)
    # for cedula in cedulasValidas:
    #     print(cedula)
    #     agrupado = {
    #         key:list(group) for key, group in groupby(cedulasValidas,key=lambda x:x['provincia'])  
    #     }   
    # for provincia,cedulas in agrupado.items():
    #     convertirACSV(cedulas,provincia+'.csv')
    return cedulasValidas
    #print(agrupado)
    # for prov in agrupado:
    #     print(prov)
        
def procesarVentas(dato):
    ventas=[]
    for index, venta in enumerate(dato):
        if (index>0):
            vendedor=venta[1]
            id=venta[0]
            esValido = validarCedula(vendedor)
            if esValido:
                vendedor = {
                    'id': id,
                    'vendedor': vendedor
                }
                ventas.append(vendedor)
                
                

def procesarCSV(filas, indexCedula=0):
    cedulas = []
    for index, fila in enumerate(filas):
        if (index>0):
            cedula=fila[indexCedula]
            esValido = validarCedula(cedula)
            
            if esValido:
                digitoProvincia = (cedula[:2])
                provincia = obtenerProvincia(digitoProvincia)
                #print(provincia)
                cedula = {
                    'cedula': cedula,
                    'valida': esValido,
                    'provincia': provincia["nombre"] if  provincia else "",
                    'region':provincia["region"] if provincia  else "" 
                }
                cedulas.append(cedula)
    return cedulas
                
                
                
# def main():
#     datos = importarCSV("./Cedulas_Data.csv", ";")
#     cedulasProcesadas = procesarCSV(datos, 0)
#     print(cedulasProcesadas)
    
# main()
    
