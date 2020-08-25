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
