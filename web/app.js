const express = require('express')
const app = express()
const multer = require('multer');
const path = require('path')
const http = require('http');

const fs = require('fs');
const APP_PORT = 5555

const upload = multer({dest: 'uploads/'});
const server = app.listen(APP_PORT, () => {
    console.log(`App running on port ${APP_PORT}`)
})

const io = require('socket.io')(server, {
    allowEIO3: true // false by default
}
)

app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'pug')

app.use(express.static('public'))


// File upload endpoint
app.post('/upload', upload.single('file'), (req, res) => {
    console.log('File uploaded:', req.file);
    var FormData = require('form-data');
    let form = new FormData();
    form.append('file', fs.createReadStream(req.file.path));
    var request = http.request({
        host: "localhost",
        port: 8080,
        path: "/upload",
        method: 'post',
        headers: form.getHeaders()
    });
    form.pipe(request);
    request.on('response', function (res) {
        console.log(res.statusCode);
    });

    console.log(request);
    res.render('index')

});

app.get('/', (req, res) => {
    res.render('index')
})


io.on('connection', function (socket) {
    socket.on('chatter', function (message) {
        http.get('http://localhost:8080/analyse/' + message, (resp) => {
            let data = '';
            // A chunk of data has been received.
            resp.on('data', (chunk) => {
                data += chunk;
            });

            // The whole response has been received. Print out the result.
            var jsonObject
            resp.on('end', () => {
                var jsonObject = JSON.parse(data);
                console.log(jsonObject.summary);
                io.emit('chatter', jsonObject.summary)
            });


        }).on("error", (err) => {
            console.log("Error: " + err.message);
        });
    });
});

