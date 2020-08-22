# -*- coding: utf-8 -*-
from django.db import models
import os

# heroku 현재는 python 3.6. 버전만 지원함

# 음악정보 추출 라이브러리
# 모델 수정후에는 반드시 히로쿠 마이그레이션 필요함
# heroku pg:reset (DB 클리어)
# DB 클리어 후 반드시 마이그레이션 필요함
# heroku run python manage.py makemigrations
# heroku run python manage.py migrate
# heroku run bash --app sylee-music-player (히로쿠 폴더 접근)

# 모델 변경시 할일 순서
# 0. (add/modify some someapp/models.py)
# 1. django settings => change db to sqlite3
# 2. python manage.py makemigrations someapp
# 3. python manage.py migrate
# 4. django settings => chnge db to postregreSQL
# 4. git add someapp/migrations/*.py (to add the new migration file)
# 5. git commit -m "added migration for app someapp"
# 6. git push heroku master
# 7. heroku pg:reset
# 8. heroku run python manage.py migrate
# 9. heroku run python manage.py createsuperuser
# 10. heroku logs --tail

# 모델이나 DB 관련 에러 나면 migrations 폴더 통째로 날리고 새로 생성한 후 
# __init__.py 파일 넣어주고 다시 마이그레이션 하기


# CharField max_length 가 너무 크니까 오류남 => 길이제한 없는 TextFiled로 교체함
# CharField max_length 너무 크게 잡으면 DatabaseError: value too long for type character varying 오류 메시지 뜸
class AudioFile(models.Model):

    cover = models.TextField()
    album = models.TextField()
    title = models.TextField()
    artist = models.TextField()
    genre = models.TextField()
    release = models.TextField()
    lyrics = models.TextField()
    duration = models.TextField()
    cloudSrc = models.TextField()

    def __unicode__(self):
        return self.title

 