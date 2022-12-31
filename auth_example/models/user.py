# Clase 9 nov
## Se borran los los archivos models y views y se crean las CARPETAS en auth_example (models, views, serializers)
## Se crea un __init__.py en cada carpeta

from django.db import models # Librerías ya hechas y que se heredan de Django
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin # COnfiguración de usuarios
from django.contrib.auth.hashers import make_password #Codifica la contraseña para manipularla de manera segura

# Clase 9 nov
class UserManager(BaseUserManager): #Administrador aplicación
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("El cliente debe tener un username.")
        user = self.model(username=username) # El primer model es heredado de BaseUserManager desde INSTALLED_APPS (settings)
        user.set_password(password) #Conf el password para el usuario
        user.save(using=self._db) # Base configurada para el proyecto y no en la de Django
        return user

    def create_superuser(self, username, password=None): #Admin de Django. Este es más "peligroso"
        user = self.create_user(    # Lamado del método create_user que se creó arriba de la clase UserManager
            username = username,
            password = password
        )
        user.is_admin = True # Ej ususario creado en UserManager ahora es admin de Django
        user.save(using=self._db) 
        return user

# Clase 9 nov
class User(AbstractBaseUser, PermissionsMixin): # Se heredan las librerias. Creación del modelo User
    id          = models.BigAutoField(primary_key=True)
    username    = models.CharField('Username', max_length=20, unique=True) # Primer atributo es un alias
    password    = models.CharField('Password', max_length=256) # 256 porque está encriptado en un hash settings -> SIMPLE_JWT{'ALGORITH':'HS256}
    name        = models.CharField('Name', max_length=50)
    email       = models.EmailField('Email', max_length=100, unique=True)

    def save(self, **kwargs): #Paso intermedio antes de guardar en la base de datos (kwargs -> dict de argumentos). Self lo hace parte de una clase (métodoS)
        some_salt = 'mMUj0DrIK6vgtdIYepkIxN'
        self.password = make_password(self.password, some_salt) # Toma la contraseña del user, la pasa por el salt y crea una contraseña de 256 caracteres
        super().save(**kwargs) # invocar a la super clase y usa el método save. Guarda el ususrio y el password encriptado

    objects        = UserManager()
    USERNAME_FIELD = 'username' # Campo sobre el cual hace la validación al momento de autenticarse. Podría ser email (por ejemplo)
    