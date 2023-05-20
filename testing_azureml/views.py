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
        symboling = int(request.POST['symboling'])
        normalized_losses = float(request.POST['normalized-losses'])
        make = request.POST['make']
        fuel_type = request.POST['fuel-type']
        aspiration = request.POST['aspiration']
        num_of_doors = request.POST['num-of-doors']
        body_style = request.POST['body-style']
        drive_wheels = request.POST['drive-wheels']
        engine_location = request.POST['engine-location']
        wheel_base = float(request.POST['wheel-base'])
        length = float(request.POST['length'])
        width = float(request.POST['width'])
        height = float(request.POST['height'])
        curb_weight = int(request.POST['curb-weight'])
        engine_type = request.POST['engine-type']
        num_of_cylinders = request.POST['num-of-cylinders']
        engine_size = int(request.POST['engine-size'])
        fuel_system = request.POST['fuel-system']
        bore = float(request.POST['bore'])
        stroke = float(request.POST['stroke'])
        compression_ratio = int(request.POST['compression-ratio'])
        horsepower = int(request.POST['horsepower'])
        peak_rpm = int(request.POST['peak-rpm'])
        city_mpg = int(request.POST['city-mpg'])
        highway_mpg = int(request.POST['highway-mpg'])

        # Crear el objeto de datos para la solicitud al endpoint
        data = {
            "Inputs": {
                "WebServiceInput0": [
                    {
                        "symboling": symboling,
                        "normalized-losses": normalized_losses,
                        "make": make,
                        "fuel-type": fuel_type,
                        "aspiration": aspiration,
                        "num-of-doors": num_of_doors,
                        "body-style": body_style,
                        "drive-wheels": drive_wheels,
                        "engine-location": engine_location,
                        "wheel-base": wheel_base,
                        "length": length,
                        "width": width,
                        "height": height,
                        "curb-weight": curb_weight,
                        "engine-type": engine_type,
                        "num-of-cylinders": num_of_cylinders,
                        "engine-size": engine_size,
                        "fuel-system": fuel_system,
                        "bore": bore,
                        "stroke": stroke,
                        "compression-ratio": compression_ratio,
                        "horsepower": horsepower,
                        "peak-rpm": peak_rpm,
                        "city-mpg": city_mpg,
                        "highway-mpg": highway_mpg
                    }
                ]
            },
            "GlobalParameters": {}
        }

        # Convertir los datos a formato JSON
        body = str.encode(json.dumps(data))

        # URL y clave de API proporcionadas por Azure ML
        url = 'http://256e9022-0805-4716-87c2-6a926ed0766e.brazilsouth.azurecontainer.io/score'
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






