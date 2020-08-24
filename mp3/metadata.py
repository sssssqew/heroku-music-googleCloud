import eyed3 # 태그 추출
from django.conf import settings
from .googleConfig import configGoogFirebaseStroage

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

def get_metadata(songName, path):
    storageInfos=configGoogFirebaseStroage()
    user=storageInfos["user"]
    gsCoverFolder = "covers"
    default_cover_path=settings.STATIC_URL+'albumCover/cdp.png'
    metadata={"cover":default_cover_path,
                        "album": "", "title": "", "artist": "","genre": "", 
                        "release": "","duration": "00:00","lyrics":"" }

    if path:
        audiofile = eyed3.load(path)
        # pprint(vars(audiofile.tag))
        if audiofile:

            if audiofile.info and audiofile.info.time_secs:
                metadata["duration"]=duration_from_seconds(audiofile.info.time_secs)[-5:]
                print("duration: %s" % duration_from_seconds(audiofile.info.time_secs)[-5:])

            if audiofile.tag:
                # 구글 스토리지에 앨범 커버를 저장함
                if audiofile.tag.images:
                    for image in audiofile.tag.images:
                        coverName=audiofile.tag.title or songName
                        path_on_cloud = gsCoverFolder+"/"+coverName +".jpg"
                        storageInfos["storage"].child(path_on_cloud).put(image.image_data)

                        metadata["cover"] = storageInfos["storage"].child(
                            path_on_cloud).get_url(user['idToken'])
            
                # 메타데이터 추출
                metadata["album"]=audiofile.tag.album or ""
                metadata["title"]=audiofile.tag.title or songName
                metadata["artist"]=audiofile.tag.artist or ""
                metadata["release"]=audiofile.tag.getBestDate()  or ""

                if audiofile.tag.genre:
                    metadata["genre"]=audiofile.tag.genre # 인덱스 오류 자주남 (에러처리)

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
                #     image_file = open(settings.STATICFILES_DIRS[0]+'/covers/'+songName, "wb")
                #     # print("Writing image file: {0} - {1}({2}).jpg".format(artist_name, album_name, image.picture_type))
                #     image_file.write(image.image_data)
                #     image_file.close()

    return metadata