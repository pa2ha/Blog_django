#!-*-coding:utf-8-*-
from datetime import datetime

from django.db import models


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        now = datetime.now()
        return super().get_queryset().filter(
            is_published=True,
            pub_date__lte=now
        )
