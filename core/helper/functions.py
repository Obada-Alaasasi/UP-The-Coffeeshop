from django.contrib.auth.models import User
from.Exceptions import PswdLength, PswdRule

def check_password(password):
    '''validate credentials'''

    #password too short:
    if len(password) < 8:
        return PswdLength

    #password rules:
    elif password.islower() or password.isupper() or password.isalpha():
        return PswdRule

    else: return None





