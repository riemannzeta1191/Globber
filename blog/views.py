
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import viewsets
from user.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import GlobberUser
from .models import Topic,Article
from .Validator.serializer import ArticleSerializer
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
class ArticlesListView(APIView):

    def get(self, request):
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many=True, context={"request":request})
        return Response(serializer.data)


class ArticleCRUD(APIView):

    def post(self, request):
        topic = request.data["topic"]
        title = request.data["title"]
        content = request.data["content"]
        category = request.data["category"]
        queryset = GlobberUser.objects.get(username=request.user.username)
        if request.user.id == queryset.id:
            serializer = ArticleSerializer(data=request.data,context={"request":request})
            if serializer.is_valid(raise_exception=True):
                data = serializer.validated_data
                serializer.save()
                return Response(serializer.data)


class Article_Update(APIView):
    serializer = ArticleSerializer

    def put(self, request, id):
        title = request.data["title"]
        topic = request.data["topic"]
        try:
            article = Article.objects.get(id=id, title=title)
            serializer = self.serializer(article, data=request.data, context={"request":request,"topic":topic})
            if serializer.is_valid(raise_exception=True):
                data = serializer.validated_data
                serializer.save()
                return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


