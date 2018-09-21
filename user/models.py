from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.


class GlobberUser(AbstractUser):
    name = models.CharField(max_length=250, null=True, default='/',
                                  blank=True)

