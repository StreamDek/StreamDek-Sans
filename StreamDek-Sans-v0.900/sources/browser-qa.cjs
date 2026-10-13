// Usage: node browser-qa.cjs; playwright must be available on NODE_PATH.
const {chromium}=require('playwright');
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
 const errors=[]; page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
 await page.goto('file:///'+path.join(root,'index.html').replaceAll('\\','/'));await page.evaluate(()=>document.fonts.ready);
 const faces=[];
 for(const dir of ['ttf','otf','woff2','variable'])for(const file of fs.readdirSync(path.join(root,'fonts',dir))){
   if(!/\.(ttf|otf|woff2)$/.test(file))continue;
   const result=await page.evaluate(async({dir,file})=>{
      const f=new FontFace('QA'+file.replace(/\W/g,''),`url("fonts/${dir}/${file}")`);
      try{await f.load();document.fonts.add(f);const c=document.createElement('canvas').getContext('2d');c.font=`32px "${f.family}"`;return {file,status:f.status,width:c.measureText('StreamDek Sans Il1 O0').width}}catch(e){return {file,status:'error',error:String(e)}}
   },{dir,file});faces.push(result);
 }
 await page.locator('#sample').fill('À bientôt · Żółć · Il1 O0 · 01:42:08');
 await page.locator('#weight').fill('725');await page.locator('#weight').dispatchEvent('input');
 await page.locator('#size').fill('36');await page.locator('#size').dispatchEvent('input');
 await page.locator('#zero').check();await page.locator('#theme').click();
 const controls=await page.locator('#live').evaluate(e=>({text:e.textContent,weight:getComputedStyle(e).fontWeight,size:getComputedStyle(e).fontSize,features:getComputedStyle(e).fontFeatureSettings}));
 await page.screenshot({path:path.join(root,'qa','edge-desktop.png')});
 await page.setViewportSize({width:390,height:844});
 const mobileOverflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
 await page.screenshot({path:path.join(root,'qa','edge-mobile.png')});
 const report={browser:browser.version(),engine:'Microsoft Edge / Chromium on Windows; headless',faces,controls,mobileOverflow,errors,status:errors.length||faces.some(f=>f.status!=='loaded')||mobileOverflow?'FAIL':'PASS'};
 fs.writeFileSync(path.join(root,'qa','browser-validation.json'),JSON.stringify(report,null,2));
 await browser.close();console.log(JSON.stringify(report,null,2));if(report.status!=='PASS')process.exit(1);
})();
