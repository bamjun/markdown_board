# board/views.py
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post, Image, Comment
import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import PostForm, CommentForm
import re

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'a_board/post_list.html', {'posts': posts})


@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('file')
        image_instance = Image.objects.create(image=image)
        return JsonResponse({'url': image_instance.image.url, 'id': image_instance.id})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            image_ids = json.loads(request.POST.get('image_ids', '[]'))
            post.image_list = image_ids
            post.save()
            # 게시물이 생성될 때 해당 이미지의 check_for_upload 필드를 True로 설정
            Image.objects.filter(id__in=image_ids).update(check_for_upload=True)
            Image.objects.filter(check_for_upload=False).delete()

            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'a_board/post_form.html', {'form': form, 'post': None})


def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            old_image_ids = set(post.image_list)
            post = form.save(commit=False)
            
            # 게시글 내용에서 이미지 URL을 추출합니다.
            content_image_ids = set()
            urls = re.findall(r'!\[image\]\((.*?)\)', post.content)
            for url in urls:
                filename = url.split('/')[-1]
                try:
                    image = Image.objects.get(image='images/' + filename)
                    content_image_ids.add(image.id)
                except Image.DoesNotExist:
                    continue

            # 삭제할 이미지 ID는 기존 이미지 리스트에 있는데, 게시글 내용에는 없는 ID입니다.
            to_delete_image_ids = old_image_ids - content_image_ids
            
            # 삭제할 이미지를 실제로 삭제합니다.
            for image_id in to_delete_image_ids:
                try:
                    image = Image.objects.get(id=image_id)
                    image.delete()
                except Image.DoesNotExist:
                    continue
            
            # 게시글의 이미지 리스트를 새 이미지 리스트로 업데이트합니다.
            post.image_list = list(content_image_ids)
            post.save()
            
            # 게시물이 업데이트될 때 해당 이미지의 check_for_upload 필드를 True로 설정
            Image.objects.filter(id__in=content_image_ids).update(check_for_upload=True)
            
            # check_for_upload가 False인 이미지 삭제
            Image.objects.filter(check_for_upload=False).delete()
            
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'a_board/post_form.html', {'form': form, 'post': post})


def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('post_list')

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    comment_form = CommentForm()
    return render(request, 'a_board/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    return redirect('post_detail', post_id=post.id)

def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('post_detail', post_id=post_id)
