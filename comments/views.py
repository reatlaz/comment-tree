from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .models import Comment


def list_comments(request):
    def build_hierarchy(comment):
        children = Comment.objects.filter(parent=comment)
        return {'id': comment.id, 'text': comment.text, 'created': comment.created, 'replies': [build_hierarchy(c) for c in children]}
    comments = Comment.objects.filter(parent__isnull=True)
    # hierarchy = [{'text': c.text, 'created': c.created, 'replies': []} for c in comments]
    hierarchy = [build_hierarchy(c) for c in comments]



    # comments = Comment.objects.filter(parent__isnull=True)
    # serialized_comments = serializers.serialize('json', [ comments, ])
    return JsonResponse({
        # 'data': CommentSerializer(Comments, many=True).data,
        'data': hierarchy
    })

@csrf_exempt
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    children = Comment.objects.filter(parent_id=comment_id)

    children.update(parent_id=comment.parent_id)
    comment.delete()


    return JsonResponse({
        'data': comment_id
    })
