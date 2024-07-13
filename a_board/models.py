# a_board/models.py
from django.db import models
import markdown

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image_list = models.JSONField(default=list)


    def __str__(self):
        return self.title
    
    def get_markdown(self):
        return markdown.markdown(self.content)
    
    def delete(self, *args, **kwargs):
        # 게시글 삭제 시 연관된 이미지를 삭제
        for image_id in self.image_list:
            try:
                image = Image.objects.get(id=image_id)
                image.delete()
            except Image.DoesNotExist:
                continue
        super().delete(*args, **kwargs)

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    check_for_upload = models.BooleanField(default=False)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.id} on {self.post}'
