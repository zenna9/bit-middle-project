// // document.getElementById('currentDatetime').value = new Date().toISOString().slice(0, -1);

// document.getElementById('currentDate').value = new Date().toISOString().substring(0, 10);

// function date(today){
//     let day = date(today);
//     document.getElementById('currentDate').value = day.toISOString().substring(0, 10);
// }
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

function hideorseek(what) {
    target_x = document.getElementById(what);
    target_x.style.display = 'block';
}


$('.circle1').circleProgress({
    value: 0.8,
    fill: {
        gradient: [
            ['orange', 1],
            ['pink', 1]
        ],
        gradientAngle: Math.PI / 4
    }
}).on('circle-animation-progress', function(event, progress, stepValue) {
    $(this).find('b').text(stepValue.toFixed(2).substr(1) * 100 + "% ");
});


$('.circle2').circleProgress({
    value: 0.2,
    fill: {
        gradient: [
            ['blue', 1],
            ['pink', 1]
        ],
    }
}).on('circle-animation-progress', function(event, progress, stepValue) {
    $(this).find('b').text(stepValue.toFixed(2).substr(1) * 100 + "% ");
});




$('.circle3').circleProgress({
    value: 0.5,
    fill: {
        gradient: [
            ['yellow', 1],
            ['pink', 1]
        ],
        gradientAngle: Math.PI / 4
    }
}).on('circle-animation-progress', function(event, progress, stepValue) {
    $(this).find('b').text(stepValue.toFixed(2).substr(1) * 100 + "% ");
});
$('.circle4').circleProgress({
    value: 0.5,
    fill: {
        gradient: [
            ['yellow', 1],
            ['pink', 1]
        ],
        gradientAngle: Math.PI / 4
    }
}).on('circle-animation-progress', function(event, progress, stepValue) {
    $(this).find('b').text(stepValue.toFixed(2).substr(1) * 100 + "% ");
});