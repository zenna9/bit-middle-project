// document.getElementById('currentDatetime').value = new Date().toISOString().slice(0, -1);

// document.getElementById('currentDate').value = new Date().toISOString().substring(0, 10);

function date(today){
    let day = date(today);
    document.getElementById('currentDate').value = day.toISOString().substring(0, 10);
}

function dopercent(idinput, sons,mother){
    var idinput = document.getElementById(idinput).style
    let son = sons ;
    let mom = mother ;
    let per = son/mom*100+"%";
    idinput.width = per;
    console.log(idinput)
}

function getvalue(){
    var idx = document.getElementById('idx').value;
    var datex = document.getElementById('datex').value;
    var urll = 'm/'+idx+'/'+datex;
    console.log(idx);
    return urll;
}

function zen_hideorseek(what) {
    target_x = document.getElementById(what);
    target_x.style.display = 'block';
}


