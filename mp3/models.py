#-*- coding: utf-8 -*-
from django.db import models
import os

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
 
from mutagen.id3 import ID3

class AudioFile(models.Model):

	song = models.FileField(upload_to='upload', null=True) 
	name = models.CharField(max_length=300, null=True)	

	def __unicode__(self):
		return self.name 

	def filename(self):
		return os.path.basename(self.song.file.name)

	def metadata(self):
		
		musicName = os.path.splitext(self.filename())[0] # 확장자를 제외한 파일명 
		coverPath = 'static/albumCover/'+ musicName + '.jpg'  
		coverDefault = 'cdp.png'
		titleDefault = os.path.splitext(self.name)[0]

		meta = {"cover": coverDefault, "album": "", "title": titleDefault, "artist": "", "genre": "", "release": "", "encodedby": "", "lyrics": "", "duration": 0}

		if self.song:

			# 메타데이터 추출 
			try:
				id3 = ID3(self.song)
				
				for key in id3:
					if "APIC" in key:
						# 특정위치에 태그에서 읽은 앨범커버 이미지를 복사함 
						if not os.path.exists(coverPath):
							with open(coverPath, 'wb') as img:
								img.write(id3.getall(key)[0].data)
						else:
							print ("cover already exists !!")						

						meta["cover"] = musicName + '.jpg'

					if "TALB" in key:
						meta["album"] = str(id3.getall(key)[0])					

					if "TIT" in key:
						meta["title"] = str(id3.getall(key)[0])
						
					if "TPE" in key:
						meta["artist"] = str(id3.getall(key)[0])	

					if "TCON" in key:
						meta["genre"] = str(id3.getall(key)[0])
					
					if "TDRC" in key:
						meta["release"] = str(id3.getall(key)[0])
					
					if "TENC" in key or "COMM" in key:
						meta["encodedby"] = str(id3.getall(key)[0])

					if "USLT" in key:
						try:	
							meta['lyrics'] = id3.getall(key)[0]
						except:
							print ("failed to extract lyrics :(")			

				# meta["duration"] = id3.pprint()

			except:
				print ("failed to extract metadata :(")

		else:
			print ("There is no song :(");

		# print('------------------------------------')
		# print ("cover : " + meta["cover"])
		# print ("album : " + meta["album"])
		# print ("title : " + meta["title"])
		# print ("artist : " + meta["artist"])
		# print ("genre : " + meta["genre"])
		# print ("release : " + meta["release"])
		# print ("encodedby : " + meta["encodedby"])
		# print ("lyrics : " + meta["lyrics"])
		# print ("duration : " + str(meta["duration"]))

		return meta 
