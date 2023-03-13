from django.urls import path
from comments.views import list_comments, delete_comment
urlpatterns = [
    path('', list_comments, name='list_comments'),
    path('<int:comment_id>/', delete_comment, name='delete_comment'),
]
