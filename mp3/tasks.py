from __future__ import absolute_import, unicode_literals
from celery import shared_task,current_task
from celery.result import AsyncResult

import os
import time
from .metadata import get_metadata
from .models import AudioFile
from .googleConfig import configGoogFirebaseStroage

# @shared_task
# def add(x, y):
#   print("inside tasks .............")
#   print(x)
#   return x + y

# @shared_task 
# 로컬에서만 celery 테스트하기
 # 구글 파이어베이스 스토리지에 음악파일 업로드하기
def uploadSongToGoogleStorage(songInfos):
  storageInfos=configGoogFirebaseStroage()
  print("storage info =>" + str(storageInfos["storage"]))
  print("song path =>"+songInfos["savedFilePath"])
  # print("task id =>"+current_task.request.id)

  # 변수 초기화
  gsFileFolder = "songs"
  path_on_cloud = gsFileFolder+"/"+songInfos["name"] #  업로드 경로 설정

  # 업로드 하는데 시간 존나 오래 걸림 (5~6초) => 파일 압축이 필요함
  # 히로쿠에 올리니까 좀 빨라짐 (1~2초)
  GS_upload_time = time.time()
  storageInfos["storage"].child(path_on_cloud).put(songInfos["savedFilePath"])
  print("--- Google Upload  Time: %s seconds ---" % (time.time() - GS_upload_time))

  metadata_start_time = time.time()
  metadata = get_metadata(songInfos["name"] ,songInfos["savedFilePath"])
  print(metadata["title"])
  print("--- MetaData Extracted Time: %s seconds ---" % (time.time() - metadata_start_time))

  # 임시파일이므로 디스크 용량을 차지하니까 지워줌
  os.remove(songInfos["savedFilePath"])

  # DB에 음악파일 저장
  DB_start_time = time.time()
  audioFile = AudioFile(cover=metadata["cover"], album=metadata["album"], title=metadata["title"], 
                                      artist=metadata["artist"], genre=metadata["genre"],
                                      release=metadata["release"], duration=metadata["duration"], lyrics=metadata["lyrics"], 
                                        cloudSrc=storageInfos["storage"].child(path_on_cloud).get_url(storageInfos['user']['idToken']))

  audioFile.save()
  print("--- DB Time: %s seconds ---" % (time.time() - DB_start_time))
  print(songInfos["name"] + ' just saved in db :)')
  print('\n')

  # task id 를 이용하여 결과를 요청한 곳에 리턴해줌
  # res = AsyncResult(current_task.request.id)

  # 리턴값은 반드시 시리얼로 변경 가능한 (serializable) 값이어야 함 => 객체는 안됨 
  # return res
  return "succeed"


