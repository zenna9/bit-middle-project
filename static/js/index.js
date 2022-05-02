function change(idx){
    console.log(idx);
    var add = document.getElementById('zen_calender').value;
    window.location.pathname = 'm/'+idx+'/'+add;
}

function onload(date, perdan){
    document.getElementById('zen_calender').value=date;
    tan = document.getElementById('tan').style.width;
    console.log(date)
    console.log(perdan)





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
  
  tag()

// function getpercent(per) {
//     let pers = per;
//     console.log(per);
//     // let thiss = document.getElementById(tan).style;
//     // thiss.width = pers;
//     // console.log('pers');
// }
