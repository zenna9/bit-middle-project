function change(idx){
    console.log(idx);
    var add = document.getElementById('zen_calender').value;
    window.location.pathname = 'm/'+idx+'/'+add;
}

function onload(date){
    document.getElementById('zen_calender').value=date;
}
