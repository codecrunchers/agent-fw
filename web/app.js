const express = require('express');
const multer = require('multer');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

const upload = multer({ dest: 'uploads/' });

app.use(express.static('public'));

app.post('/upload', upload.single('file'), (req, res) => {
  io.emit('file-uploaded');
  res.status(200).send();
});

io.on('connection', (socket) => {
  socket.on('file-uploaded', () => {
    // Start chat session
  });
});

server.listen(3000, () => {
  console.log('Server is running on port 3000');
});
