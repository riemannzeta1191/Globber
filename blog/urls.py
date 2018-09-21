from django.conf.urls import url
from .views import ArticlesListView,ArticleCRUD
from blog import views

urlpatterns = [
        url(r'^articles/$', views.ArticlesListView.as_view(), name='articles'),
        url(r'^article/$', views.ArticleCRUD.as_view(), name='article'),
        url(r'^article/(?P<id>[0-9]+)/$', views.Article_Update.as_view(), name='update'),

]