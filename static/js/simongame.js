
const startbutton = document.getElementById('start-button');
let buttons = document.querySelectorAll('button');
let squres = ['red','green','blue','yellow'];
let level = 0;
let playerPattern = [];
let timeoutIds = [];
let isShowingPattern = false;

buttons.forEach(button => {
    if (button.id !== 'start-button' && button.id !== 'play-again-button') {
        button.addEventListener('click', playerPatternFunc);
    }
});

function startGame() {
    level = 1;
    playerPattern = [];
    pattern =[];
    let points = document.getElementById("points")
    points.innerHTML=1;
    let startHtml = document.getElementById('start');
    let set1Html = document.getElementById('set1');
    set1Html.style.display = 'flex';
    let set2Html = document.getElementById('set2');
    set2Html.style.display = 'flex';
    startHtml.style.display = 'none';
    randomPattern()
}

function playerPatternFunc() {
    if (isShowingPattern) {
        return;  
    }
    let squrechoose = this.id;
    playerPattern.push(squrechoose)
    if (playerPattern.length === pattern.length) {
        console.log('user array' + playerPattern)
        setTimeout(() => {
        checkPatterns(playerPattern)
    }, 50); 
    }
}

function checkPatterns(playerPattern) {
    let matching = true;
    for (i=0; i<playerPattern.length; i++) {
        if (playerPattern[i] !== pattern[i]) {
            matching = false;
        }
    }
    if (matching == true) {
        playerPattern = [];
        console.log("its a match");
        level += 1;
        points.innerHTML=level;
        nextLevel()


    } else {

        handlePoints(level) 
        gameOver()
    }
} 


function randomPattern() {
let randomIndex = Math.floor(Math.random() * squres.length);
let randomSqure = squres[randomIndex];
pattern.push(randomSqure);
console.log('random array' + pattern);
showPattern(pattern);
}

function showPattern(pattern) {
    isShowingPattern = true;  // Set the flag to true during pattern display

    let delay = 800;
    timeoutIds = [];
    for (let i = 0; i < pattern.length; i++) {
        let timeoutId = setTimeout(() => {
            flashButton(pattern[i]);
            makesound(pattern[i]); 
        }, delay);
        timeoutIds.push(timeoutId);
        delay += 800;
    }
        // After the pattern display is complete, reset the flag to false
        setTimeout(() => {
            isShowingPattern = false;
        }, delay);
    
}

function nextLevel() {
    playerPattern = []

    randomPattern()
}

function gameOver() {
    var gameoversound = new Audio('static/sounds/gameover.mp3')
    gameoversound.play();
    let container = document.getElementById('simoncontainer');
    let gameover = document.getElementById('gameover');
    container.style.display = 'none';
    gameover.style.display = 'flex';
    timeoutIds.forEach(id => clearTimeout(id));
    timeoutIds = [];
}

function flashButton(color) {
    let button= document.getElementById(color)
    button.style.backgroundColor = 'white';
    setTimeout(() => {
        button.style.backgroundColor = color;
    }, 500); 
}


function playAgain() {
    let container = document.getElementById('simoncontainer');
    let gameover = document.getElementById('gameover');
    container.style.display = 'flex';
    gameover.style.display = 'none';
    let playerLevel = level - 1;
    let current_highest_level = document.getElementById('highestlevel').innerHTML;
    if ( playerLevel > current_highest_level) {
        current_highest_level = playerLevel;
        alert("You achieved a new record! Well done")
    }
    level = 1;


    timeoutIds.forEach(id => clearTimeout(id));
    timeoutIds = [];
    startGame()
}


for (var i=0; i<document.querySelectorAll(".squre").length; i++) {
    document.querySelectorAll("button")[i+1].addEventListener("click", function () {
        var squrechoose = this.classList[0];
       console.log(squrechoose)
       if (!isShowingPattern) {
            makesound(squrechoose);
        }
    });
}

function handlePoints(points) {
    let simonHighest = null;
    let pointsExistance = false;
    axios.get("http://127.0.0.1:5000/api/points").then(response=> {
        const scores = response.data;
        console.log(scores)
        scores.map(game=> {
            if (game.game == "simon") {
                wsimonHighest = game.highest_score;
                console.log(simonHighest)
                pointsExistance = true;
            }
        })
        if (pointsExistance == false) {
            axios.post('/api/points/add', {points:points, game:'simon', action:'insert'}).then(response => {
                console.log("add new")
        })} 
        else if (points > simonHighest) {
        axios.post('/api/points/add', {points:points, game:'simon',action:'update'}).then(response => {
            console.log("update db")
        })}
    })

}

function makesound(squrechoose) {
    switch (squrechoose) {
        case "blue":
            var blue = new Audio('static/sounds/blue.mp3')
            blue.play();
            break;

        case "green":
            var green = new Audio('static/sounds/green.mp3')
            green.play();
            break;
            
        case "red":
            var red = new Audio('static/sounds/red.mp3')
            red.play();
            break;

        case "yellow":
            var yellow = new Audio('static/sounds/yellow.mp3')
            yellow.play();
            break;

        default:
            console.log("default");
            break;
    }
}