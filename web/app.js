const express = require('express')
const app = express()
const path = require('path')

const APP_PORT = 5555

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

app.get('/', (req, res) => {
    res.render('index')
})


io.on('connection', function (socket) {
    socket.on('chatter', function (message) {
        const http = require('http');
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

