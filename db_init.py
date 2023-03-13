import json
import os
import sys
import random
import string

from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
import django

sys.path.append(
    os.path.join(os.path.dirname(__file__), 'comment_tree')
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings")
django.setup()
from django.conf import settings


from collections import deque
from comments.models import Comment

with open('secrets.json') as f:
    secrets = json.load(f)

def get_secret(setting, secrets=secrets):
    '''Get the secret variable or return explicit exception.'''
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Set the {0} environment variable'.format(setting)
        raise ImproperlyConfigured(error_msg)

letters = string.ascii_letters

get = lambda node_id: Comment.objects.get(pk=node_id)

Comment.objects.all().delete()
root = Comment.add_root(text='root')

values = []
q = deque()

for _ in range(random.randint(100, 200)):
    text = ''.join(random.choice(letters) for _ in range(random.randint(4, 10)))
    node = get(root.pk).add_child(text=text)
    q.append(node.pk)

for depth in range(1, 7):
    next_q = deque()
    while q:
        parent_id = q.popleft()
        for _ in range(random.randint(0, 3)):
            text = ''.join(random.choice(letters) for _ in range(random.randint(4, 10)))
            node = get(parent_id).add_child(text=text)
            next_q.append(node.pk)

    q = next_q


