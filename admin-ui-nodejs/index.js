const express = require("express");
const path = require("path");
require('dotenv').config()
list = require('./public/script.js').Request;

const app = express();
const port = process.env.PORT || "8000";

// app.get("/", (req, res) => {
//     res.status(200).send("WHATABYTE: Food For Devs");
//   });

app.listen(port, () => {
console.log(`Listening to requests on http://localhost:${port}`);
});

// app.set("views", path.join(__dirname, "views"));
// app.set("view engine", "pug");

// app.get("/", (req, res) => {
//     res.render("index", { title: "Home" });
//   });

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, '/public/index.html'));
  });

app.get('/request', async function(req, res) {
    const dataItems = await list.prototype.getAwsData();
    console.log("data sending: ", dataItems);
    res.send(dataItems);
});