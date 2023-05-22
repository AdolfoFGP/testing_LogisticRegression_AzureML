from django.http import HttpResponse
from django.shortcuts import render
import urllib.request
import json
from . import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def prediction_form(request):
    if request.method == 'POST':
        # Obtener los datos del formulario enviado por el usuario
        PatientID = int(request.POST['PatientID'])
        Pregnancies = int(request.POST['Pregnancies'])
        PlasmaGlucose = int(request.POST['PlasmaGlucose'])
        DiastolicBloodPressure = int(request.POST['DiastolicBloodPressure'])
        TricepsThickness = int(request.POST['TricepsThickness'])
        SerumInsulin = int(request.POST['SerumInsulin'])
        BMI = float(request.POST['BMI'])
        DiabetesPedigree = float(request.POST['DiabetesPedigree'])
        Age = int(request.POST['Age'])
        

        # Crear el objeto de datos para la solicitud al endpoint
        data = {
            "Inputs": {
                "input1": [
                    {
                        "PatientID": 1882185,
                        "Pregnancies": 9,
                        "PlasmaGlucose": 104,
                        "DiastolicBloodPressure": 51,
                        "TricepsThickness": 7,
                        "SerumInsulin": 24,
                        "BMI": 27.36983156,
                        "DiabetesPedigree": 1.3504720469999998,
                        "Age": 43
                    }
                ]
            },
            "GlobalParameters": {}
        }

        # Convertir los datos a formato JSON
        body = str.encode(json.dumps(data))

        # URL y clave de API proporcionadas por Azure ML
        url = 'http://dd899ce8-3734-4a8e-8e7e-2b17ea9e37b8.brazilsouth.azurecontainer.io/score'
        api_key = settings.get_azure_api_key()  # Reemplaza con tu clave de API

                # Configurar las cabeceras de la solicitud
        headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

        # Realizar la solicitud al endpoint de Azure ML
        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')

            # Procesar la respuesta JSON obtenida
            prediction = json.loads(result)

            # Renderizar la página de resultados con la predicción obtenida
            return render(request, 'prediction_result.html', {'prediction': prediction})

        except urllib.error.HTTPError as error:
            # Manejar errores de solicitud
            error_message = f"The request failed with status code: {error.code}"
            return render(request, 'error.html', {'error_message': error_message})

    else:
        # Renderizar la página del formulario
        return render(request, 'prediction_form.html')






