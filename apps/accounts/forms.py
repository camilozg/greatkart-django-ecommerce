from django.contrib.auth.forms import UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Para modificar el formulario de creación de Usuario por defecto heredamos
    de UserCreationForm. En la clase Meta definimos el modelo y los campos que
    queremos en el formulario.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        """
        Podemos sobreescribir el método __init__ para hacer modificaciones en el formulario.
        En este caso agregamos la clase 'form-control', los placeholders y eliminamos el
        sufijo de dos puntos que traen los labels por defecto en Django.
        """
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.label_suffix = ''  # Eliminamos el sufijo ':'

        self.error_messages['password_mismatch'] = 'Las contraseñas no coinciden.'

        labels = {
            'password2': 'Confirmar contraseña',
        }

        placeholders = {
            'first_name': 'Ingresa tu nombre',
            'last_name': 'Ingresa tus apellidos',
            'phone_number': 'Ingresa tu teléfono',
            'email': 'Ingresa tu email',
            'password1': 'Ingresa una contraseña',
            'password2': 'Confirma la contraseña',
        }

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field in placeholders:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            if field in labels:
                self.fields[field].label = labels[field]
