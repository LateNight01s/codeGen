import Parser from 'html-tokenizer';
import fs from 'fs';

( async () => {
    await fs.readFile('data/code/10.html', 'utf8', (err, data) => {
        if(data===undefined) return;
         for (const token of Parser.Parser.parse(data)) {
              switch (token.type) {
                case 'open': {
                  console.log(`Opening tag: ${token.name}`);
                  console.log('Attributes:', token.attributes);
                }
                case 'text': {
                  console.log(`Text node: ${token.text}`);
                }
                case 'close': {
                  console.log(`Closing tag: ${token.name}`);
                }
                case 'comment': {
                  console.log(`Comment: ${token.text}`);
                }
              }
           }
    })


})();
