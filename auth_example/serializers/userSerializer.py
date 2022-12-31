from ..models.user import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta: # Metadata del serializer
        model = User # Modelo a asociar el serializer
        fields = ['id', 'username', 'password', 'name', 'email'] #campos que espero lleguen desde el body en postman, que son los mismos atributos de la clase Users

    def to_representation(self, obj): # La respuesta al servicio web para el ususario. Acá se hacen los inner join
        user = User.objects.get(id=obj.id) # obj es de tipo User
        return {  # La respuesta en el servicio web y lo que se mostrará al consultar por usuario. No se muestra el password 
            'id' : user.id,
            'username' : user.username,
            'name' : user.name,
            'email' : user.email
        }