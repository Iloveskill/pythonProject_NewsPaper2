from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating_sum = Post.objects.filter(author=self).aggregate(Sum('post_rating'))['post_rating_sum']
        comment_rating_sum = \
            Comment.objects.filter(user__author=self).aggregate(Sum('comment_rating'))['comment_rating__sum']
        post_comment_rating_sum = \
            Comment.objects.filter(post__author=self).aggregate(Sum('comment_rating'))['comment_rating__sum']
        self.author_rating = post_rating_sum * 3 + comment_rating_sum +post_comment_rating_sum
        self.save()

class Category(models.Model):
    category_news = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    post_type_choices = (('nw', 'Новость'), ('ct', 'Статья'))
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=post_type_choices)
    post_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    post_name = models.CharField(max_lenght=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def post_like(self):
        self.post_rating += 1
        self.save()

    def post_dislike(self):
        self.save()

    def preview(self):
        print(str(self.post_text)[:123], '...')

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    data_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def comment_like(self):
        self.comment_rating += 1
        self.save()

    def comment_dislike(self):
        self.comment_rating -= 1
        self.save()

