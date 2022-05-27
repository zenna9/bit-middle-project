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
var arr = document.getElementById('idlist').innerText;
// function letsdoidcheck(arr){
document.getElementById("zen-checkbtn").onclick=function(){
    // console.log("진입")
    console.log("어레이리스트는",arr);
    let yourid = String(document.idcheck.inputid.value);
    if (arr.indexOf("'"+yourid+"'")>=0) {
        console.log("입력한 아이디는",yourid);
        console.log(arr.indexOf("'"+yourid+"'"));
        hideordisplay(['zen-impos1'],['zen-impos2','zen-possi1', 'zen-possi2'])
        
    } else if (yourid.length <=3) {
        // document.getElementById('zen-impos2').style.display = 'block';
        hideordisplay(['zen-impos2'],['zen-impos1','zen-possi1', 'zen-possi2'])
    } else {
        hideordisplay(['zen-possi1', 'zen-possi2'],['zen-impos1','zen-impos2'])
        // document.getElementById('zen-possi1').style.display = 'block';
        // document.getElementById('zen-possi2').style.display = 'block';
    }
}

document.getElementById("zen-possi2").onclick=function(){
    willbeyourid= document.getElementById('inputid').value;
    document.getElementById('username').value = willbeyourid
    document.getElementById('dimmed').style.display = 'none';
}
