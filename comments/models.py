from django.db import models

from treebeard.mp_tree import MP_Node

class Comment(MP_Node):
    text = models.TextField(null=False)
    created = models.DateTimeField(blank=True, auto_now_add=True)
    # parent = models.ForeignKey('self', null=True, related_name='replies', on_delete=models.CASCADE)


    def __str__(self):
        return 'Comment: {}'.format(self.text)