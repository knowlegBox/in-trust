from django.contrib import admin
from .models import Article, Category, Tag, News, Profile, NewsletterSubscriber, ContactMessage

# Register your models here.
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(News)
admin.site.register(Profile)
admin.site.register(NewsletterSubscriber)
admin.site.register(ContactMessage)
