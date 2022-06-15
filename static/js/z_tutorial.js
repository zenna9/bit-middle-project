const slides = document.querySelector(".slides");
const leftbtn = document.querySelector('.toleft');
const rightbtn=document.querySelector('.toright');
let slideNo = 0;
rightbtn.addEventListener("click",function goSlide(){
    console.log('진입')
    console.log(slideNo, typeof(slideNo));
    if (slideNo<4){
        slideNo += 1;
        console.log(slideNo);
        document.querySelector(`#slide${slideNo}`).style.transform=`translateX(${-100.7*slideNo}%)`;
    
        console.log(`#slide${slideNo}`,document.querySelector(`#slide${slideNo}`).transform);
        }
    }
);
leftbtn.addEventListener("click",function goSlide(){
    if(slideNo>0){
        console.log('진입')
        console.log(slideNo, typeof(slideNo));
        slideNo -= 1;
        console.log(slideNo);
        const whatwillchange=document.querySelector(`#slide${slideNo+1}`).style;
        whatwillchange.transform=`translateX(0%)`;
        console.log(`#slide${slideNo}`,document.querySelector(`#slide${slideNo}`).transform);
        }
    }
);