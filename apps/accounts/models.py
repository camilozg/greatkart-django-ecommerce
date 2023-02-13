from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    Heredar de BaseUserManager y sobreeescribir los métodos create_user
    y create_superuser para crear un UserManager customizado.
    """

    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        # user.is_active = True
        # user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Heredar de AbstractBaseUser y agregar el CustomUserManager al atributo objects.
    Agregar a settings.py el usuario customizado: AUTH_USER_MODEL = 'accounts.User'
    """

    first_name = models.CharField("nombre", max_length=50, blank=True)
    last_name = models.CharField("apellido", max_length=50, blank=True)
    username = models.CharField("usuario", max_length=50, unique=True)
    email = models.EmailField("email", max_length=100, unique=True)
    phone_number = models.CharField("teléfono", max_length=50, blank=True)

    # Campos mandatorios del User por defecto
    is_admin = models.BooleanField("es admin", default=False)
    is_staff = models.BooleanField("es staff", default=False)

    # Campos extra del User por defecto que no son mandatorios
    last_login = models.DateTimeField("último acceso", auto_now_add=True)
    date_joined = models.DateTimeField("fecha de registro", auto_now_add=True)
    # is_active = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Campo de login, por defecto es username
    REQUIRED_FIELDS = ['username']  # Campos requeridos para crear un usuario

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return self.email

    # Métodos mandatorios cuando se hereda de AbstractBaseUser
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
