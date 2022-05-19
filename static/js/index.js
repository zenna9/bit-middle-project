function change(idx){
    console.log(idx);
    var add = document.getElementById('zen_calender').value;
    window.location.pathname = 'm/'+idx+'/'+add;
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
function gosubmit() {
  console.log('접근은 함');
  let dd = document.getElementById('form_to_upload');
  console.log(dd);
  dd.submit();
}