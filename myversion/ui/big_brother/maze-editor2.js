const canvas = document.getElementById('maze');
const ctx = canvas.getContext('2d');
const gridSize = 10; // Updated to a smaller grid size for better visibility
const cellSize = canvas.width / gridSize;

let lines = [];
let cameras = [];
let currentCamera = [];
let drawingLine = false;
let drawingCamera = false;
let tempLine = [];

function drawGrid() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 0.5;
    for (let x = 0; x <= canvas.width; x += cellSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    for (let y = 0; y <= canvas.height; y += cellSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
}

function drawLines() {
    ctx.strokeStyle = '#FF0000';
    ctx.lineWidth = 2;
    lines.forEach(line => {
        ctx.beginPath();
        ctx.moveTo(line[0].x * cellSize, line[0].y * cellSize);
        ctx.lineTo(line[1].x * cellSize, line[1].y * cellSize);
        ctx.stroke();
    });

    if (tempLine.length === 2) {
        ctx.beginPath();
        ctx.moveTo(tempLine[0].x * cellSize, tempLine[0].y * cellSize);
        ctx.lineTo(tempLine[1].x * cellSize, tempLine[1].y * cellSize);
        ctx.stroke();
    }
}

function drawCameras() {
    ctx.fillStyle = '#00FF00';
    cameras.forEach(camera => {
        camera.forEach(point => {
            ctx.beginPath();
            ctx.arc(point.x * cellSize, point.y * cellSize, 3, 0, 2 * Math.PI);
            ctx.fill();
        });
        if (camera.length === 3) {
            ctx.fillStyle = 'rgba(0, 255, 0, 0.3)';
            ctx.beginPath();
            ctx.moveTo(camera[0].x * cellSize, camera[0].y * cellSize);
            ctx.lineTo(camera[1].x * cellSize, camera[1].y * cellSize);
            ctx.lineTo(camera[2].x * cellSize, camera[2].y * cellSize);
            ctx.closePath();
            ctx.fill();
            ctx.fillStyle = '#00FF00';
        }
    });
}

function redraw() {
    drawGrid();
    drawLines();
    drawCameras();
    updateElementsList();
}

canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((e.clientX - rect.left) / cellSize);
    const y = Math.floor((e.clientY - rect.top) / cellSize);

    if (drawingLine) {
        if (tempLine.length === 0) {
            tempLine.push({x, y});
        } else {
            tempLine.push({x, y});
            lines.push(tempLine);
            tempLine = [];
            drawingLine = false;
        }
    } else if (drawingCamera) {
        currentCamera.push({x, y});
        if (currentCamera.length === 3) {
            cameras.push(currentCamera);
            currentCamera = [];
            drawingCamera = false;
        }
    }
    redraw();
});

document.getElementById('drawLineButton').addEventListener('click', () => {
    drawingLine = true;
    drawingCamera = false;
    tempLine = [];
});

document.getElementById('addCameraButton').addEventListener('click', () => {
    drawingCamera = true;
    drawingLine = false;
    currentCamera = [];
});

document.getElementById('saveButton').addEventListener('click', () => {
    const data = {
        lines,
        cameras
    };

    fetch('https://example.com/save', {  // замените на ваш URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log('Success:', result);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function loadExistingData() {
    fetch('https://example.com/load', {  // замените на ваш URL
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        lines = data.lines || [];
        cameras = data.cameras || [];
        redraw();
    })
    .catch(error => {
        console.error('Error loading data:', error);
    });
}

function deleteLine(index) {
    lines.splice(index, 1);
    redraw();
}

function deleteCamera(index) {
    cameras.splice(index, 1);
    redraw();
}

function updateElementsList() {
    const elementsList = document.getElementById('elementsList');
    elementsList.innerHTML = '';

    lines.forEach((line, index) => {
        const listItem = document.createElement('div');
        listItem.className = 'list-item';
        listItem.textContent = `Линия ${index + 1}`;
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Удалить';
        deleteButton.onclick = () => deleteLine(index);
        listItem.appendChild(deleteButton);
        elementsList.appendChild(listItem);
    });

    cameras.forEach((camera, index) => {
        const listItem = document.createElement('div');
        listItem.className = 'list-item';
        listItem.textContent = `Камера ${index + 1}`;
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Удалить';
        deleteButton.onclick = () => deleteCamera(index);
        listItem.appendChild(deleteButton);
        elementsList.appendChild(listItem);
    });
}

window.onload = () => {
    loadExistingData();
    redraw();
};

redraw();
