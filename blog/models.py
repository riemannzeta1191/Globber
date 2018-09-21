import psycopg2


from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.
from user.models import GlobberUser


class Topic(models.Model):
    topic = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.topic


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    @staticmethod
    def create_db_connection():

        connection = psycopg2.connect(
            database="blog",
            user="sayan",
            password="",
        )
        return connection

    @classmethod
    def truncate(cls):
        connection = cls.create_db_connection()
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))


class Article(models.Model):
    title = models.CharField(max_length=70, unique=True)
    content = models.CharField(max_length=3000)
    author = models.ForeignKey(GlobberUser,related_name='article_author',on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Category,related_name='article_category', on_delete=models.CASCADE,null=True)
    date = models.DateField(null=True)
    image = models.URLField()
    topic = models.ManyToManyField(Topic)

