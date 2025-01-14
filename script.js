const cells = document.querySelectorAll('.cell');
const restartButton = document.getElementById('restart');
const winnerOverlay = document.getElementById('winnerOverlay');
const winnerMessage = document.getElementById('winnerMessage');
const confettiCanvas = document.getElementById('confettiCanvas');
let currentPlayer = 'X';
let board = ['', '', '', '', '', '', '', '', ''];
let gameActive = true;

const winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
];

function handleCellClick(event) {
    const clickedCell = event.target;
    const clickedCellIndex = parseInt(clickedCell.getAttribute('data-index'));

    if (board[clickedCellIndex] !== '' || !gameActive) {
        return;
    }

    board[clickedCellIndex] = currentPlayer;
    clickedCell.textContent = currentPlayer;
    clickedCell.classList.add(currentPlayer);

    checkResult();
}

function checkResult() {
    let roundWon = false;

    for (let i = 0; i < winningConditions.length; i++) {
        const [a, b, c] = winningConditions[i];
        if (board[a] === '' || board[b] === '' || board[c] === '') {
            continue;
        }
        if (board[a] === board[b] && board[a] === board[c]) {
            roundWon = true;
            break;
        }
    }

    if (roundWon) {
        showWinner(currentPlayer);
        return;
    }

    if (!board.includes('')) {
        showWinner("It's a draw!");
        return;
    }

    currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
}

function showWinner(player) {
    winnerMessage.textContent = player === "It's a draw!" ? player : `Player ${player} Wins!`;
    gameActive = false;
    winnerOverlay.classList.remove('hidden');
    startConfetti();
}

function restartGame() {
    currentPlayer = 'X';
    board = ['', '', '', '', '', '', '', '', ''];
    gameActive = true;
    cells.forEach(cell => {
        cell.textContent = '';
        cell.classList.remove('X', 'O');
    });
    winnerOverlay.classList.add('hidden');
    stopConfetti();
}

function startConfetti() {
    const confetti = confettiCanvas.getContext('2d');
    confettiCanvas.width = window.innerWidth;
    confettiCanvas.height = window.innerHeight;

    const particles = [];
    for (let i = 0; i < 300; i++) {
        particles.push({
            x: Math.random() * confettiCanvas.width,
            y: Math.random() * confettiCanvas.height,
            r: Math.random() * 5 + 2,
            dx: Math.random() * 4 - 2,
            dy: Math.random() * 4 + 2,
            color: `hsl(${Math.random() * 360}, 100%, 50%)`,
        });
    }

    function draw() {
        confetti.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
        particles.forEach(p => {
            confetti.beginPath();
            confetti.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            confetti.fillStyle = p.color;
            confetti.fill();
        });
    }

    function update() {
        particles.forEach(p => {
            p.x += p.dx;
            p.y += p.dy;

            if (p.x < 0 || p.x > confettiCanvas.width || p.y > confettiCanvas.height) {
                p.x = Math.random() * confettiCanvas.width;
                p.y = -10;
            }
        });
    }

    function loop() {
        draw();
        update();
        requestAnimationFrame(loop);
    }

    loop();
}

function stopConfetti() {
    confettiCanvas.getContext('2d').clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
}

cells.forEach(cell => {
    cell.addEventListener('click', handleCellClick);
});

restartButton.addEventListener('click', restartGame);
