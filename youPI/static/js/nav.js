window.get = function(url) {
    return fetch(url, {method: "GET"});
}
function doFetch(){
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