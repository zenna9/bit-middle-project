function change(idx){
    console.log(idx);
    var add = document.getElementById('zen_calender').value;
    window.location.pathname = 'm/ain/'+add;
}

function loadfunction(date, perkcal, pertan, perdan, perji){
  document.getElementById('zen_calender').value=date;
  document.getElementById('perkcal1').style.width=perkcal;
  document.getElementById('pertan').style.width=pertan;
  document.getElementById('perdan').style.width=perdan;
  document.getElementById('perji').style.width=perji;
  document.getElementById('perkcal2').style.width=perkcal;
}

// for progress tag in HTML 
function tag () {
    let progress = document.querySelector('.progressTag')
    let interval = 1
    let updatesPerSecond = 1000 / 60
    let end = progress.max * 0.8
  
    function animator () {
      progress.value = progress.value + interval
      if ( progress.value + interval < end){
        setTimeout(animator, updatesPerSecond);
      } else { 
        progress.value = end
      }
    }
  
    setTimeout(() => {
      animator()
    }, updatesPerSecond)
  }
  
// function getpercent(per) {
//     let pers = per;
//     console.log(per);
//     // let thiss = document.getElementById(tan).style;
//     // thiss.width = pers;
//     // console.log('pers');
// }
function gosubmit() { // topbar의 사진업로드 실행
  let dd = document.getElementById('form_to_upload');
  dd.submit();
}


// var obj = document.getElementById('newfood')
// obj.onclick = function(){

//   console.log("mii");
// }
function newfood() {
  document.getElementById('jikil').style.display = "inline-table";
}
function addfood(nu){
  var obj = document.getElementById(nu)
  obj.style.display="inline-table";
}

// 3-1: sidebar submit시 사진 없으면 경고하는 부분
const submitform = document.querySelector("#photoform");

submitform.addEventListener("submit",submitPhoto)

function changeFormText(ment){ // if false이면 박스에 멘트 띄우는 내용
  const formText = submitform.querySelector("#ment");
  formText.innerHTML = ment
  formText.style.backgroundColor = '#FA5882';
  formText.style.color = "#ffffff"
}

function submitPhoto(event){
  event.preventDefault();
  const imgInput = submitform.querySelector("#file").value;
  const urllen = (imgInput).indexOf(".")+1;

  //파일의 확장자 자른거
  const fileFormat = imgInput.substr(urllen,imgInput.length);

  //사용가능한 포맷 리스트
  const possibleFormat = ['bmp', 'dng', 'jpeg', 'jpg', 'mpo', 'png', 'tif', 'tiff', 'webp']
  if(imgInput=== ""){
    changeFormText("사진을 먼저 첨부해주세요");
  }else if(!(possibleFormat.includes(fileFormat))){
    changeFormText("분석 가능한 확장자 : <br>bmp, dng, jpeg, jpg, mpo, png, tif, tiff, webp");
  }else {
    submitform.submit();
  }
}
//종료 3-1