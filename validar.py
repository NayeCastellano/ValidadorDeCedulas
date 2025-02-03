


import csv #libreria para manejar archivos csv
from itertools import groupby # Funcion para agrupar una lista segun un criterio 
from operator import itemgetter # Para acceder a elementos de una lista 

#Recibe la direccion del archivo y el caracter delimitador 
def importarCSV(direccionArchivo, delimiter): 
    try: #intenta capturar errores que puedan surgir durante el llamado del archivo
        with open(direccionArchivo, 'r', encoding = 'utf-8') as archivo:
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
    provincias = {  # Creo un diccionario del numero con su provincia 
        "01": "Azuay",
        "02": "Bolívar",
        "03": "Cañar",
        "04": "Carchi",
        "05": "Cotopaxi",
        "06": "Chimborazo",
        "07": "El Oro",
        "08": "Esmeraldas",
        "09": "Galápagos",
        "10": "Guayas",
        "11": "Imbabura",
        "12": "Loja",
        "13": "Los Ríos",
        "14": "Manabí",
        "15": "Morona Santiago",
        "16": "Napo",
        "17": "Pichincha",
        "18": "Santa Elena",
        "19": "Santo Domingo de los Tsáchilas",
        "20": "Sucumbíos",
        "21": "Tungurahua",
        "22": "Zamora-Chinchipe",
        "23": "Pastaza",
        "24": "Orellana",
        "30": "Ecuatorianos en el exterior"
    }
    provincia = provincias[numeroProvincia] # Busqueda del nombre de la provincia por su clave
    return provincia # Retorna el nombre de la provincia

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
            provincia= " "
            if esValido:
                digitoProvincia = (cedula[:2])
                provincia = obtenerProvincia(digitoProvincia)
                
            persona = {
                "cedula": cedula,
                "nombres": nombre,
                "valido": esValido,
                "provincia": provincia
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
    for cedula in cedulasValidas:
        print(cedula)
    agrupado = {
            key:list(group) for key, group in groupby(cedulasValidas,key=lambda x:x['provincia'])  
        }   
    for provincia,cedulas in agrupado.items():
        convertirACSV(cedulas,provincia+'.csv')
        
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

def main():
    #datos = importarCSV("./Cedulas_Data.csv", ";")
    #procesarCedulas(datos)
    datosVentas=importarCSV("./ventasDataIng.csv",';')
    procesarVentas(datosVentas)
    
main()
    
