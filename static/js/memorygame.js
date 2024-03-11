let buttons = document.querySelectorAll('button');
let counter = 0; 
let coupleList = []
let coupleidList = []
let idmatched = []
let points = 50;
let optionText; 


const cardArrays = {
    animals: [
        {img: 'clown-fish'},
        {img: 'owl'},
        {img: 'frog'},
        {img: 'lion'},
        {img: 'crab'},
        {img: 'pig'},
        {img: 'shark'},
        {img: 'snake'},
        {img: 'clown-fish'},
        {img: 'owl'},
        {img: 'frog'},
        {img: 'lion'},
        {img: 'crab'},
        {img: 'pig'},
        {img: 'shark'},
        {img: 'snake'},
    ],
    space: [
        {img: 'alien'},
        {img: 'asteroid'},
        {img: 'astronaut'},
        {img: 'black-hole'},
        {img: 'meteorite'},
        {img: 'radar'},
        {img: 'solar-system'},
        {img: 'sun'},
        {img: 'alien'},
        {img: 'asteroid'},
        {img: 'astronaut'},
        {img: 'black-hole'},
        {img: 'meteorite'},
        {img: 'radar'},
        {img: 'solar-system'},
        {img: 'sun'},
    ],
    socialmedia: [
        {img: 'facebook'},
        {img: 'instagram'},
        {img: 'whatsapp'},
        {img: 'linkedin'},
        {img: 'snapchat'},
        {img: 'tik-tok'},
        {img: 'tumblr'},
        {img: 'twitter'},
        {img: 'facebook'},
        {img: 'instagram'},
        {img: 'whatsapp'},
        {img: 'linkedin'},
        {img: 'snapchat'},
        {img: 'tik-tok'},
        {img: 'tumblr'},
        {img: 'twitter'},
    ],
};


buttons.forEach(button => {
    if (button.id !== 'start-button' && button.id !== 'option') {
        button.addEventListener('click', displayimg);
    }
});

function option(button) {
    optionText = button.innerHTML;  
    console.log(optionText) 
    let optionsbuttons = document.getElementById('options');
    optionsbuttons.style.display = 'none';
    let gamerows = document.getElementById('gamerows');
    gamerows.style.display = 'flex';
    randomimg(cardArrays[optionText]);

}

function startGame() {
    counter = 0; 
    coupleList = []
    coupleidList = []
    idmatched = []
    points = 50;
    let pointshtml = document.getElementById("points")
    pointshtml.innerHTML=points;
    let optionsbuttons = document.getElementById('options');
    optionsbuttons.style.display = 'flex';
    let h3html = document.getElementById('start');
    let buttonstartHtml = document.getElementById('start-button');
    h3html.style.display = 'none';
    buttonstartHtml.style.display = 'none';
}


function randomimg(chosenCards) {
    const shuffledCards = [...chosenCards]; 
    timesToLoop = shuffledCards.length;
    for (let i = 0; i < timesToLoop; i++) {
        let randomIndex = Math.floor(Math.random() * shuffledCards.length);
        let randomCard = shuffledCards[randomIndex].img;
        let idimg = document.getElementById('sq' + i);
        idimg.style.backgroundImage = 'none';
        idimg.setAttribute('data-image', randomCard);
        shuffledCards.splice(randomIndex, 1);
    }
}

function displayimg() {
    if (counter < 2) { 
        let sqid = document.getElementById(this.id);
        if (this.id== coupleidList[0]) {
            alert("You can't select the same image twice")
        } else {
        counter += 1; 
        console.log(counter);
        sqRandom = sqid.getAttribute('data-image');
        sqid.style.backgroundImage = "url('/static/images/"+optionText+"/"+sqRandom + ".png')";
        coupleList.push(sqRandom);
        coupleidList.push(this.id);

        if (counter === 2) {
            setTimeout(function() {
                counter = 0;
                checkCouple(coupleList, coupleidList);
            }, 1000); 
        }
    }
}}

function checkCouple(coupleList, coupleidList) {
    if (coupleList[0] === coupleList[1]) {
        idmatched.push(coupleidList[0]);
        idmatched.push(coupleidList[1]);
        console.log(idmatched);
        console.log(idmatched.length)
        if (idmatched.length === 16) {
            alert('You have matched all the cards! Your points: ' + points + '. Well done');
            playAgain()
        } else {
            whatNext(coupleList, coupleidList, idmatched);
        }
    } else {
        points -= 2;
        let pointshtml = document.getElementById("points")
        pointshtml.innerHTML=points;
        whatNext(coupleList, coupleidList, idmatched);
    }
}


function whatNext(coupleList, coupleidList, idmatched) {
    console.log(idmatched);
    buttons.forEach(button => {
        if (button.id !== 'start-button' && !idmatched.includes(button.id)) {
            button.style.backgroundImage = 'none';
            button.style.backgroundColor = ' rgb(209, 212, 175); '
        }
    });
    
    coupleList.length = 0;
    coupleidList.length = 0;
}

function playAgain() {
    let h3html = document.getElementById('start');
    let buttonstartHtml = document.getElementById('start-button');
    h3html.style.display = 'flex';
    buttonstartHtml.style.display = 'flex';
    let gamerows = document.getElementById('gamerows');
    gamerows.style.display = 'none';
}