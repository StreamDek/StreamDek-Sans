"""Render standalone specimens, glyph galleries and an interactive local proof."""
from pathlib import Path
import sys,json,shutil,html,math
from PIL import Image,ImageDraw,ImageFont
from build import ROOT,STYLES

BG='#0b0b0f'; INK='#f5f7fb'; MUTED='#a3a8b0'; ACCENT='#34ceda'
def font(size,weight=400): return ImageFont.truetype(str(ROOT/'fonts/ttf'/f'StreamDekSans-{STYLES[weight]}.ttf'),size)
def text(d,xy,s,size=28,weight=400,fill=INK,**kw): d.text(xy,s,font=font(size,weight),fill=fill,anchor='lt',**kw)
def rule(d,y,w=1440): d.line((72,y,w-72,y),fill='#30333b',width=1)
def logo(im,xy,size):
    q=Image.open(ROOT/'specimens/streamdek-logo.png').convert('RGBA'); q.thumbnail((size,size),Image.Resampling.LANCZOS); im.paste(q,xy,q)
def header(im,d,number,title,subtitle):
    logo(im,(72,58),50); text(d,(142,64),'StreamDek / Type studio',22,500); text(d,(1230,64),number,20,500,ACCENT)
    text(d,(72,155),title,66,500); text(d,(74,249),subtitle,22,400,MUTED); rule(d,310)
def wrap(d,s,x,y,width,size=25,weight=400,fill=INK,leading=38):
    line=''
    for word in s.split():
        test=(line+' '+word).strip()
        if d.textlength(test,font=font(size,weight))>width and line:
            text(d,(x,y),line,size,weight,fill); y+=leading; line=word
        else: line=test
    if line: text(d,(x,y),line,size,weight,fill); y+=leading
    return y

def sheets():
    source_logo=Path(r'C:\Dev\StreamDekMobile\android\app\src\main\res\drawable-nodpi\streamdek_logo_transparent.png')
    if source_logo.exists(): shutil.copy2(source_logo,ROOT/'specimens/streamdek-logo.png')
    im=Image.new('RGB',(1440,1800),BG); d=ImageDraw.Draw(im)
    header(im,d,'01 / 06','StreamDek Sans','Original letterforms. Six weights. One continuous voice.')
    text(d,(72,355),'Made for the',96,300); text(d,(72,475),'next great story.',96,700)
    text(d,(74,632),'Quiet geometry. Open counters. Softly finished terminals.',26,400,MUTED)
    for i,(w,s) in enumerate(STYLES.items()):
        y=740+i*132; text(d,(74,y+9),f'{w}  /  {s}',21,400,MUTED); text(d,(360,y),'The art of watching.',53,w)
    rule(d,1560); text(d,(72,1610),'a e g s    I l 1    O 0    01:42:08',56,500)
    text(d,(72,1720),'REVIEW BUILD 0.900  /  ORIGINAL OUTLINES  /  NO APP INTEGRATION',17,500,MUTED)
    im.save(ROOT/'specimens/01-family.png')
    im=Image.new('RGB',(1440,1800),'#f5f4f0'); d=ImageDraw.Draw(im)
    text(d,(72,62),'STREAMDEK SANS / CHARACTER STUDY',21,500,'#555c66')
    text(d,(72,140),'Clarity, by design.',77,500,'#16181d')
    rows=[('UPPERCASE','ABCDEFGHIJKLM\nNOPQRSTUVWXYZ',73),('LOWERCASE','abcdefghijklm\nnopqrstuvwxyz',81),('NUMERALS & SIGNS','0123456789\n€ £ $ ¥  % & @ #  + − × ÷',63),('ACCENTS & LANGUAGE','À Á Â Ã Ä Å Æ Ç È É Ê Ë\nŁ ł Ń ń Œ œ ß Ş ş Ž ž',53)]
    y=310
    for label,s,size in rows:
        text(d,(74,y),label,18,500,'#6b717b'); y+=48
        for line in s.split('\n'): text(d,(72,y),line,size,400,'#16181d'); y+=size+28
        y+=30
    text(d,(72,1515),'“One more episode?”  —  2026',43,500,'#16181d')
    text(d,(72,1605),'Il1  O0  rn m  cl d  vv w  a e g s',45,400,'#16181d')
    text(d,(72,1720),'Cap height 700 / x-height 520 / 1000 units per em',20,400,'#656b73')
    im.save(ROOT/'specimens/02-characters.png')
    im=Image.new('RGB',(1440,1800),BG); d=ImageDraw.Draw(im)
    header(im,d,'03 / 06','A place for every story.','Standalone composition using the existing StreamDek logo.')
    d.rounded_rectangle((72,358,1368,1090),radius=32,fill='#171a21')
    text(d,(112,403),'STREAMDEK ORIGINAL / DESIGN SAMPLE',19,600,ACCENT)
    text(d,(110,485),'The Last',96,300); text(d,(110,601),'Horizon',112,700)
    text(d,(115,759),'2026    •    4K UHD    •    2h 08m    •    CC',23,500,MUTED)
    wrap(d,'At the edge of a quiet ocean, an unexpected signal brings two strangers together. A story about finding your way home.',115,820,870,27,400,INK,43)
    d.rounded_rectangle((112,961,343,1030),radius=22,fill=INK)
    d.polygon([(141,981),(141,1011),(165,996)],fill=BG); text(d,(185,982),'Resume',27,600,BG)
    text(d,(385,983),'01:42:08 / 02:08:00',26,500,MUTED)
    text(d,(74,1150),'Continue Watching',43,600)
    cards=[('Northern Lights','Series / S02 E04'),('The Quiet Sea','Film / 2026'),('After Midnight','Series / S01 E08')]
    for i,(a,b) in enumerate(cards):
        x=72+i*438; d.rounded_rectangle((x,1230,x+414,1462),radius=22,fill=['#182d38','#253b3d','#2b253d'][i])
        d.line((x+26,1427,x+388,1427),fill='#56606b',width=5); d.line((x+26,1427,x+250,1427),fill=ACCENT,width=5)
        text(d,(x,1500),a,28,500); text(d,(x,1548),b,19,400,MUTED)
    rule(d,1620); text(d,(102,1666),'Home     Search     Watchlist     My Media     Settings',30,500)
    text(d,(72,1750),'Logo copied from the existing app. Control geometry is illustrative.',17,400,MUTED)
    im.save(ROOT/'specimens/03-brand-preview.png')
    # Pixel-sized proof: rendered directly at these sizes, without supersampling.
    im=Image.new('RGB',(1440,1400),'#f5f4f0'); d=ImageDraw.Draw(im)
    text(d,(64,55),'Small text / native pixel proof',52,500,'#16181d')
    text(d,(64,139),'View at 100%. These are pixel sizes, not a phone or TV certification.',22,400,'#5e6672')
    sample='Continue Watching  •  Episode 04  •  01:42:08  •  Il1 O0  •  Français / Português / Polski'
    for col,bg,fg in [(0,'#f5f4f0','#16181d'),(1,BG,INK)]:
        x=40+col*700; d.rounded_rectangle((x,210,x+660,1330),radius=20,fill=bg)
        y=250
        for size in [12,14,16,18,20,24,28,32]:
            text(d,(x+24,y),f'{size} px / Regular',17,500,fg); y+=34
            y=wrap(d,sample,x+24,y,610,size,400,fg,round(size*1.6))+32
    im.save(ROOT/'specimens/04-small-sizes.png')
    # TV proof at a genuine 1920 x 1080 frame; physical distance remains a review.
    im=Image.new('RGB',(1920,1080),BG); d=ImageDraw.Draw(im); logo(im,(100,65),68)
    text(d,(212,82),'StreamDek',42,600); text(d,(790,91),'Home     Search     Watchlist     Settings',30,500,MUTED)
    text(d,(105,246),'The Last Horizon',96,600); text(d,(109,377),'2026    4K UHD    2h 08m    Subtitles',30,500,MUTED)
    wrap(d,'An unexpected signal. A distant coastline. One journey that changes everything. Discover your next favourite story.',110,460,1100,36,400,INK,56)
    d.rounded_rectangle((108,660,405,748),radius=28,fill=INK); d.polygon([(142,686),(142,722),(170,704)],fill=BG); text(d,(194,686),'Resume',36,600,BG)
    d.line((110,877,1810,877),fill='#40444d',width=6); d.line((110,877,1350,877),fill=ACCENT,width=6)
    text(d,(109,930),'01:42:08',28,500); text(d,(1660,930),'02:08:00',28,500,MUTED)
    text(d,(109,1020),'1080p DESIGN PROOF / Assess at native resolution on your target TV and viewing distance.',19,400,MUTED)
    im.save(ROOT/'specimens/05-tv-1080p.png')
    im=Image.new('RGB',(1440,1540),'#f5f4f0'); d=ImageDraw.Draw(im)
    text(d,(72,65),'Reference, not a template.',63,500,'#16181d')
    text(d,(74,171),'Same 64 px size and sample. Outlines are independently authored.',22,400,'#5e6672')
    sf=ImageFont.truetype(str(ROOT/'references/GoogleSans-Regular.ttf'),64)
    for y,label,f in [(290,'StreamDek Sans / Regular / original',font(64)),(590,'Google Sans / Regular / reference only',sf)]:
        text(d,(74,y),label,22,500,'#5e6672')
        d.text((72,y+61),'StreamDek  /  The next story',font=f,fill='#16181d',anchor='lt')
        d.text((72,y+163),'a e g s   I l 1   O 0   012345',font=f,fill='#16181d',anchor='lt')
    text(d,(74,954),'SF Pro Rounded',35,500,'#16181d')
    wrap(d,'Reference link only. No Apple font is bundled or rendered here because its published license restricts use in mockups for non-Apple platforms.',74,1026,1220,26,400,'#5e6672',40)
    text(d,(74,1201),'Design response',31,500,'#16181d')
    wrap(d,'StreamDek Sans keeps generous apertures, a high x-height and quiet geometry. Its restrained terminal rounding, footed l and dotted zero establish a separate UI voice.',74,1260,1210,26,400,'#5e6672',40)
    im.save(ROOT/'specimens/06-reference-comparison.png')
    im=Image.new('RGB',(1440,1800),BG); d=ImageDraw.Draw(im)
    header(im,d,'07 / 07','Stories, in every detail.','Reading texture and the eight current StreamDek locales.')
    para=('When a message arrives from a station thought to be abandoned, a documentary filmmaker returns to the coast where she grew up. '
          'The familiar harbour has changed, but the people who kept its stories are still there. Across one extraordinary summer, she follows a trail of recordings, '
          'rebuilds an old friendship and discovers why some memories are worth returning to. Beautifully observed and quietly surprising, The Last Horizon is a story '
          'about listening closely, finding connection and choosing what comes next. Continue from where you left off, explore the complete series, or save it for a quieter evening. '
          'Subtitles and audio options are available in the player. Your next great story can begin whenever you are ready.')
    y=wrap(d,para,74,365,1270,26,400,INK,42)
    rule(d,y+36); y+=90
    languages=[('English','Continue Watching · My Media · Next episode'),('Deutsch','Weiterschauen · Größe · Straße · Über uns'),('Español','Continuar viendo · Películas · Próximo episodio'),('Français','Continuer à regarder · Œuvre · Épisode suivant'),('Italiano','Continua a guardare · Novità · Prossimo episodio'),('Nederlands','Verder kijken · Mijn media · Volgende aflevering'),('Polski','Kontynuuj oglądanie · Zażółć gęślą jaźń'),('Português','Continuar a ver · Séries · Próximo episódio')]
    for label,sample in languages:
        text(d,(74,y),label,19,500,MUTED); text(d,(295,y-3),sample,26,400); y+=88
    text(d,(74,1726),'Language samples illustrate glyph coverage; they do not change application translations.',17,400,MUTED)
    im.save(ROOT/'specimens/07-reading-languages.png')
    coverage=json.loads((ROOT/'qa/coverage.json').read_text(encoding='utf-8'))
    for page in range(math.ceil(len(coverage)/96)):
        im=Image.new('RGB',(1440,1850),'white'); d=ImageDraw.Draw(im)
        text(d,(50,28),f'StreamDek Sans / complete glyph proof / {page+1}',32,500,'#111111')
        for i,item in enumerate(coverage[page*96:(page+1)*96]):
            x=40+(i%8)*175; y=100+(i//8)*143
            d.rectangle((x,y,x+166,y+132),outline='#dddddd')
            text(d,(x+10,y+12),item['codepoint'],14,400,'#747474')
            d.text((x+80,y+90),item['character'],font=font(49),fill='#111111',anchor='ms')
        im.save(ROOT/f'specimens/glyphs-{page+1:02}.png')

def web():
    rows=''.join(f'<div class="weight"><small>{w} / {s}</small><div style="font-weight:{w}">The art of watching.</div></div>' for w,s in STYLES.items())
    samples=''.join(f'<figure><img loading="lazy" src="specimens/{p.name}" alt="{p.stem}"><figcaption>{p.stem.replace("-"," ")}</figcaption></figure>' for p in sorted((ROOT/'specimens').glob('0*.png')))
    doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>StreamDek Sans — Type specimen</title>
<style>
@font-face{font-family:StreamDek;src:url('fonts/variable/StreamDekSans-Variable.woff2') format('woff2');font-weight:300 800;font-display:swap}
@font-face{font-family:GoogleRef;src:url('references/GoogleSans-Regular.ttf') format('truetype');font-weight:400}
*{box-sizing:border-box}body{margin:0;background:#0b0b0f;color:#f5f7fb;font-family:StreamDek,Arial,sans-serif;font-synthesis:none;line-height:1.5}main{max-width:1180px;margin:auto;padding:45px 32px}header{display:flex;gap:18px;align-items:center;color:#a3a8b0}header img{width:46px}h1{font-size:clamp(48px,8vw,104px);line-height:1.1;font-weight:500;letter-spacing:-.025em;margin:70px 0 28px}p{max-width:760px;color:#a3a8b0;font-size:20px}a{color:#6fe1e7}h2{font-weight:500;font-size:36px;margin:50px 0 20px}.tag{color:#6fe1e7;font-size:14px;text-transform:uppercase;letter-spacing:.1em}.panel{background:#171a21;border-radius:24px;padding:32px;margin:28px 0}.controls{display:flex;flex-wrap:wrap;gap:28px;align-items:center}label{display:grid;gap:7px;font-size:16px}input[type=range]{accent-color:#34ceda;width:210px}input[type=text]{font:inherit;color:inherit;background:#242831;border:1px solid #454a56;border-radius:10px;padding:12px;width:100%}button{background:#f5f7fb;color:#111;font:inherit;border:0;border-radius:10px;padding:10px 16px;cursor:pointer}#live{padding:45px 0 20px;font-size:64px;line-height:1.4;overflow-wrap:anywhere;min-height:180px}#test-panel.light{background:#f5f4f0;color:#16181d}.weight{display:grid;grid-template-columns:200px 1fr;gap:24px;border-bottom:1px solid #30333b;padding:25px 0;align-items:center}.weight small{color:#a3a8b0}.weight div{font-size:44px}.alphabet{font-size:36px;overflow-wrap:anywhere}.comparison{display:grid;grid-template-columns:1fr 1fr;gap:25px}.comparison div{font-size:33px}.comparison small{display:block;font:14px Arial;color:#a3a8b0;margin-bottom:20px}.google{font-family:GoogleRef}figure{margin:32px 0}figure img{width:100%;height:auto;display:block;border-radius:12px}figcaption{color:#a3a8b0;font-size:14px;padding-top:10px}.links{display:flex;gap:22px;flex-wrap:wrap}footer{border-top:1px solid #30333b;margin-top:70px;padding-top:30px;color:#a3a8b0}@media(max-width:700px){main{padding:24px 18px}.panel{padding:22px}.weight{grid-template-columns:1fr;gap:8px}.weight div{font-size:32px}.comparison{grid-template-columns:1fr}#live{font-size:40px}}
</style><main><header><img src="specimens/streamdek-logo.png" alt="StreamDek logo">StreamDek / Type studio</header>
<h1>StreamDek Sans</h1><div class="tag">Original family · 300–800 · Review build 0.900</div>
<p>Quiet geometry for a world of stories. Six independently generated weights, a continuous weight axis, and softly finished original letterforms.</p>
<div class="links"><a href="docs/DESIGN.md">Design specifications</a><a href="docs/VALIDATION.md">Validation & limitations</a><a href="docs/INTEGRATION.md">Future integration guide</a><a href="LICENSE.txt">License & provenance</a></div>
<h2>Make it your own sentence.</h2><section class="panel" id="test-panel"><label>Sample text<input id="sample" type="text" value="The next story starts here."></label><div class="controls"><label>Weight <output id="weight-value">400</output><input id="weight" type="range" min="300" max="800" value="400"></label><label>Size <output id="size-value">64 px</output><input id="size" type="range" min="12" max="112" value="64"></label><button id="theme" type="button">Light / dark</button><label><span>Slashed zero</span><input type="checkbox" id="zero"></label></div><div id="live" aria-live="polite">The next story starts here.</div></section>
<h2>Six weights. A consistent voice.</h2>ROWS
<h2>Letters, numbers, detail.</h2><section class="panel alphabet">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>0123456789 / Il1 O0 rn m<br>ÀÁÂÃÄÅ Æ Ç ÈÉÊË Łł Œœ ß Żż<br>€ £ $ ¥ © ® ™ … — « » “ ”</section>
<h2>A reference, never a source.</h2><section class="panel comparison"><div><small>STREAMDEK SANS / REGULAR</small>The next story.<br>a e g s / Il1 O0</div><div class="google"><small>GOOGLE SANS / REGULAR</small>The next story.<br>a e g s / Il1 O0</div></section><p>Google Sans is included under its <a href="references/GoogleSans-OFL.txt">OFL license</a> solely as a reference. <a href="https://developer.apple.com/fonts/">SF Pro Rounded’s official reference</a> is linked; its font is not bundled or rendered for this non-Apple specimen.</p>
<h2>Specimen collection</h2>SHEETS
<footer>This is a standalone design artifact. Application files have not been changed. Real-device readability, platform rendering and final design approval remain release gates.</footer></main>
<script>const $=id=>document.getElementById(id);function update(){const w=$('weight').value,s=$('size').value;$('live').textContent=$('sample').value;$('live').style.fontWeight=w;$('live').style.fontSize=s+'px';$('live').style.fontFeatureSettings=$('zero').checked?'"zero" 1':'"zero" 0';$('weight-value').textContent=w;$('size-value').textContent=s+' px'}['sample','weight','size','zero'].forEach(id=>$(id).addEventListener('input',update));$('theme').onclick=()=>$('test-panel').classList.toggle('light');document.fonts.ready.then(()=>document.documentElement.dataset.fonts='ready');</script></html>'''
    (ROOT/'index.html').write_text(doc.replace('ROWS',rows).replace('SHEETS',samples),encoding='utf-8')
if __name__=='__main__': sheets(); web(); print('Specimens rendered')
