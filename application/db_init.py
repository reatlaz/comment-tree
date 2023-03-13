import mysql.connector
import json, os
import random
import string

from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from collections import deque


with open('secrets.json') as f:
    secrets = json.load(f)

def get_secret(setting, secrets=secrets):
    '''Get the secret variable or return explicit exception.'''
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Set the {0} environment variable'.format(setting)
        raise ImproperlyConfigured(error_msg)
    
conn = mysql.connector.connect(
    host=get_secret('DATABASES_HOST'),
    database=get_secret('DATABASES_NAME'),
    user=get_secret('DATABASES_USER'),
    password=get_secret('DATABASES_PASSWORD'))

cursor = conn.cursor()
letters = string.ascii_letters

settings.configure()

values = []
q = deque()
id = 1
count = 0
for _ in range(random.randint(100, 200)):
    text = ''.join(random.choice(letters) for _ in range(random.randint(4, 10)))
    values.append(f"({id}, '{text}', '{timezone.now()}', null)")
    id += 1
    q.append(id)
    count += 1

cursor.execute(f'''
    TRUNCATE TABLE comments_comment;
    INSERT INTO comments_comment (id, text, created, parent_id)
        VALUES {','.join(values)};
''', multi=True)
conn.commit()
for depth in range(1, 7):
    values = []
    next_q = deque()
    while q:
        parent = q.popleft()
        for _ in range(random.randint(0, 3)):
            text = ''.join(random.choice(letters) for _ in range(random.randint(4, 10)))
            values.append(f"({id}, '{text}', '{timezone.now()}', {parent})")
            id += 1
            next_q.append(id)
            count += 1
    q = next_q

    cursor.execute(f'''
        INSERT INTO comments_comment (id, text, created, parent_id)
            VALUES {','.join(values)};
    ''')
    conn.commit()

print(count)