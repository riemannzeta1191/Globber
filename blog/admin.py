from django.contrib import admin
from .models import Article, Category,Topic
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'author', 'date','image')
    list_filter = ['topic']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')



class TopicAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Topic, TopicAdmin)