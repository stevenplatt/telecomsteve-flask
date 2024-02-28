var { Readability } = require('@mozilla/readability');
var { JSDOM } = require('jsdom');

var doc = new JSDOM("<body>Look at this cat: <img src='./cat.jpg'></body>", {
        url: "https://www.theverge.com/2024/2/27/24084494/sony-playstation-layoffs-2024"
    });

let reader = new Readability(doc.window.document);
let article = reader.parse();

// Make article globally accessible
global.article = article;