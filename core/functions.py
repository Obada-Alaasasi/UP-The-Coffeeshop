from django.contrib.auth.models import User

def check_password(password):
    '''validate credentials'''

    #password too short:
    if len(password) < 8:
        return 'Password must be at least 8 characters'

    #password rules:
    elif password.islower() or password.isupper() or password.isalpha():
        return 'Password must contain at least: 1 uppercase, 1 lowercase, and 1 number'

    else: return None

