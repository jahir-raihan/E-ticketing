from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserRegisterForm(UserCreationForm):

    """Form to register a student"""

    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'station_name', 'password1', 'password2']


class UserRegisterForm2(UserCreationForm):

    """Form to register a student"""

    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'password1', 'password2']