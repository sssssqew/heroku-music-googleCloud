# -*- coding: utf-8 -*-
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from mutagen.id3 import ID3
import os 
from django.conf import settings
from .models import AudioFile


def get_metadata(song):
	name = default_storage.get_valid_name(song.name)

	meta = {"song": "", "cover": "static/mp3/cdp.png", "name": name, "album": "", "title": name, "artist": "", 
								"genre": "", "release": "", "encodedby": "", "lyrics": "", "duration": ""}
				
	# 메타데이터 추출 
	try:
		id3 = ID3(song)

		if not default_storage.exists('files/'+name):
			meta["song"] = default_storage.save('files/'+name, song)
			# print(meta["song"])
		else:
			print("song exists ^^")
		
		for key in id3:
			if "APIC" in key:
				# 특정위치에 태그에서 읽은 앨범커버 이미지를 복사함 
				if not default_storage.exists('covers/'+os.path.splitext(name)[0]+'.jpg'):
					meta["cover"] = default_storage.save('covers/'+os.path.splitext(name)[0]+'.jpg', 
						ContentFile(id3.getall(key)[0].data))
					# print(meta["cover"])
				else:
					print("cover exists ^^")

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

	# DB에 음악파일 저장 
	audioFile = AudioFile(**meta)
	audioFile.save()
	# print (song.name + ' just saved in db :)')
	# print ('\n')