# -*- coding: utf-8 -*-
from django.db import models
import os
import uuid

# 음악정보 추출 라이브러리
# 모델 수정후에는 반드시 히로쿠 마이그레이션 필요함
# heroku pg:reset (DB 클리어)
# DB 클리어 후 반드시 마이그레이션 필요함
# heroku run python manage.py makemigrations
# heroku run python manage.py migrate
# heroku run bash --app sylee-music-player (히로쿠 폴더 접근)

# 모델 변경시 할일 순서
# 1. (add/modify some someapp/models.py)
# 2. python manage.py makemigrations someapp
# 3. python manage.py migrate
# 4. git add someapp/migrations/*.py (to add the new migration file)
# 5. git commit -m "added migration for app someapp"
# 6. git push heroku
# 7. heroku pg:reset
# 8. heroku run python manage.py migrate



class AudioFile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cover = models.CharField(max_length=500, null=True)
    album = models.CharField(max_length=300, null=True)
    title = models.CharField(max_length=300, null=True)
    artist = models.CharField(max_length=300, null=True)
    genre = models.CharField(max_length=300, null=True)
    release = models.CharField(max_length=300, null=True)
    lyrics = models.CharField(max_length=300, null=True)
    duration = models.CharField(max_length=300, null=True)
    cloudSrc = models.CharField(max_length=500, null=True)

    def __unicode__(self):
        return self.title

    def get_GoogleStorageFolderName(self):
        return "songs"

 