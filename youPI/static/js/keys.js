window.get = function(url, data) {
    return fetch(url, {method: "GET"});
  }
function resetExpiredToken(){
    console.log("Resetting")
    const resetENDPOINT = "/reset"
    fetch(resetENDPOINT).then((res)=>{
        console.log(res.message);
    }).catch((e)=>{
        console.log(e);
    })
    
}