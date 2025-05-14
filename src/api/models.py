from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    categories = models.ManyToManyField('Category', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    is_private = models.BooleanField(default=False, blank=True, null=True)
    active = models.BooleanField(default=False, blank=True, null=True)
    metas = models.JSONField(default=dict, blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="article_updated_by")
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="article_added_by")
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    active = models.BooleanField(default=False, blank=True, null=True)
    metas = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="category_updated_by")
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="category_added_by")
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    active = models.BooleanField(default=False, blank=True, null=True)
    metas = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="tag_updated_by")
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="tag_added_by")
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

class News(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True,null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    category = models.CharField(max_length=100, choices=[
        ('ia', 'IA'),
        ('securite', 'Sécurité'),
        ('reseaux', 'Réseaux'),
        ('developpement', 'Développement'),
    ], blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=False, blank=True, null=True)
    metas = models.JSONField(default=dict, blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="news_updated_by")
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="news_added_by")
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    avatar = models.CharField(max_length=256, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=False, blank=True, null=True)
    metas = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="profile_updated_by")
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="profile_added_by")
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, blank=True, null=True)
    subscribed_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_confirmed = models.BooleanField(default=False, blank=True, null=True)
    confirmation_token = models.CharField(max_length=64, unique=True, blank=True, null=True)
    active = models.BooleanField(default=False, blank=True, null=True)
    metas = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="news_letter_subscriber_updated_by")
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="news_letter_subscriber_added_by")
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_processed = models.BooleanField(default=False, blank=True, null=True)
    active = models.BooleanField(default=False, blank=True, null=True)
    metas = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="contact_message_updated_by")
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="contact_message_added_by")
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)
