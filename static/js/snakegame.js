var blockSize = 25;
var rows = 15;
var cols = 20;
var board;
var context;

//snake body
var snakeX = blockSize * 5;
var snakeY = blockSize * 5;
var snakeBody = [];
// food 
var foodX;
var foodY;
//snake speed
var velocityX = 0;
var velocityY = 0;

var gameOver = false;

var gameInterval; // Variable to store the interval ID

window.onload = function () {
    board = document.getElementById("snake_board")
    board.height = rows * blockSize;
    board.width = cols * blockSize
    context = board.getContext("2d");

    startGame();
}

function startGame() {
    let points = document.getElementById("points");
    points.innerHTML = 0;
    clearInterval(gameInterval);
    placeFood();
    snakeX = blockSize * 5;
    snakeY = blockSize * 5;
    snakeBody = [];
    velocityX = 0;
    velocityY = 0;
    gameOver = false;
    document.addEventListener("keyup", changeDirection);

    gameInterval = setInterval(update, 1000 / 10);
}

function increasePoints() {
    let points = document.getElementById("points");
    let level = parseInt(points.innerHTML);
    points.innerHTML = level +1;
}

function update() {

    if (gameOver) {
        return;
    }
    context.fillStyle = "black";
    context.fillRect(0, 0, board.width, board.height);
    context.fillStyle = "lime";
    context.fillRect(foodX, foodY, blockSize, blockSize);

    if (snakeX == foodX && snakeY == foodY) {
        snakeBody.push([foodX, foodY])
        increasePoints()
        placeFood();
    }

    for (let i = snakeBody.length - 1; i > 0; i--) {
        snakeBody[i] = snakeBody[i - 1];
    }

    if (snakeBody.length) {
        snakeBody[0] = [snakeX, snakeY]
    }
    context.fillStyle = "red";
    snakeX += velocityX * blockSize;
    snakeY += velocityY * blockSize;
    context.fillRect(snakeX, snakeY, blockSize, blockSize);
    for (let i = 0; i < snakeBody.length; i++) {
        context.fillRect(snakeBody[i][0], snakeBody[i][1], blockSize, blockSize)
    }

    if (snakeX < 0 || snakeX > cols * blockSize || snakeY < 0 || snakeY > rows * blockSize) {
        endGame();
    }
    for (let i = 0; i < snakeBody.length; i++) {
        if (snakeX == snakeBody[i][0] && snakeY == snakeBody[i][1]) {
            endGame();
        }
    }
}

function placeFood() {
    foodX = Math.floor(Math.random() * cols) * blockSize;
    foodY = Math.floor(Math.random() * rows) * blockSize;
}

function changeDirection(e) {
    if (e.code == "ArrowUp" && velocityY != 1) {
        velocityX = 0;
        velocityY = -1;
    }
    else if (e.code == "ArrowDown" && velocityY != -1) {
        velocityX = 0;
        velocityY = 1;
    }
    else if (e.code == "ArrowLeft" && velocityX != 1) {
        velocityX = -1;
        velocityY = 0;
    }
    else if (e.code == "ArrowRight" && velocityX != -1) {
        velocityX = 1;
        velocityY = 0;
    }
}

function endGame() {
    gameOver = true;
    alert("Game Over!");
    // Stop listening to key events
    document.removeEventListener("keyup", changeDirection);
    // Clear the canvas
    context.clearRect(0, 0, board.width, board.height);
    // Reset the game
    let points = document.getElementById("points");
    points_num = parseInt(points.innerHTML)
    handlePoints(points_num) 
    startGame();
}

function handlePoints(points) {
    let snakeHighest = null;
    let pointsExistance = false;
    axios.get("http://127.0.0.1:5000/api/points").then(response=> {
        const scores = response.data;
        console.log(scores)
        scores.map(game=> {
            if (game.game == "snake") {
                snakeHighest = game.highest_score;
                console.log(snakeHighest)
                pointsExistance = true;
            }
        })
        if (pointsExistance == false) {
            axios.post('/api/points/add', {points:points, game:'snake', action:'insert'}).then(response => {
                console.log("add new")
        })} 
        else if (points > snakeHighest) {
        axios.post('/api/points/add', {points:points, game:'snake',action:'update'}).then(response => {
            console.log("update db")
        })}
    })

}