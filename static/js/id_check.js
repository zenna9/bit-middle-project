// 채은 : 아이디 중복체크 팝업 띄우는 js
function hideordisplay(display, hide){
    let t1 = display;
    let f1 = hide;
    for (let i = 0; i < t1.length; i++) {
      t = document.getElementById(t1[i]);
      t.style.display = 'block'
    }
    for (let i = 0; i < f1.length; i++) {
        f = document.getElementById(f1[i]);
        f.style.display = 'none';
    }
}

// 채은 : 아이디 중복체크하는 js
var arr = document.getElementById('idlist').innerText;
document.getElementById("zen-checkbtn").onclick=function(){
    let yourid = String(document.idcheck.inputid.value);
    if (arr.indexOf("'"+yourid+"'")>=0) {
        hideordisplay(['zen-impos1'],['zen-impos2','zen-possi1', 'zen-possi2'])
    } else if (yourid.length <=3) {
        hideordisplay(['zen-impos2'],['zen-impos1','zen-possi1', 'zen-possi2'])
    } else {
        hideordisplay(['zen-possi1', 'zen-possi2'],['zen-impos1','zen-impos2'])
    }
}
//채은 : 중복체크 끝난 아이디를 회원가입 폼에 다시 가져다주는 js
document.getElementById("zen-possi2").onclick=function(){
    willbeyourid= document.getElementById('inputid').value;
    document.getElementById('username').value = willbeyourid
    document.getElementById('dimmed').style.display = 'none';
}
