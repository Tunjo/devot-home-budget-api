import json
import os
import django
import sys
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def hash_passwords_in_fixture(fixture_path):
    try:
        with open(fixture_path, 'r') as file:
            data = json.load(file)

        for user in data:
            if 'password' in user['fields']:
                user['fields']['password'] = make_password(user['fields']['password'])

        with open(fixture_path, 'w') as file:
            json.dump(data, file, indent=2)

        print(f'Passwords hashed successfully in {fixture_path}!')
    except Exception as e:
        print(f'Error hashing passwords: {e}')
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python hash_fixture_passwords.py <fixture_path>')
        sys.exit(1)

    fixture_path = sys.argv[1]
    hash_passwords_in_fixture(fixture_path)