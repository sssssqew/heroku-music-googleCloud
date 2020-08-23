# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseNotFound,
    Http404
)

from .models import AudioFile
from django.conf import settings

# from pprint import pprint

import time

# 비동기 작업
from .tasks import uploadSongToGoogleStorage, add

# 페이지 렌더링은 파일전송 성공시 Ajax 콜백함수(success)에서 한번만 함
# Ajax 콜백함수(success)가 호출되면 페이지를 새로고침함
# 새로고침하면 아래 함수로 들어와 모든 리소스를 업데이트하고 렌더링함

from django.conf import settings

def save_song(pathToSave, song):
    with open(pathToSave, "wb") as f:
        f.write(song.read())


def index(request):
    print("rendering start...")
    try:
        musics = AudioFile.objects.all()
    except:
        musics = None
    context = {"musics": musics}

    return render(request, 'mp3/layout.html', context)

# Ajax 콜이 오면 db 에 파일을 저장만 함
def saveSong(request):
    start_time = time.time()
    print("save files...")

    if request.method == 'POST' and request.FILES:
        print("request !!")

        for song in request.FILES.getlist('songFile'):
            try:
                DB_get_time = time.time()
                audioFile = AudioFile.objects.get(title=song.name)
                print(song.name + ' already exists in db !!')
                print("--- DB access Time: %s seconds ---" % (time.time() - DB_get_time))
            except:
                # 업로드한 임시파일이 셀러리가 실행될때 파일이 존재하지 않아 임시로 저장한 후 샐러리 실행후 삭제함
                savedFilePath=settings.STATICFILES_DIRS[0]+'/'+song.name
                save_song(savedFilePath,song)
                
                # 구글 스토리지에 음원과 앨범아트 업로드하는 건 셀러리를 이용한 비동기 처리로 실행함(너무 오래 걸리는 작업이라서)
                songInfos={"name": song.name, "savedFilePath": savedFilePath}
                print("google upload started ......")
                add.delay(4,9)
                res=uploadSongToGoogleStorage.delay(songInfos)
                print(res.state) # 'SUCCESS'
                print(res.get()) # 7

    print("--- Execute Time: %s seconds ---" % (time.time() - start_time))

    # 파일저장만 하면 되기 때문에 return 값이 없음
    # return redirect('mp3:home')
    return HttpResponse("")
