from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .models import Comment


def list_comments(request):

    return JsonResponse({
        'data': Comment.dump_bulk()[0].get('children', 'no comments')
    })

@csrf_exempt
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    children = comment.get_children()
    for child in children:
        child.move(comment)

    comment.delete()

    return JsonResponse({'data': comment_id})
