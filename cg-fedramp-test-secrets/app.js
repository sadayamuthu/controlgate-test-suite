// Gate 1: Secrets & Credential Gate
const express = require('express');
const app = express();

const dbPassword = "superSecretPassword123!";
const awsAccessKey = "AKIAIOSFODNN7EXAMPLE";

app.get('/', (req, res) => {
    res.send('Hello World!');
});

app.listen(3000, () => {
    console.log('Server is running');
});
