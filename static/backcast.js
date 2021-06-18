// function toggleHourlyShow() {
//     console.log("HIIIII")
//     var x = document.getElementsByClassName("hour_by_hour_box");
//     for (let div in x){
//             console.log(x[div].style.display)
//             if (x[div].style.display == "none") {
//                 console.log("block inline")
//                 x[div].style.display = "block-inline";
//                 } else {
//                     console.log("none")
//                 x[div].style.display = "none";
//                 }
//             }

//   }

$("#hide").click(function(){
    console.log("hi")
    $(".hour_by_hour_box").hide();
  });
  
  $("#show").click(function(){
    $(".hour_by_hour_box").show();
  });