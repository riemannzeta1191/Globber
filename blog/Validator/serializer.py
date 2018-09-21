from rest_framework import serializers

from blog.models import Article,Category,Topic
import datetime


class TopicSerializer(serializers.ModelSerializer):
    topic = serializers.CharField()

    class Meta:
        model = Topic
        fields = ('id','topic')


class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField()

    class Meta:
        model = Category
        fields = ('id','name',)


class ArticleSerializer(serializers.ModelSerializer):

    topic = TopicSerializer(many=True)
    category = CategorySerializer()
    title = serializers.CharField()
    current_user = serializers.SerializerMethodField('get_user')
    current_date = serializers.SerializerMethodField('get_date')

    def get_user(self, obj):
        request = self.context['request']
        if request:
            return {"id": request.user.id, "name": request.user.name}

    def get_date(self, obj):
        return datetime.date.today()

    class Meta:
        model = Article
        fields = ('id', 'topic','current_user','category','title', 'current_date','content')

    def create(self, validated_data):
        topic_data = validated_data.pop('topic')
        categories = validated_data.pop('category')
        date = datetime.date.today()
        cat, created = Category.objects.get_or_create(name=categories["name"],slug=categories["name"])
        article = Article.objects.create(**validated_data, category_id=cat.id, author_id=self.context['request'].user.id)
        article.date = date
        article.save()
        for topic in topic_data:
            queryset,_ = Topic.objects.get_or_create(topic=topic["topic"])
            article.topic.add(queryset)
        return article

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get('content', instance.content)
        topics = self.context['topic']
        ids = [el['id'] for el in topics]
        article = Article.objects.filter(id=instance.id,title=instance.title).prefetch_related('topic')
        for elem in article:
            queryset = elem.topic.all()
            t_ids = [topic.id for topic in queryset]
            if len(ids)-len(t_ids)>0:
                diff_list = [m for m in ids if m not in t_ids]
                for diff in diff_list:
                    topic_instance = Topic.objects.get(id=diff)
                    instance.topic.add(topic_instance)
            else:
                diff_list = [m for m in t_ids if m not in ids]
                for diff in diff_list:
                    topic_instance = Topic.objects.get(id=diff)
                    instance.topic.remove(topic_instance)

        instance.save()
        return instance
