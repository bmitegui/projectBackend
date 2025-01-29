from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

from firebase_admin import db

class LandingAPI(APIView):
    
    name = 'Landing API'

    # Coloque el nombre de su colección en el Realtime Database
    collection_name = 'coleccion'

    def get(self, request):
        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')
        
        # get: Obtiene todos los elementos de la colección
        data = ref.get()

        # Devuelve un arreglo JSON
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):	        
        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')

        current_time  = datetime.now()
        custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
        request.data.update({"saved": custom_format })
        
        # push: Guarda el objeto en la colección
        new_resource = ref.push(request.data)
        
        # Devuelve el id del objeto guardado
        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)

class LandingAPIDetail(APIView):

     name = 'Landing Detail API'

     collection_name = 'coleccion'

     def get(self, request, pk):
        ref = db.reference(f'{self.collection_name}')
    
        # get: Obtiene todos los elementos de la colección
        data = ref.get()

        resultado = data.get(pk)

        if resultado is None:
            # Si no se encuentra, retornar un error 404
            return Response({"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Devuelve el elemento encontrado
        return Response(resultado, status=status.HTTP_200_OK)

     def put(self, request, pk):
        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}/{pk}')

        # Verificar si el elemento existe
        if not ref.get():
            return Response({"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar los datos
        ref.update(request.data)

        return Response({"message": "Elemento actualizado exitosamente"}, status=status.HTTP_200_OK)

     def delete(self, request, pk):
        # Referencia al elemento específico
        ref = db.reference(f'{self.collection_name}/{pk}')
        
        # Verificar si el elemento existe
        if not ref.get():
            return Response({"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Eliminar el elemento
        ref.delete()

        return Response({"message": "Elemento eliminado exitosamente"}, status=status.HTTP_200_OK)