window.get = function(url, data) {
    return fetch(url, {method: "GET"});
  }
function resetExpiredToken(){
    const resetENDPOINT = "/reset"
    fetch(resetENDPOINT).then(()=>{
        console.log("Successfully reseted");
    }).catch((e)=>{
        console.log(e);
    })
}