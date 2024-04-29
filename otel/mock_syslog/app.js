const express = require('express')
require('dotenv').config()
const app = express()
const port = 54526
app.get('/', (req, res) => {
    var final = 1000000

    for (var i = 0; i < final; i++) {
        res.write(process.env.LOG_SAMPLE);
        res.write('\n')
        setTimeout(() => { console.log(i); }, i * 1000);
    }    
    res.end();   
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

