import { chromium } from 'playwright';
import { mkdirSync, rmSync, writeFileSync } from 'node:fs';
const D='assets/figma/v14/ask_seq/', QS='I want to find someone to go climbing with me';
const b=await chromium.launch();const p=await (await b.newContext({viewport:{width:900,height:1800},deviceScaleFactor:1})).newPage();
await p.goto('http://localhost:5173/',{waitUntil:'networkidle'});
await p.addStyleTag({content:'.device{--device-scale:2 !important} .dynamic-island,.status-bar,.status-time,.status-icons,.home-indicator{visibility:hidden !important} .phone,.device{border-radius:0 !important;box-shadow:none !important}'});
await p.waitForTimeout(1500);
const clip=await p.locator('.phone').boundingBox();
await p.getByRole('button',{name:'Ask me about people'}).click();await p.waitForTimeout(1200);
for(const ch of QS){const k=ch===' '?p.locator('.kb-key.is-space'):p.locator('.kb-keys button').filter({hasText:new RegExp('^'+ch+'$','i')});const bb=await k.first().boundingBox();await p.mouse.click(bb.x+bb.width/2,bb.y+bb.height/2);}
await p.waitForTimeout(600);
if(process.env.KB!=='keep') await p.addStyleTag({content:'.kb{visibility:hidden !important}'});
await p.waitForTimeout(300);
await p.screenshot({path:D+'_query.png',clip});
const cdp=await p.context().newCDPSession(p);const frames=[];
cdp.on('Page.screencastFrame',f=>{frames.push({ts:f.metadata.timestamp,d:f.data});cdp.send('Page.screencastFrameAck',{sessionId:f.sessionId}).catch(()=>{});});
await cdp.send('Page.startScreencast',{format:'jpeg',quality:95,maxWidth:900,maxHeight:1800,everyNthFrame:1});
await p.waitForTimeout(300);
const tc=Date.now()/1000;await p.getByRole('button',{name:'Send'}).click();
await p.waitForTimeout(6000);await cdp.send('Page.stopScreencast');
const fr=frames.slice(Math.max(0,frames.findIndex(f=>f.ts>=tc-0.1)));const T=fr[0].ts,n=Math.floor((fr.at(-1).ts-T)*12);let j=0;
rmSync(D+'raw',{recursive:true,force:true});mkdirSync(D+'raw',{recursive:true});
for(let i=0;i<n;i++){while(j+1<fr.length&&fr[j+1].ts-T<=i/12)j++;writeFileSync(`${D}raw/f${String(i).padStart(3,'0')}.jpg`,Buffer.from(fr[j].d,'base64'));}
writeFileSync(D+'clip.json',JSON.stringify({clip,n,frames:frames.length}));console.log(n,clip,frames.length);
await b.close();
