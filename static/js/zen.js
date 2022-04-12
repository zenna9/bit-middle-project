// document.getElementById('currentDatetime').value = new Date().toISOString().slice(0, -1);

document.getElementById('currentDate').value = new Date().toISOString().substring(0, 10);

function date(today){
    let day = date(today);
    document.getElementById('currentDate').value = day.toISOString().substring(0, 10);
}
function dopercent(sons,mother){
    let son = sons ;
    let mom = mother ;
    let per = son/mom
    console.log(per)
    return this.style.width = per
}
function zenna(id, sonn, momm){
    let son = sonn;
    let mom = momm;
    let who = document.getElementById(id);
    console.log(son/mom, "구해줘..") ;


}