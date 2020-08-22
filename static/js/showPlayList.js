// 음악리스트 행을 생성
tableRow = document.createElement("tr");
musicList.appendChild(tableRow);

// 앨범커버 생성
coverColumn = document.createElement("td");
cover = document.createElement("img");

cover.setAttribute("width", "50");
cover.setAttribute("height", "auto");
cover.className = "img-circle albumart";
cover.src = coverImg;
cover.alt = artistInfo + " - " + titleInfo;
cover.lyrics = lyrics;
cover.value = cnt;
cover.url = url;
cover.clicked = true;
cover.addEventListener("click", popupCDPlayer, false);

coverColumn.appendChild(cover);
tableRow.appendChild(coverColumn);

// 앨범 커버를 제외한 나머지 정보 표시
album = document.createElement("td"); // album
album.innerText = albumInfo;
album.className = "no-td";
tableRow.appendChild(album);

title = document.createElement("td"); // title
title.innerText = titleInfo;
tableRow.appendChild(title);

artist = document.createElement("td"); // artist
artist.innerText = artistInfo;
artist.className = "no-td";
tableRow.appendChild(artist);

genre = document.createElement("td"); // genre
genre.innerText = genreInfo;
genre.className = "no-td";
tableRow.appendChild(genre);

release = document.createElement("td"); // release
release.innerText = releaseInfo;
release.className = "no-td";
tableRow.appendChild(release);

time = document.createElement("td"); // time
time.innerText = duration;
time.className = "no-td";
tableRow.appendChild(time);

// 가사, 재생, 좋아요 버튼  + Progress bar 생성
for (var j = 0; j < 3; j++) {
  buttons = document.createElement("td");

  if (j == 0) {
    lyricsButton = document.createElement("input");
    lyricsButton.type = "button";
    lyricsButton.className = "btn btn-info btn-sm";
    lyricsButton.value = "Lyrics";

    buttons.className = "no-td";
    buttons.appendChild(lyricsButton);
  } else if (j == 1) {
    playButton = document.createElement("input");
    playButton.type = "button";
    playButton.className = "btn btn-warning btn-sm";
    playButton.value = "Play";
    playButton.id = cnt;
    playButton.url = url;
    playButton.addEventListener("click", playMusic, false);

    buttons.appendChild(playButton);

    // progress bar 생성 (부트스트랩 이용)
    playButton = document.createElement("div");
    playButton.className = "progress";
    bar = document.createElement("div");
    bar.className = pClassName;
    bar.role = "progressbar";
    bar.ariaValuenow = "";
    bar.ariaValuemin = "0";
    bar.ariaValuemax = "100";
    bar.style.width = "0%";
    bar.duration = duration;

    playButton.appendChild(bar);
    buttons.appendChild(playButton);
  } else if (j == 2) {
    buttons.className = "no-td";
    // "좋아요" 이미지 생성
    likeButton = document.createElement("img");
    likeButton.src = likeImg;
    likeButton.setAttribute("width", "25");
    likeButton.setAttribute("height", "auto");

    buttons.appendChild(likeButton);

    // 재생횟수 표시
    likeButton = document.createElement("p");
    likeButton.className = "favor";
    likeButton.innerText = 0;
    likeButton.value = cnt;

    buttons.appendChild(likeButton);
  }

  tableRow.appendChild(buttons);
}

cnt = cnt + 1;
