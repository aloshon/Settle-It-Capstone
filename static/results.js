let $title = document.getElementById("title");
let $overview = document.getElementById("overview");
let $release_date = document.getElementById("release_date");
let $original_language = document.getElementById("original_language");
let $poster_path = document.getElementById("backdrop_path");
let titleId = localStorage.getItem('title_id')

async function getData(){
    type = localStorage.getItem("type")
    response = await axios.get(`https://api.themoviedb.org/3/${type}/${titleId}?api_key=15b5132e550555979a53ba7eec9012ca&language=en-US`);
    fillPage(response)
}

function fillPage(response){
    $($poster_path).attr("src", `https://image.tmdb.org/t/p/w500${response.data.poster_path || response.data.backdrop_path}`);
    $($title).html(`<h1>${response.data.title || response.data.name || "No Title!"}</h1>`);
    $($original_language).html(`<h2><b>Original language:</b> ${response.data.original_language}</h2>`);
    $($release_date).html(`<h3>First Aired in ${response.data.release_date || response.data.first_air_date}</h3>`);
    $($overview).html(`<h6> ${response.data.overview}</h6>`);
    localStorage.setItem("last_session", `${response.data.title || response.data.name || "No Title!"}`)
}

$(document).ready(function() { 
    getData()
})