#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
		HttpResponse, 
		HttpResponseRedirect, 
		HttpResponseNotFound,
		Http404
	)

from .models import AudioFile
import os

# 페이지 렌더링은 파일전송 성공시 Ajax 콜백함수(success)에서 한번만 함
# Ajax 콜백함수(success)가 호출되면 페이지를 새로고침함 
# 새로고침하면 아래 함수로 들어와 모든 리소스를 업데이트하고 렌더링함 
def index(request):

	print ("rendering start...")
	print("new release ~~~~~~~~~")

	try:
		musics = AudioFile.objects.all()
	except:
		musics = None
	
	print(musics)

	context = {"musics":musics}

	return render(request, 'mp3/layout.html', context)
	

# Ajax 콜이 오면 db 에 파일을 저장만 함
def saveSong(request):
	print ("save files...")

	if request.method == 'POST' and request.FILES:
		print ("request !!")

		for song in request.FILES.getlist('songFile'):
			try:
				audioFile = AudioFile.objects.get(name=song.name)
				print (song.name + ' already exists in db !!')
	 
			except:
				# DB에 음악파일 저장 
				audioFile = AudioFile(song=song, name=song.name)
				audioFile.save()
				print (song.name + ' just saved in db :)')
				print ('\n')

				cmd = 'find static/upload -iname "' + audioFile.filename() +'" -execdir mid3iconv -e cp949 {} \;'
				os.system(cmd)

	# 파일저장만 하면 되기 때문에 return 값이 없음 
	return redirect('mp3:home')











