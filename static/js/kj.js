function change_cal(idx){
    var cal_date = document.getElementById('kj_calender').value;
    window.location.pathname = 'm/'+ idx +'/'+ cal_date +'/'+ 'mypage';
}
