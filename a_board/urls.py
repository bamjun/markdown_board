# a_board/urls.py
from django.urls import path
from .views import post_list, post_create, post_update, post_delete, post_detail, upload_image, add_comment, delete_comment

urlpatterns = [
    path('', post_list, name='post_list'),
    path('create/', post_create, name='post_create'),
    path('update/<int:post_id>/', post_update, name='post_update'),
    path('delete/<int:post_id>/', post_delete, name='post_delete'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('upload_image/', upload_image, name='upload_image'),
    path('post/<int:post_id>/add_comment/', add_comment, name='add_comment'),
    path('post/<int:post_id>/delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
]
