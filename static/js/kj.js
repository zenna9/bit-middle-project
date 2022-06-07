function change_cal(idx){
    console.log(idx);
    var cal_date = document.getElementById('kj_calender').value;
    window.location.pathname = 'm/ain/'+ cal_date +'/'+ 'mypage';
}
