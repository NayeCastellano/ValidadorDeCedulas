from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .data import obtener_usuarios, obtenerUsuario
from .validar import procesarCSV, importarCSV
import json
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
class HelloWorldView(View):
    def get(self, request):
        return JsonResponse(
            {
                "message": "Hello world"
             }
            )
        
        
@csrf_exempt
def login_view(request):
    print("Requesting.....")
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Leer JSON
            email = data.get("email")
            password = data.get("password")
            user = obtenerUsuario(email, password)
            if user:
                return JsonResponse(user, status=200)
            else:
                return JsonResponse({"error": "Credenciales incorrectas"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400)

@csrf_exempt
def obtenerRegistros(request):
    print("Getting cedulas....")
    if request.method == "GET" or request.method == "POST":
        try:
            
            region = request.GET.get('region')
            
            datos = importarCSV("Cedulas_Data.csv", ";")
            cedulasProcesadas = procesarCSV(datos, 0)
            celulasFiltradas = []
            
            if region:
                celulasFiltradas = [cedula for cedula in cedulasProcesadas if cedula['region'] == region]
            else: celulasFiltradas = cedulasProcesadas

                
            data_serializable = []
            for item in celulasFiltradas:
                data_serializable.append({
                    'cedula': item['cedula'],
                    'valida': item['valida'],
                    'provincia': item['provincia'],
                    'region': item['region'],
                })
            return JsonResponse(data_serializable, status=200, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400)
