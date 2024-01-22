
function getQuestion(id){
    window.location.href='/quiz?quiz_id='+id   
}

// function getfunction(id){
//     fetch('/delete-note',{
//         method:'POST',
//         body:JSON.stringify({quiz_id:id}),
//     }).then((res)=>{
//         window.location.href='/'
//     })
// }