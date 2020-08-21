console.log("server start");
var loadStart = new Date().getTime();

// 전역으로 사용할 객체 (element)
var audio = document.getElementById("musicPlayer"); // 현재곡 객체
var fileSelect = document.getElementById("fileSelect");
var musicFiles = document.getElementById("musicFiles"); // 파일입력 객체
var pClassName = "progress-bar progress-bar-warning"; // Progress bar 클래스명
var player = null;
var prevID = -1; // 이전곡 ID
var pEl; // 이전곡 객체
var cnt = 0; // 곡의 수 카운트
var where = -1; // 0 : 재생버튼 , 1 : CD 플레이어
var isEnd = false;
var prevClicked = true;

/**************************  드래그앤 드롭 기능  ***********************/

var dropzone = document.getElementById("dropzone");
dropzone.addEventListener("dragenter", dragenter, false);
dropzone.addEventListener("dragover", dragover, false);
dropzone.addEventListener("dragleave", dragleave, false);
dropzone.addEventListener("drop", drop, false);

function dragenter(e) {
  e.stopPropagation();
  e.preventDefault();
}

function dragover(e) {
  e.stopPropagation();
  e.preventDefault();

  dropzone.className = "hover";
}

function dragleave(e) {
  e.stopPropagation();
  e.preventDefault();

  dropzone.className = "";
}

function drop(e) {
  e.stopPropagation();
  e.preventDefault();

  var dt = e.dataTransfer;
  var files = dt.files;

  handleFiles(files);
}

/**************************  앨범 클릭시 CD Player 재생 ***********************/

// CD 플레이어 재생에 필요한 객체
var modal = document.getElementById("myModal");
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
var lyricsContent = document.getElementById("lyricsContent");
var clickedOrNOt = false;

modal.addEventListener("click", controlSongList);
modal.addEventListener("mouseover", showControlButton);

// 이전곡, 다음곡 재생 안내
function showControlButton(e) {
  var x = e.clientX;
  var y = e.clientY;
  var w = window.innerWidth;
  var hw = parseInt(w / 2);

  if (!clickedOrNOt) {
    if (x >= hw) {
      // console.log("right");
      modal.setAttribute("title", "배경화면 오른쪽 절반 클릭시 다음곡 재생");
    } else {
      // console.log("left");
      modal.setAttribute("title", "배경화면 왼쪽 절반 클릭시 이전곡 재생");
    }
  }
}

// CD 플레이어 초기화
function CDinit(id) {
  modalImg.src = id.src;
  modalImg.alt = id.alt;
  modalImg.value = id.value;
  modalImg.url = id.url;
  modalImg.lyrics = id.lyrics;

  // 가사 변경
  lyricsContent.innerText = id.lyrics;
  captionText.innerHTML = id.alt;
}

// 현재 재생중인 플레이어만 계속 돌아가게 하기
function spinCD(id) {
  if (id.value != prevID) {
    modalImg.clicked = true;
    modalImg.className = "modal-content";
  } else {
    if (!isEnd) {
      modalImg.clicked = prevClicked;
      modalImg.className += " spinning";
    }
  }
}

// 이전곡, 다음곡 재생 컨트롤
function controlSongList(e) {
  var art;
  var x = e.clientX;
  var y = e.clientY;
  var w = window.innerWidth;
  var hw = parseInt(w / 2);

  // 앨범 커버가 아니라 여백을 클릭했을 때
  if (!clickedOrNOt) {
    if (x >= hw) {
      console.log("right");
      if (modalImg.value + 1 <= cnt - 1) {
        art = document.getElementsByClassName("img-circle albumart")[
          modalImg.value + 1
        ];
        console.log(art); // 다음곡
        transfer();
      } else {
        console.log("this song is last");
      }
    } else {
      console.log("left");
      if (modalImg.value - 1 >= 0) {
        art = document.getElementsByClassName("img-circle albumart")[
          modalImg.value - 1
        ];
        console.log(art); // 이전곡
        transfer();
      } else {
        console.log("this song is first");
      }
    }

    function transfer() {
      CDinit(art);

      // 현재 재생중인 플레이어만 계속 돌아가게 하기
      if (where != 0) spinCD(art);
    }
  } else {
    clickedOrNOt = false;
  }
}

// CD 플레이어 화면표시
function popupCDPlayer(e) {
  modal.style.display = "block";

  CDinit(e.target);

  // 현재 재생중인 플레이어만 계속 돌아가게 하기
  if (where != 0) spinCD(e.target);
}

var timer = 0;
var delay = 400;
var prevent = false;

// 더블클릭시 팝업화면 사라짐
modalImg.ondblclick = function(e) {
  clearTimeout(timer);
  prevent = true;
  modal.style.display = "none";
};

// Play 버튼과 Progress bar 상태 초기화
function retrieve() {
  pEl = document.getElementById(prevID);
  pEl.value = "Play";

  prevProgress = document.getElementsByClassName(pClassName)[prevID];
  prevProgress.style.width = "0";
}

// 더블클릭시 클릭 이벤트도 같이 실행되는데 이를 막기위해 타이머 설정함
modalImg.onclick = function(e) {
  clickedOrNOt = true;
  timer = setTimeout(function() {
    if (!prevent) {
      if (prevID != e.target.value) {
        // 이전곡과 다른곡 재생시
        console.log("You played new song !!");
        audio.src = e.target.url;

        if (prevID != -1) {
          // Play 버튼으로 노래를 듣다가 CD Player로 다른 음악을 재생시
          if (where == 0) {
            modalImg.clicked = true;
            retrieve();
            console.log(
              "You played the other song with play button right before"
            );

            // 이전에 CD Player 로 노래를 듣다가 이전곡 다음곡 재생시
          } else {
            // pEl = document.getElementById(prevID);
            // pEl.clicked = true;
          }
        }
      } else {
        // Play 버튼에서 나와서 같은 노래를 CD Player로 다시 틀었을 경우
        if (where == 0) {
          modalImg.clicked = true;
          audio.src = e.target.url;
          retrieve();
          console.log("You played the same song with play button right before");
        }
      }

      // Play에서  Pause 로 갈수도 있고 다시 Play 버튼을 누를수도 있음
      if (e.target.clicked == true) {
        audio.play();
        e.target.clicked = false;
        prevClicked = e.target.clicked;
        console.log("play");

        // 노래가 끝나서 새로 재생할 때
        audio.onended = function() {
          console.log("music really ended !!");
          e.target.clicked = true;

          e.target.className = "modal-content";
          isEnd = true;
        };

        // 새로운 곡을 재생하면 좋아요 1 증가
        if (audio.currentTime == 0) {
          var like = document.getElementsByClassName("favor")[e.target.value];
          like.innerText = parseInt(like.innerText) + 1;

          e.target.className += " spinning";
          isEnd = false;
        }
      } else if (e.target.clicked == false) {
        audio.pause();
        e.target.clicked = true;
        prevClicked = e.target.clicked;
        console.log("Pause");
      }

      prevID = e.target.value; // 이전 노래의 객체 저장
      where = 1;
    }
    prevent = false;
  }, delay);
};

/************************** Play 버튼 클릭시 음악 재생 ***********************/

function playMusic(e) {
  progress = document.getElementsByClassName(pClassName)[e.target.id];

  if (prevID != e.target.id) {
    // 이전곡과 다른곡 재생시
    console.log("You played new song !!");
    audio.src = e.target.url;

    if (prevID != -1) {
      // CD Player 버튼으로 노래를 듣다가 Play 버튼으로 다른 음악을 재생시
      if (where == 1) {
        // CD Player 로 듣다가 Play 버튼으로 다른 음악을 재생시
        modalImg.clicked = true;
        modalImg.className = "modal-content";

        console.log("You played the other song with cd player right before");
      } else {
        // Play 버튼으로 다른 음악을 재생시
        retrieve();
      }
    }
  } else {
    // CD Player에서 나와서 같은 노래를 Play 버튼으로 다시 틀었을 경우
    if (where == 1) {
      audio.src = e.target.url;

      modalImg.clicked = true;
      modalImg.className = "modal-content";

      console.log("You played the same song with cd player right before");
    }
  }

  // Play에서  Pause 로 갈수도 있고 다시 Play 버튼을 누를수도 있음
  if (e.target.value == "Play") {
    audio.play();
    e.target.value = "Pause";
    console.log("play");

    // 노래가 끝나서 새로 재생할 때
    audio.onended = function() {
      console.log("music really ended !!");
      e.target.value = "Play";
    };

    // 현재까지 재생한 시간 표시
    audio.ontimeupdate = function() {
      // 버튼으로 재생한 경우만 재생위치 표시
      if (where == 0) {
        w = (audio.currentTime / audio.duration) * 100;
        progress.style.width = w + "%";
      }
    };

    // 새로운 곡을 재생하면 좋아요 1 증가
    if (audio.currentTime == 0) {
      var like = document.getElementsByClassName("favor")[e.target.id];
      like.innerText = parseInt(like.innerText) + 1;
    }
  } else if (e.target.value == "Pause") {
    audio.pause();
    e.target.value = "Play";
    console.log("Pause");
  }

  prevID = e.target.id; // 이전 노래의 객체 저장
  where = 0;
}

/**************************  파일입력을 핸들링하는 이벤트  ***********************/

function handleFiles(files) {
  var formData = new FormData($("#passData").get(0));

  for (var i = 0; i < files.length; i++) {
    var file = files[i];

    dropzone.className = "";

    // 입력파일 타입 체크 (audio 타입만 전송)
    originType = musicFiles.getAttribute("accept").split("/", 1);
    fType = file.type.split("/", 1);

    if (originType[0] != fType[0]) {
      alert("File type is not allowed." + "\n" + "file : " + file.name);
    } else {
      // 전송할 파일 추가함
      formData.append("songFile", file);
    }
  }

  // 파일을 서버로 전송함
  console.log("file transfer start");
  var uploadStart = new Date().getTime();
  var uploadSpeed = 0;

  // Ajax 방식
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/pass/", true);
  xhr.onreadystatechange = function(response) {
    if (xhr.readyState == 4) {
      if (xhr.status == 200) {
        console.log("file successfully submitted");
        console.log("page reloading...");
        location.reload();
        uploadSpeed = new Date().getTime() - uploadStart;
        console.log("upload speed..." + uploadSpeed / 1000 + " sec");
      } else {
        console.log("error occured while uploading file");
      }
    }
  };
  xhr.send(formData);
}
