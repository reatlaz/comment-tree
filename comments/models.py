from django.db import models

class Comment(models.Model):
    text = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    # grandparent = models.ForeignKey('self', null=True, related_name='child_replies', on_delete=models.SET(parent.parent))
    parent = models.ForeignKey('self', null=True, related_name='replies', on_delete=models.CASCADE)



    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return self.text if self.text else ''
    