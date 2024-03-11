
let rounds = 0;

function playShuffleSound() {
    let audio = new Audio('static/sounds/shufflecard.mp3');
    audio.play();
}

function playRoundSound() {
    let audio = new Audio('static/sounds/flipcard.mp3');
    audio.play();
}

function startGame() {
    playShuffleSound()
    rounds = 0;
    let round_html = document.getElementById('rounds_num');
    round_html.innerHTML = `Round: ${rounds}`;
    let player_points = 0;
    let computer_points = 0;
    let gameinfohtml = document.getElementById('game_info');
    let thegamehtml = document.getElementById('thegame');
    let player_points_html = document.getElementById('player_points');
    let computer_points_html = document.getElementById('computer_points');
    player_points_html.innerHTML = player_points
    computer_points_html.innerHTML = computer_points
    thegamehtml.style.display = 'flex';
    gameinfohtml.style.display = 'none';
    let player_card = document.getElementById('player_card');
    let computer_card = document.getElementById('computer_card'); 
    player_card.innerHTML = ''
    computer_card.innerHTML = ''
}

function playAgain() {
    let game_over = document.getElementById('gameover');
    game_over.style.display = 'none';
    let player_section = document.getElementById('player_section');
    let computer_section = document.getElementById('computer_section'); 
    let result_section = document.getElementById('result_section'); 

    player_section.style.display = 'flex';
    computer_section.style.display = 'flex';
    result_section.style.display = 'flex';

    let round_button = document.getElementById('round-button');
    round_button.style.display = "block"
    startGame()
}

function endgame(winner_str) {
    let game_over = document.getElementById('gameover');
    let round_button = document.getElementById('round-button');
    game_over.style.display = 'flex';
    round_button.style.display = 'none';
    let player_section = document.getElementById('player_section');
    let computer_section = document.getElementById('computer_section'); 
    let result_section = document.getElementById('result_section'); 

    player_section.style.display = 'none';
    computer_section.style.display = 'none';
    result_section.style.display = 'none';

    let winner_html = document.getElementById('winner'); 
    winner_html.innerHTML = winner_str

}

function winner(player_points,computer_points) {
    if (player_points > computer_points) {
        winner_str = 'YOU are the WINNER'
    } if (player_points < computer_points) {
        winner_str = 'The computer is the WINNER'
    } if (player_points === computer_points) {
        winner_str = 'ITS A TIE' 
    }
    endgame(winner_str)
}

function round() {
    playRoundSound()
    rounds = rounds + 1 
    const PlayerRandomNumber = Math.floor(Math.random() * (15 - 2 + 1)) + 2;
    const ComputerRandomNumber = Math.floor(Math.random() * (15 - 2 + 1)) + 2;
    let result_section = document.getElementById('result_section');
    result_section.style.display = 'flex';
    let player_card = document.getElementById('player_card');
    let computer_card = document.getElementById('computer_card'); 
    let player_points = parseInt(document.getElementById('player_points').innerHTML, 10)
    let computer_points = parseInt(document.getElementById('computer_points').innerHTML, 10);
    let round_html = document.getElementById('rounds_num');
    round_html.innerHTML = `Round: ${rounds}`;
    player_card.innerHTML = `<img src="/static/images/war_cards/${PlayerRandomNumber}.png" alt="" class="card">`;
    computer_card.innerHTML = `<img src="/static/images/war_cards/${ComputerRandomNumber}.png" alt="" class="card">`;

    if (PlayerRandomNumber > ComputerRandomNumber) {
        player_points = player_points + 2; 
        let player_points_html = document.getElementById('player_points'); 
        let points = document.getElementById("points");
        player_points_html.innerHTML = player_points;
        points.innerHTML = player_points;
    } 
    if (PlayerRandomNumber < ComputerRandomNumber) {
        computer_points = computer_points + 2;
        let computer_points_html = document.getElementById('computer_points'); 
        computer_points_html.innerHTML = computer_points
    }
    if (rounds === 11) {
        winner(player_points,computer_points)
    }

}