from rest_framework import status, views # status de respuesta HTTP, views 
from rest_framework.response import Response # Respuestas personalizadas
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # obtener pareja token
from ..serializers.userSerializer import UserSerializer


class UserCreateView(views.APIView):
    def post(self, request, *args, **kwargs): # request: toda la información del llamado por REST
        serializer = UserSerializer(data=request.data) #data es el diccionario con los campos del UserSerializer desde postman (body) o servicio web
        serializer.is_valid(raise_exception=True) # VAlida la información del userSerializer (fields)
        serializer.save() # Guarda info en el serializer. Crea el usuario

        token_data = {'username' : request.data['username'], # vienen en body del postman
                      'password' : request.data['password']}
        token_serializer = TokenObtainPairSerializer(data=token_data) # token_data para crear el token
        token_serializer.is_valid(raise_exception=True)
        return Response(token_serializer.validated_data, status=status.HTTP_201_CREATED)
        