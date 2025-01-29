from django.shortcuts import render

# Importe requests y json
import requests
import json

# Create your views here.
from django.http import HttpResponse

# Importe el decorador login_required
from django.contrib.auth.decorators import login_required, permission_required

# Restricción de acceso con @login_required y permisos con @permission_required
@login_required
@permission_required('main.index_viewer', raise_exception=True)
def index(request):
    # Arme el endpoint del REST API
    current_url = request.build_absolute_uri()
    url = current_url + '/api/v1/landing'

    # Petición al REST API
    response_http = requests.get(url)
    response_dict = json.loads(response_http.content)

    print("Endpoint ", url)
    print("Response ", response_dict)

    # Respuestas totales
    total_responses = len(response_dict.keys())

    # Valores de la respuesta
    responses = list(response_dict.values())  # Convertir a lista para ordenar

    # Manejo de fechas
    if responses:  # Verificar que hay respuestas
        # Ordenar por la fecha 'saved'
        responses.sort(key=lambda x: x.get('saved'))
        first_response_date = responses[0].get('saved', 'N/A')  # Fecha de la primera respuesta
        last_response_date = responses[-1].get('saved', 'N/A')  # Fecha de la última respuesta
    else:
        first_response_date = 'N/A'
        last_response_date = 'N/A'

    # Objeto con los datos a renderizar
    data = {
        'title': 'Landing - Dashboard',
        'total_responses': total_responses,
        'responses': responses,
        'first_response_date': first_response_date,
        'last_response_date': last_response_date,
    }

    # Renderización en la plantilla
    return render(request, 'main/index.html', data)