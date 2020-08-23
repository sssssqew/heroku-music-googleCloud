import pyrebase # 구글 파이어베이스

def configGoogFirebaseStroage():
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
    # 구글 스토리지 초기화
  firebase = pyrebase.initialize_app(config)
  auth = firebase.auth()
  storage = firebase.storage()
  user = auth.sign_in_with_email_and_password(
      "syleemomo@gmail.com", "rkrrlska7496ab@")

  # auth.create_user_with_email_and_password(email, password) # 이메일 생성
  storageInfos={"storage":storage, "user":user }

  return storageInfos