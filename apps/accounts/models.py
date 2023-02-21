from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Para crear un usuario customizado primero creamos un UserManager heredando de
    BaseUserManager y sobreescribimos los métodos create_user y create_superuser.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Recibe como parámetros los campos requeridos para crear un usuario.
        Puede recibir campos adicionales en **extra_fields. Los campos adicionales
        deben estar definidos en el modelo
        """
        if not email:
            raise ValueError('El usuario debe tener un email')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    Podemos usar AbstractUser o AbstractBaseUser para crear el usuario customizando
    asigandole el CustomUserManager creado previamente en la variable objects.

    AbstractUser:

        Usamos todos los campos del usuario por defecto de Django. Podemos excluir
        algunos campos igualandolos a None y podemos agregar otros campos.

    Campos por defecto:

        username
        email
        first_name
        last_name
        is_staff
        is_superuser
        is_active
        last_login
        date_joined
    """

    email = models.EmailField("email", max_length=100, unique=True)
    phone_number = models.CharField("teléfono", max_length=50, blank=True)

    username = None

    USERNAME_FIELD = 'email'  # Campo de login. Por defecto es username
    REQUIRED_FIELDS = []  # Campos requeridos para crear un superusuario

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return self.email


# class User(AbstractBaseUser, PermissionsMixin):
#     """
#     AbstractBaseUser:

#         Definimos nosotros mismos los campos del usuario. Si queremos podemos
#         agregar los campos por defecto.

#         Los campos is_superuser y last_login siempre son creados por AbstractBaseUser
#         así no los definamos.

#         El campo is_staff es mandatorio si no se sobreescribe el método is_staff() que
#         retorna un booleano indicando si el usuario es administrador. Si queremos
#         usar otro nombre o eliminar el campo debemos sobreescribir el método retornando
#         el valor de la variable que reemplace ese campo o retornando siempre True
#         en caso de que no usemos ningún sustituto. Al usar otra variable habría que
#         agregarla al método create_superuser de CustomUserManager sustituyendo a
#         user.is_staff .

#         Adicionalmente, heredamos de la clase PermissionsMixin para otorgarle al
#         ususario todas las caracteristicas de permisos de Django.
#     """

#     email = models.EmailField("email", max_length=100, unique=True)
#     first_name = models.CharField("nombre", max_length=50, blank=True)
#     last_name = models.CharField("apellido", max_length=50, blank=True)
#     phone_number = models.CharField("teléfono", max_length=50, blank=True)
#     is_admin = models.BooleanField(default=False)
#     # is_staff = models.BooleanField("staff", default=False)
#     # is_superuser = models.BooleanField("super usuario", default=False)
#     # is_active = models.BooleanField("activo", default=False)
#     # last_login = models.DateTimeField("último acceso", auto_now_add=True)
#     # date_joined = models.DateTimeField("fecha de registro", auto_now_add=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     class Meta:
#         verbose_name = 'usuario'
#         verbose_name_plural = 'usuarios'

#     def __str__(self):
#         return self.email

#     @property
#     def is_staff(self):
#         return self.is_admin
