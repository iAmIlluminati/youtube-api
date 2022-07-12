window.get = function(url) {
    return fetch(url, {method: "GET"});
  }

// API KEYS FUNCTIONS 

  function resetExpiredToken(){
    console.log("Resetting")
    const resetENDPOINT = "/reset"
    fetch(resetENDPOINT).then((res)=>{
        console.log(res);
    }).catch((e)=>{
        console.log(e);
    })    
    window.location.href="/keys";
}



// DASHBOARD FUNCTIONS

function doFetch(){
    console.log("Toggling the API")
    var tog = document.getElementById("switch").checked
    const startENDPOINT = "/api"
    const stopENDPOINT = "/stop"
    if(tog){
        fetch(startENDPOINT).then((res)=>{
            console.log(res);
        }).catch((e)=>{
            console.log(e);
        })      
    }else{
        fetch(stopENDPOINT).then((res)=>{
            console.log(res);
        }).catch((e)=>{
            console.log(e);
        })
    }
}