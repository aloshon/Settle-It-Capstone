let $tv_btn = document.getElementById("tv_btn");
let $movie_btn = document.getElementById("movie_btn");
let $startSessionBtn = document.getElementById("session_start");
let $last_settled = document.getElementById("last_settled");
let $genre = document.getElementById("genre");
api_key='15b5132e550555979a53ba7eec9012ca' // api key for getting movie data

function lastSession(){
    title = localStorage.getItem("last_session");
    $($last_settled).html(`Last session ended with:<h2>${title}</h2>`);
}

function getInputs(){
    localStorage.setItem("genre", $genre.value);
}

function toggleNav() {
    var x = document.getElementById("myLinks");
    if (x.style.display === "block") {
      x.style.display = "none";
    } else {
      x.style.display = "block";
    }
}

$(document).ready(function() { 
    lastSession()
});

// Changes color of like button when clicked
$("#review-like button").click(function(){
    if($(this).hasClass("btn-primary")){
        $(this).removeClass("btn-primary");
        $(this).toggleClass("btn-secondary");
    } else if($(this).hasClass("btn-secondary")){
        $(this).removeClass("btn-secondary");
        $(this).toggleClass("btn-primary")
    }
})

// These are for when user click on one of the session-starting buttons in the homepage
try {
    $($startSessionBtn).on("click",getInputs);
    $movie_btn.addEventListener("click", localStorage.setItem("type", "movie"));
    $tv_btn.addEventListener("click", localStorage.setItem("type", "tv"));
  }
  catch(err) {
    console.log("Dont' worry, everything ran I just couldn't find the buttons!")
}
