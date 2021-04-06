import puppeteer from 'puppeteer';
import fs from 'fs';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

    // W3RESOURCE Examples Webpages
    const WEBSITES = ['https://www.w3schools.com/html/html_examples.asp', 'https://www.w3schools.com/css/css_examples.asp']
    let URLS = []
    for(let URL of WEBSITES){
        await page.goto(URL, {waitUntil: 'load'});
        const LINKS = await page.evaluate(() => {
            let links = Array.from(document.querySelectorAll('div.w3-bar-block'))
            let urls = links.map(item => Array.from(item.children).filter(val => val.href != undefined && val.href != '').map(l => l.href))
            urls = urls.filter(item => item.length>0)
            urls = [].concat.apply([], urls)
            return urls
        })
        URLS = URLS.concat(LINKS)
    }

    // const dimensions = await page.evaluate(() => {
    // return {
    //   width: document.documentElement.clientWidth,
    //   height: document.documentElement.clientHeight,
    //   deviceScaleFactor: window.devicePixelRatio,
    // };
  // });

  // console.log('Dimensions:', dimensions);
     // const frame = await page.evaluate(() => {
     //    return document.getElementById("iframeResult").contentDocument.body;
    // });

        const DIR = 'data/html'
        for(let [index, url] of URLS.entries()){
            try {
                console.log(`fetching ${url}...`)
                await page.goto(url, {waitUntil: 'load'});
                await page.addScriptTag({url: 'https://html2canvas.hertzen.com/dist/html2canvas.min.js'})
                const htmlCode = await page.evaluate(() => {
                    return document.getElementsByClassName('CodeMirror-code')[0].innerText
                })
                await fs.writeFileSync(`${DIR}/${index+1}.html`, htmlCode.replace(/[\u200B-\u200D\uFEFF]/g, ''))
                console.log(`${index+1}.html saved!`)

                const imageData = await page.evaluate(async () => {
                    return html2canvas(document.getElementById('iframeResult').contentDocument.body).then(function(canvas) {
                        return canvas.toDataURL();
                    });
                })
                let data = imageData.replace(/^data:image\/\w+;base64,/, "");
                let buf = new Buffer.from(data, 'base64');
                await fs.writeFileSync(`${DIR}/${index+1}.png`, buf);
                // const ex = await page.$("#iframecontainer")
                // await ex.screenshot({ path: `${DIR}/${index+1}.png` });
                console.log(`${index+1}.png saved!\n`)
            }catch (e){
                console.log(e)
                continue
            }
        }

  await browser.close();
})();
