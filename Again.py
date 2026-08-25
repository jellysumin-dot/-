
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌 깨기",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 벽돌 깨기")
st.caption("방향키 또는 마우스로 패들을 움직여 모든 벽돌을 깨보세요!")

game = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        background: #111827;
        color: white;
        font-family: Arial, sans-serif;
        text-align: center;
    }

    #game {
        background: #0f172a;
        border: 3px solid #38bdf8;
        border-radius: 10px;
        display: block;
        margin: 10px auto;
        max-width: 100%;
    }

    .info {
        font-size: 18px;
        margin: 8px;
    }

    button {
        background: #38bdf8;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        font-weight: bold;
    }

    button:hover {
        background: #0ea5e9;
    }
</style>
</head>

<body>

<div class="info">
    점수: <span id="score">0</span>
    &nbsp;&nbsp;
    목숨: <span id="lives">3</span>
</div>

<canvas id="game" width="700" height="500"></canvas>

<button onclick="restartGame()">🔄 다시 시작</button>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let score = 0;
let lives = 3;

let ball = {
    x: canvas.width / 2,
    y: canvas.height - 70,
    dx: 4,
    dy: -4,
    radius: 8
};

let paddle = {
    width: 110,
    height: 14,
    x: canvas.width / 2 - 55,
    speed: 8
};

let rightPressed = false;
let leftPressed = false;

const brickRows = 6;
const brickCols = 9;
const brickWidth = 65;
const brickHeight = 22;
const brickPadding = 10;
const brickTop = 45;
const brickLeft = 18;

let bricks = [];

function createBricks() {
    bricks = [];

    for (let r = 0; r < brickRows; r++) {
        bricks[r] = [];

        for (let c = 0; c < brickCols; c++) {
            bricks[r][c] = {
                x: brickLeft + c * (brickWidth + brickPadding),
                y: brickTop + r * (brickHeight + brickPadding),
                alive: true
            };
        }
    }
}

function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = "#facc15";
    ctx.fill();
    ctx.closePath();
}

function drawPaddle() {
    ctx.beginPath();
    ctx.roundRect(
        paddle.x,
        canvas.height - 30,
        paddle.width,
        paddle.height,
        7
    );
    ctx.fillStyle = "#38bdf8";
    ctx.fill();
    ctx.closePath();
}

function drawBricks() {

    for (let r = 0; r < brickRows; r++) {
        for (let c = 0; c < brickCols; c++) {

            const brick = bricks[r][c];

            if (!brick.alive) continue;

            ctx.beginPath();

            ctx.roundRect(
                brick.x,
                brick.y,
                brickWidth,
                brickHeight,
                5
            );

            const colors = [
                "#ef4444",
                "#f97316",
                "#eab308",
                "#22c55e",
                "#06b6d4",
                "#8b5cf6"
            ];

            ctx.fillStyle = colors[r];
            ctx.fill();

            ctx.closePath();
        }
    }
}

function collisionDetection() {

    for (let r = 0; r < brickRows; r++) {

        for (let c = 0; c < brickCols; c++) {

            const brick = bricks[r][c];

            if (!brick.alive) continue;

            if (
                ball.x > brick.x &&
                ball.x < brick.x + brickWidth &&
                ball.y > brick.y &&
                ball.y < brick.y + brickHeight
            ) {

                ball.dy = -ball.dy;
                brick.alive = false;

                score += 10;

                document.getElementById("score").textContent = score;

                checkWin();
            }
        }
    }
}

function checkWin() {

    let remaining = 0;

    for (let r = 0; r < brickRows; r++) {
        for (let c = 0; c < brickCols; c++) {
            if (bricks[r][c].alive) remaining++;
        }
    }

    if (remaining === 0) {

        alert("🎉 축하합니다! 모든 벽돌을 깼어요!");

        restartGame();
    }
}

function resetBall() {

    ball.x = canvas.width / 2;
    ball.y = canvas.height - 70;

    ball.dx = Math.random() > 0.5 ? 4 : -4;
    ball.dy = -4;

    paddle.x = canvas.width / 2 - paddle.width / 2;
}

function update() {

    // 벽 충돌
    if (
        ball.x + ball.dx > canvas.width - ball.radius ||
        ball.x + ball.dx < ball.radius
    ) {
        ball.dx = -ball.dx;
    }

    if (ball.y + ball.dy < ball.radius) {
        ball.dy = -ball.dy;
    }

    // 패들 충돌
    if (
        ball.y + ball.radius >= canvas.height - 30 &&
        ball.y + ball.radius <= canvas.height - 15 &&
        ball.x >= paddle.x &&
        ball.x <= paddle.x + paddle.width
    ) {

        ball.dy = -Math.abs(ball.dy);

        // 패들 위치에 따라 공의 방향 변경
        let hitPosition =
            (ball.x - paddle.x) / paddle.width;

        ball.dx = (hitPosition - 0.5) * 9;
    }

    // 공이 아래로 떨어짐
    if (ball.y + ball.dy > canvas.height - ball.radius) {

        lives--;

        document.getElementById("lives").textContent = lives;

        if (lives <= 0) {

            alert("게임 오버! 점수: " + score);

            restartGame();

        } else {

            resetBall();
        }
    }

    // 패들 이동
    if (rightPressed &&
        paddle.x < canvas.width - paddle.width) {

        paddle.x += paddle.speed;
    }

    if (leftPressed && paddle.x > 0) {

        paddle.x -= paddle.speed;
    }

    ball.x += ball.dx;
    ball.y += ball.dy;

    collisionDetection();
}

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    drawBricks();
    drawBall();
    drawPaddle();

    update();

    requestAnimationFrame(draw);
}

document.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "ArrowRight") {
            rightPressed = true;
        }

        if (event.key === "ArrowLeft") {
            leftPressed = true;
        }
    }
);

document.addEventListener(
    "keyup",
    function(event) {

        if (event.key === "ArrowRight") {
            rightPressed = false;
        }

        if (event.key === "ArrowLeft") {
            leftPressed = false;
        }
    }
);

// 마우스 조작
canvas.addEventListener(
    "mousemove",
    function(event) {

        const rect = canvas.getBoundingClientRect();

        const mouseX =
            event.clientX - rect.left;

        paddle.x =
            mouseX - paddle.width / 2;

        if (paddle.x < 0)
            paddle.x = 0;

        if (
            paddle.x >
            canvas.width - paddle.width
        )
            paddle.x =
                canvas.width - paddle.width;
    }
);

function restartGame() {

    score = 0;
    lives = 3;

    document.getElementById("score").textContent = score;
    document.getElementById("lives").textContent = lives;

    createBricks();
    resetBall();
}

createBricks();
draw();

</script>

</body>
</html>
"""

components.html(game, height=600, scrolling=False)
