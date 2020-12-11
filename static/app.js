api_key='15b5132e550555979a53ba7eec9012ca' //api key is free and info is accessable to everyone so no need to hide it

const $yes = document.getElementById("yes");
const $no = document.getElementById("no");
let $title = document.getElementById("title");
let $overview = document.getElementById("overview");
let $release_date = document.getElementById("release_date");
let $original_language = document.getElementById("original_language");
let $poster_path = document.getElementById("backdrop_path");
let $current_user = document.getElementById("current_user");
let user1 = [];
let user2 = [];
let pagesCompleted = 0;
let choicesMade = 0;
let user1Yes = [];
let user2Yes = [];
let upper_bound = 300;

class Session {
    constructor(user1, user2){
        this.user1 = user1;
        this.user2 = user2;
        this.currUser = user1;
    };

    switchUsers(){
        this.currUser = this.currUser === this.user1 ? this.user2 : this.user1;
    }
}
// Set up new session class
let session = new Session(user1, user2)

function checkCurrentUser(){
    if ($current_user.innerHTML == 'Current User: #1'){
        $(":button").prop('disabled',true);
        $($current_user).html("SWITCH USERS!!!")
        setTimeout(function(){
           // enable click after 2 seconds
           $("button").prop('disabled',false);
           $($current_user).html("Current User: #2")
        },2000); // 2 second delay
    } else if ($current_user.innerHTML == 'Current User: #2'){
        $(":button").prop('disabled',true);
        $($current_user).html("SWITCH USERS!!!")
        setTimeout(function(){
           // enable click after 2 seconds
           $("button").prop('disabled',false);
           $($current_user).html("Current User: #1")
        },2000); // 2 second delay
    }
}

function redirectIndecisive(){
    window.location.href = "/session/stopped";
    return
}

function fillPage(){
    user = session.currUser
    $($poster_path).attr("src", `https://image.tmdb.org/t/p/w500${user[0].poster_path}`);
    $($title).html(`${user[0].title}`);
    $($original_language).html(`<b>Original language:</b> ${user[0].original_language}`);
    $($release_date).html(`First aired on ${user[0].release_date}`);
    $($overview).html(`${user[0].overview}`);
}

function refillLists(){
    pagesCompleted++;
    if (pagesCompleted === (upper_bound - 1) || pagesCompleted > 99){
        redirectIndecisive();
    }else{
        createLink(randomNum);
    }
}

function compareArrays(arr1, arr2) { 
    return arr1.some(item => arr2.includes(item)) 
}

function randomUniqueNum(upper_bound){
    let limit = 100,
    amount = 100,
    lower_bound = 1,
    unique_random_numbers = [];

    if (amount > limit) limit = amount; //Infinite loop if you want more unique
                                        //Natural numbers than exist in a
                                        // given range
    while (unique_random_numbers.length < limit) {
        let random_number = Math.floor(Math.random()*(upper_bound - lower_bound) + lower_bound);
        if (unique_random_numbers.indexOf(random_number) == -1) { 
            // Yay! new random number
            unique_random_numbers.push( random_number );
        }
    }
    return unique_random_numbers;

}

let randomNum = randomUniqueNum(upper_bound);

function redirect() {
    window.location.href = "/session/end";
    return
 }

async function getResponse(link){
    response = await axios.get(link);
    setUpArrays(response);
}

function setUpArrays(response){
    if (response.data.results == 0){
        upper_bound = response.data.total_pages;
        randomNum = randomUniqueNum(upper_bound);
        createLink(randomNum)
    }
    for (let i = 0; i < response.data.results.length; i++){
        results = {};
        results['title'] = response.data.results[i].title || response.data.results[i].name;
        results['release_date'] = response.data.results[i].release_date || response.data.results[i].first_air_date;
        results['original_language'] = response.data.results[i].original_language;
        results['overview'] = response.data.results[i].overview || "None...";
        results['poster_path'] = response.data.results[i].poster_path || response.data.results[i].backdrop_path || "https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg";
        results['id'] = response.data.results[i].id;
        session.user1.push(results);
        session.user2.push(results);
    }
    shuffleArray(session.user1)
    shuffleArray(session.user2)
    sessionStorage.setItem('current_user', 'user1')
    fillPage()
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        let temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    return array
}

// When no is clicked, take the displayed show and delete it
$($no).on("click",function(evt){
    evt.preventDefault();
    if (session.user1.length == 0 && session.user2.length == 1 ){
        refillLists()
    }
    user = session.currUser;
    user.shift();
    choicesMade++;
    if(choicesMade > 4 || user.length == 0){
        session.switchUsers();
        choicesMade = 0;
        checkCurrentUser();
        fillPage();
    }
    fillPage() 
});

// When yes is clicked, take the displayed show and save it to a yes list, then delete it
$($yes).on("click",function(evt){
    evt.preventDefault();
    if (session.user1.length === 0 && session.user2.length === 1){
        refillLists()
    }
    user = session.currUser;
    if (session.currUser == session.user1){
        user1Yes.push(user[0]);
    } else {
        user2Yes.push(user[0]);
    }
    let match = compareArrays(user1Yes, user2Yes)
    if (match != false){
        localStorage.setItem('title_id', user[0].id)
        redirect()
    }
    user.shift();
    choicesMade++;
    if(choicesMade > 4 || user.length == 0){
        session.switchUsers();
        choicesMade = 0;
        checkCurrentUser();
        fillPage();
    }
    fillPage()
});

function createLink(randomNum){
    let genre = localStorage.getItem("genre");
    let sessionType = localStorage.getItem("type");
    if (sessionType == 'tv'){
        link = `https://api.themoviedb.org/3/discover/tv?api_key=${api_key}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=${randomNum[pagesCompleted]}&with_genres=${genre}`
        checkGenre(genre, link);
        return
    }
    if (sessionType == 'movie'){
        link = `https://api.themoviedb.org/3/discover/movie?api_key=${api_key}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=${randomNum[pagesCompleted]}&with_genres=${genre}`
        checkGenre(genre, link);
        return
    }
}

function checkGenre(genre, str){
    if (genre == 'None'){
        finished_link = link.replace("&with_genres=None", "");
        data = getResponse(finished_link);

        setUpArrays(data);
    }
    else {
        data = getResponse(link);
        setUpArrays(data);
    }
}

$(document).ready(function() { 
    createLink(randomNum)
})