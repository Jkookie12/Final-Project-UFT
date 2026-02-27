from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta


# =========================
# MAIN BLOG POST MODEL
# =========================
class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)

    # Image upload
    image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True
    )

    # Likes
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.title} | {self.author}"

    def get_absolute_url(self):
        return reverse('blogdetail', args=[str(self.id)])


# =========================
# COMMENTS
# =========================
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} - {self.name}"


# =========================
# OPTIONAL SECOND BLOG MODEL
# (Only keep if you really use it)
# =========================
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='blogpost_like', blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


# =========================
# LOGIN ATTEMPT TRACKING
# =========================
class LoginAttempt(models.Model):
    username = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_recent_attempts(cls, username, minutes=5):
        cutoff = timezone.now() - timedelta(minutes=minutes)
        return cls.objects.filter(
            username=username,
            timestamp__gte=cutoff
        ).count()

    def __str__(self):
        return f"{self.username} - {self.timestamp}"