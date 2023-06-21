import sys
from django.db import models
from account.models import CustomUser
from django.core.validators import MinLengthValidator


sys.path.append("..account")


class Favorite(models.Model):
    title = models.CharField(max_length=150)
    link = models.TextField(validators=[MinLengthValidator(10)])
    auth = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name='links')
