const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

const gridColor = '#ccc';
const lineColor = '#ff0000';
const cameraColor = '#00ff00';
const cameras = [];
const lines = [];
let isDrawingLine = false;
let isMovingLine = false;
let selectedLine = null;
let selectedCamera = null;
let startX, startY;

let isCameraMode = false;

// Функция для переключения режима добавления камеры
function toggleCameraMode() {
    isCameraMode = !isCameraMode;
    const modeButton = document.querySelector('button[onclick="toggleCameraMode()"]');
    modeButton.textContent = isCameraMode ? 'Режим добавления линий' : 'Режим добавления камеры';
}

// Draw grid
function drawGrid() {
    const gridSize = 20;
    ctx.strokeStyle = gridColor;
    for (let x = 0; x <= canvas.width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    for (let y = 0; y <= canvas.height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
}

// Draw lines
function drawLines() {
    ctx.strokeStyle = lineColor;
    lines.forEach(line => {
        ctx.beginPath();
        ctx.moveTo(line.startX, line.startY);
        ctx.lineTo(line.endX, line.endY);
        ctx.stroke();
    });
}

// Draw cameras
function drawCameras() {
    cameras.forEach(camera => {
        ctx.fillStyle = cameraColor;
        ctx.fillRect(camera.x - 5, camera.y - 5, 10, 10);
        ctx.beginPath();
        ctx.moveTo(camera.x, camera.y);
        ctx.lineTo(camera.fov1X, camera.fov1Y);
        ctx.lineTo(camera.fov2X, camera.fov2Y);
        ctx.closePath();
        ctx.fill();
    });
}

// Add line
function addLine(startX, startY, endX, endY) {
    lines.push({ startX, startY, endX, endY });
    draw();
}

// Обновление функции добавления камеры с учётом новых параметров
function addCamera(x, y) {
    const angle = 60; // default angle
    const length = 100; // default length
    const fov = calculateCameraFOV({ x, y }, angle, length);
    cameras.push({ x, y, ...fov });
    draw();
    updateCameraList();
}

// Update camera list
function updateCameraList() {
    const cameraList = document.getElementById('cameraList');
    cameraList.innerHTML = '';
    cameras.forEach((camera, index) => {
        const cameraItem = document.createElement('div');
        cameraItem.textContent = `Камера ${index + 1}`;
        cameraItem.onclick = () => {
            selectedCamera = camera;
            highlightCamera(camera);
        };
        cameraList.appendChild(cameraItem);
    });
}

// Highlight camera
function highlightCamera(camera) {
    draw();
    ctx.strokeStyle = '#0000ff';
    ctx.strokeRect(camera.x - 5, camera.y - 5, 10, 10);
}

// Save data to JSON
function saveData() {
    const data = {
        lines,
        cameras
    };
    console.log(JSON.stringify(data));
}

// Draw all elements
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawGrid();
    drawLines();
    drawCameras();
}

// Функция для вычисления новых координат поля зрения камеры
function calculateCameraFOV(camera, angle, length) {
    const radians1 = (Math.PI / 180) * (angle / 2);
    const radians2 = (Math.PI / 180) * (-angle / 2);
    const fov1X = camera.x + length * Math.cos(radians1);
    const fov1Y = camera.y + length * Math.sin(radians1);
    const fov2X = camera.x + length * Math.cos(radians2);
    const fov2Y = camera.y + length * Math.sin(radians2);
    return { fov1X, fov1Y, fov2X, fov2Y };
}

// Функция для обновления параметров выбранной камеры
function updateCamera() {
    if (!selectedCamera) return;
    const angle = parseInt(document.getElementById('cameraAngle').value);
    const length = parseInt(document.getElementById('cameraLength').value);
    const fov = calculateCameraFOV(selectedCamera, angle, length);
    selectedCamera.fov1X = fov.fov1X;
    selectedCamera.fov1Y = fov.fov1Y;
    selectedCamera.fov2X = fov.fov2X;
    selectedCamera.fov2Y = fov.fov2Y;
    draw();
}

// Изменение функции для выделения камеры
function highlightCamera(camera) {
    selectedCamera = camera;
    draw();
    ctx.strokeStyle = '#0000ff';
    ctx.strokeRect(camera.x - 5, camera.y - 5, 10, 10);
    document.getElementById('cameraControls').style.display = 'block';
    document.getElementById('cameraAngle').value = calculateAngle(camera);
    document.getElementById('cameraLength').value = calculateLength(camera);
}


// Функции для вычисления угла и длины
function calculateAngle(camera) {
    const dx = camera.fov1X - camera.x;
    const dy = camera.fov1Y - camera.y;
    return Math.round(Math.atan2(dy, dx) * (180 / Math.PI)) * 2;
}

function calculateLength(camera) {
    const dx = camera.fov1X - camera.x;
    const dy = camera.fov1Y - camera.y;
    return Math.round(Math.sqrt(dx * dx + dy * dy));
}



// Обновленный обработчик события mousedown для добавления или перемещения камеры
canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    startX = Math.round((e.clientX - rect.left) / 20) * 20;
    startY = Math.round((e.clientY - rect.top) / 20) * 20;

    if (isCameraMode) {
        addCamera(startX, startY);
    } else {
        isDrawingLine = true;
    }
});

canvas.addEventListener('mousemove', (e) => {
    if (!isDrawingLine) return;
    const rect = canvas.getBoundingClientRect();
    const endX = Math.round((e.clientX - rect.left) / 20) * 20;
    const endY = Math.round((e.clientY - rect.top) / 20) * 20;

    if (endX !== startX || endY !== startY) {
        draw();
        ctx.strokeStyle = lineColor;
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(endX, endY);
        ctx.stroke();
    }
});

canvas.addEventListener('mouseup', (e) => {
    if (isDrawingLine) {
        const rect = canvas.getBoundingClientRect();
        const endX = Math.round((e.clientX - rect.left) / 20) * 20;
        const endY = Math.round((e.clientY - rect.top) / 20) * 20;
        addLine(startX, startY, endX, endY);
        isDrawingLine = false;
    }
});

draw();
