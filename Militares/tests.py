import random
import string
from django.contrib.auth import get_user_model

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def reset_passwords():
    User = get_user_model()
    users = User.objects.all()
    for user in users:
        new_password = generate_strong_password()
        user.set_password(new_password)
        user.save()
        print(f'Nova senha para {user.username}: {new_password}')

# Chame essa função para redefinir as senhas
reset_passwords()
