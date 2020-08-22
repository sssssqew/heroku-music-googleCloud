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

import pyrebase # 구글 파이어베이스
import eyed3 # 태그 추출
# from pprint import pprint

import time


# 페이지 렌더링은 파일전송 성공시 Ajax 콜백함수(success)에서 한번만 함
# Ajax 콜백함수(success)가 호출되면 페이지를 새로고침함
# 새로고침하면 아래 함수로 들어와 모든 리소스를 업데이트하고 렌더링함


# 구글 파이어베이스 설정
config = {
    "apiKey": "AIzaSyCZc9YmafjkxEp9e-0_kmTwJSoi3Wxvyl0",
    "authDomain": "sylee-music-player.firebaseapp.com",
    "databaseURL": "https://sylee-music-player.firebaseio.com",
    "projectId": "sylee-music-player",
    "storageBucket": "sylee-music-player.appspot.com",
    "messagingSenderId": "446731774418",
    "appId": "1:446731774418:web:62d80332b91bc43d6f000b",
    "measurementId": "G-Y3FWCRRGK4"
}

gsFileFolder = "songs"
gsCoverFolder = "covers"

# 구글 스토리지 초기화
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
storage = firebase.storage()
user = auth.sign_in_with_email_and_password(
    "syleemomo@gmail.com", "rkrrlska7496ab@")

# auth.create_user_with_email_and_password(email, password) # 이메일 생성


def duration_from_seconds(s):
    """Module to get the convert Seconds to a time like format."""
    s = s
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    timelapsed = "{:01d}:{:02d}:{:02d}:{:02d}".format(int(d),
                                                      int(h),
                                                      int(m),
                                                      int(s))
    return timelapsed

def get_metadata(song, path):
    default_cover_path=settings.STATIC_URL+'albumCover/cdp.png'
    metadata={"cover":default_cover_path,
                        "album": "", "title": "", "artist": "","genre": "", 
                        "release": "","duration": "00:00","lyrics":"" }
    if song and path:
        audiofile = eyed3.load(path)
        # pprint(vars(audiofile.tag))

        if audiofile.info and audiofile.info.time_secs:
            metadata["duration"]=duration_from_seconds(audiofile.info.time_secs)[-5:]
            print("duration: %s" % duration_from_seconds(audiofile.info.time_secs)[-5:])

        if audiofile.tag:
            # 구글 스토리지에 앨범 커버를 저장함
            if audiofile.tag.images:
                for image in audiofile.tag.images:
                    coverName=audiofile.tag.title or song.name.split(".")[0]
                    path_on_cloud = gsCoverFolder+"/"+coverName +".jpg"
                    storage.child(path_on_cloud).put(image.image_data)

                    metadata["cover"] = storage.child(
                        path_on_cloud).get_url(user['idToken'])
        
            # 메타데이터 추출
            metadata["album"]=audiofile.tag.album or ""
            metadata["title"]=audiofile.tag.title or song.name
            metadata["artist"]=audiofile.tag.artist or ""
            metadata["release"]=audiofile.tag.getBestDate()  or ""

            if audiofile.tag.genre and str(audiofile.tag.genre).split(")") and str(audiofile.tag.genre).split(")")[1]:
                metadata["genre"]=str(audiofile.tag.genre).split(")")[1]

            if audiofile.tag.lyrics and audiofile.tag.lyrics[0] and audiofile.tag.lyrics[0].text:
                metadata["lyrics"]=audiofile.tag.lyrics[0].text 
                print("lyrics: %s" % audiofile.tag.lyrics[0].text)

            # 콘솔에 추출한 태그 정보 출력
            print("------------------------------ 태그 정보 ------------------------------")
            print("album: %s" % audiofile.tag.album)
            print("title: %s" % audiofile.tag.title)
            print("artist: %s" % audiofile.tag.artist)
            print("genre: %s" % audiofile.tag.genre)
            print("release: %s" % audiofile.tag.getBestDate())
            print("------------------------------------------------------------------------")

            # for image in audiofile.tag.images:
            #     image_file = open(settings.STATICFILES_DIRS[0]+'/covers/'+song.name, "wb")
            #     # print("Writing image file: {0} - {1}({2}).jpg".format(artist_name, album_name, image.picture_type))
            #     image_file.write(image.image_data)
            #     image_file.close()

    return metadata


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
                # 구글 파이어베이스 스토리지에 음악파일 업로드하기
                path_on_cloud = gsFileFolder+"/"+song.name #  업로드 경로 설정

                # 업로드 하는데 시간 존나 오래 걸림 (5~6초) => 파일 압축이 필요함
                GS_upload_time = time.time()
                storage.child(path_on_cloud).put(song)
                print("--- Google Upload  Time: %s seconds ---" % (time.time() - GS_upload_time))

                metadata_start_time = time.time()
                metadata = get_metadata(song, song.temporary_file_path())
                print("--- MetaData Extracted Time: %s seconds ---" % (time.time() - metadata_start_time))
             
                # DB에 음악파일 저장
                DB_start_time = time.time()
                audioFile = AudioFile(cover=metadata["cover"], album=metadata["album"], title=metadata["title"], 
                                                    artist=metadata["artist"], genre=metadata["genre"],
                                                    release=metadata["release"], duration=metadata["duration"], lyrics=metadata["lyrics"], 
                                                     cloudSrc=storage.child(path_on_cloud).get_url(user['idToken']))
                
                audioFile.save()
                print("--- DB Time: %s seconds ---" % (time.time() - DB_start_time))
                print(song.name + ' just saved in db :)')
                print('\n')

    print("--- Execute Time: %s seconds ---" % (time.time() - start_time))

    # 파일저장만 하면 되기 때문에 return 값이 없음
    return redirect('mp3:home')
