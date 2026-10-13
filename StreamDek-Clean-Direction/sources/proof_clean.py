from pathlib import Path
import json,html,shutil
from PIL import Image,ImageDraw,ImageFont
from build_clean import ROOT,STYLES

def font(size,w=400,display=False):
    sub='display' if display else 'ttf'; extra='Display' if display else ''
    return ImageFont.truetype(str(ROOT/'fonts'/sub/f'StreamDekSans-{extra}{STYLES[w]}.ttf'),size)
def text(d,x,y,s,size=26,w=400,fill='#111114',display=False):d.text((x,y),s,font=font(size,w,display),fill=fill,anchor='lt')
def wrap(d,x,y,s,width,size=27,fill='#54565d',leading=42):
    line=''
    for word in s.split():
        test=(line+' '+word).strip()
        if d.textlength(test,font=font(size))>width and line:
            text(d,x,y,line,size,fill=fill);y+=leading;line=word
        else:line=test
    text(d,x,y,line,size,fill=fill);return y+leading
def logo(im,x,y,size=52):
    p=Image.open(ROOT/'specimens/streamdek-logo.png').convert('RGBA');p.thumbnail((size,size),Image.Resampling.LANCZOS);im.paste(p,(x,y),p)

def main():
    source=Path(r'C:\Dev\StreamDekMobile\android\app\src\main\res\drawable-nodpi\streamdek_logo_transparent.png')
    if source.exists():shutil.copy2(source,ROOT/'specimens/streamdek-logo.png')
    im=Image.new('RGB',(1440,1680),'#f8f8fa');d=ImageDraw.Draw(im)
    logo(im,82,68);text(d,154,82,'StreamDek / A cleaner direction',23,500,fill='#63656d')
    text(d,78,192,'StreamDek Sans',104,600,display=True)
    text(d,83,325,'Clean. Balanced. Quietly distinctive.',35,400,fill='#686b73')
    d.line((82,428,1358,428),fill='#d8d9df',width=1)
    text(d,82,478,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',47,500)
    text(d,82,554,'abcdefghijklmnopqrstuvwxyz',58,400)
    text(d,82,650,'0123456789   Aa Ee Rr Tt   Il1 O0',43,400,fill='#656872')
    d.rounded_rectangle((80,771,1360,1425),radius=34,fill='#111114')
    text(d,128,827,'YOUR NEXT GREAT STORY',19,500,fill='#92959e')
    text(d,122,892,'The Last Horizon',80,600,fill='#fafafa',display=True)
    text(d,129,1010,'2026   ·   4K UHD   ·   2h 08m',25,500,fill='#a6a8af')
    wrap(d,129,1084,'An unexpected signal brings two strangers together on a distant coastline. A story about connection, discovery and finding your way home.',1030,30,'#d1d2d7',46)
    d.rounded_rectangle((127,1260,368,1334),radius=19,fill='#f8f8fa')
    d.polygon([(155,1282),(155,1311),(178,1297)],fill='#111114');text(d,198,1283,'Resume',27,600)
    text(d,411,1287,'01:42:08 / 02:08:00',24,500,fill='#a6a8af')
    text(d,83,1491,'Home     Search     Watchlist     My Media     Settings',29,500)
    text(d,83,1580,'Inter-derived design · restrained R, e and t refinements · no application changes',19,400,fill='#797b83')
    im.save(ROOT/'specimens/01-clean-direction.png')
    # Show the important change in rhythm, not just enlarged isolated glyphs.
    im=Image.new('RGB',(1440,1220),'#f8f8fa');d=ImageDraw.Draw(im)
    text(d,78,73,'A different starting point.',70,600,display=True)
    text(d,82,194,'Same sizes and weights. Less geometry, better text rhythm.',25,fill='#6b6e76')
    old=ROOT/'references/previous-rounded-comparison.ttf'
    text(d,82,303,'PREVIOUS ROUNDED DIRECTION',19,500,fill='#797b83')
    d.text((78,359),'StreamDek · Continue Watching',font=ImageFont.truetype(str(old),62),fill='#41434a',anchor='lt')
    d.text((81,459),'A W V Z E U I    a e g s    01:42:08',font=ImageFont.truetype(str(old),49),fill='#41434a',anchor='lt')
    d.line((82,583,1358,583),fill='#d8d9df',width=1)
    text(d,82,653,'NEW CLEAN DIRECTION',19,500,fill='#3070e0')
    text(d,78,709,'StreamDek · Continue Watching',62)
    text(d,81,809,'A W V Z E U I    a e g s    01:42:08',49)
    wrap(d,82,944,'The change is in the underlying letterforms, optical spacing and text/display designs. Rounded caps and repeated geometric shapes no longer drive the appearance.',1210,28,leading=44)
    text(d,82,1142,'Professional Inter foundation, customised under the SIL Open Font License.',21,fill='#797b83')
    im.save(ROOT/'specimens/02-direction-comparison.png')
    im=Image.new('RGB',(1440,1260),'#111114');d=ImageDraw.Draw(im)
    text(d,78,72,'One voice, six weights.',68,600,'#f8f8fa',True)
    for i,(w,s) in enumerate(STYLES.items()):
        y=240+i*142;text(d,83,y+13,f'{w} / {s}',22,400,'#989ba5');text(d,368,y,'The art of watching.',54,w,'#f8f8fa')
    text(d,83,1170,'Weight 300–800 · optical size 14–32 · text and display rendering',22,400,'#989ba5')
    im.save(ROOT/'specimens/03-weights.png')
    im=Image.new('RGB',(1440,1320),'#f8f8fa');d=ImageDraw.Draw(im)
    text(d,65,59,'Text, at actual pixel sizes.',53,600,display=True)
    text(d,66,155,'View at 100%. Native-pixel proof; physical device review is still required.',22,fill='#747781')
    sample='Continue Watching · Français · Português · Zażółć gęślą jaźń · Il1 O0 · 01:42:08'
    for x,bg,fg in [(40,'#f8f8fa','#111114'),(740,'#111114','#f8f8fa')]:
        d.rounded_rectangle((x,230,x+660,1260),radius=22,fill=bg);y=266
        for size in [12,14,16,18,20,24,28]:
            text(d,x+24,y,f'{size} px / Regular',16,500,fg);y+=38
            y=wrap(d,x+24,y,sample,610,size,fg,round(size*1.55))+36
    im.save(ROOT/'specimens/04-small-text.png')
    im=Image.new('RGB',(1920,1080),'#111114');d=ImageDraw.Draw(im);logo(im,112,78,65)
    text(d,218,95,'StreamDek',37,600,'#fafafa')
    text(d,871,102,'Home      Search      Watchlist      Settings',29,500,'#b7b9c1')
    text(d,105,292,'The Last Horizon',104,600,'#fafafa',True)
    text(d,112,436,'2026    4K UHD    2h 08m    Subtitles',28,500,'#a9acb5')
    wrap(d,111,536,'An unexpected signal. A distant coastline. One journey that changes everything. Discover your next favourite story.',1270,35,'#d3d4db',55)
    d.rounded_rectangle((110,738,421,825),radius=24,fill='#fafafa');d.polygon([(147,764),(147,800),(175,782)],fill='#111114');text(d,211,766,'Resume',32,600)
    text(d,111,969,'1080p design proof · physical TV-distance readability has not been tested',22,400,'#858993')
    im.save(ROOT/'specimens/05-tv-proof.png')
    provenance=json.loads((ROOT/'qa/provenance.json').read_text())
    doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>StreamDek Sans — Clean direction</title><style>
@font-face{font-family:StreamDek;src:url('fonts/variable/StreamDekSans-Variable.woff2') format('woff2');font-weight:300 800;font-display:swap}
*{box-sizing:border-box}body{margin:0;background:#f8f8fa;color:#111114;font-family:StreamDek,Arial,sans-serif;font-optical-sizing:auto;font-synthesis:none;line-height:1.55}main{max-width:1140px;margin:auto;padding:52px 28px}header{display:flex;align-items:center;gap:18px;color:#71747d;font-size:17px}header img{width:46px}h1{font-size:clamp(48px,8vw,94px);font-weight:600;letter-spacing:-.045em;line-height:1.05;margin:72px 0 24px}h2{font-size:34px;letter-spacing:-.03em;font-weight:600;margin:56px 0 22px}p{font-size:20px;color:#6b6f78;max-width:770px}a{color:#286bd8}section{padding:30px;border:1px solid #dadce2;border-radius:24px;margin:30px 0;background:white}.controls{display:flex;gap:30px;flex-wrap:wrap;margin:22px 0}label{display:grid;gap:8px;font-size:15px}input[type=text]{font:inherit;border:1px solid #c9cdd5;border-radius:10px;padding:14px;width:100%;background:white;color:#111114}input[type=range]{width:200px;accent-color:#286bd8}button{font:inherit;border:1px solid #c9cdd5;border-radius:10px;background:#f5f6f9;color:#111114;padding:12px 20px;cursor:pointer}#live{font-size:60px;line-height:1.3;margin:35px 0 12px;min-height:130px;overflow-wrap:anywhere;letter-spacing:-.025em}.dark{background:#111114;color:#f8f8fa}.dark input[type=text]{background:#24262d;color:#fafafa;border-color:#50545f}.weight{display:grid;grid-template-columns:190px 1fr;align-items:center;border-bottom:1px solid #d8dbe2;padding:25px 0}.weight small{color:#747883}.weight div{font-size:42px;letter-spacing:-.025em}figure{margin:38px 0}figure img{width:100%;height:auto;border-radius:14px;display:block}figcaption{font-size:14px;color:#797d86;margin-top:9px}footer{margin:65px 0 20px;color:#797d86;font-size:15px}@media(max-width:650px){main{padding:28px 18px}section{padding:20px}.weight{grid-template-columns:1fr;gap:6px}.weight div{font-size:30px}#live{font-size:40px}}
</style><main><header><img src="specimens/streamdek-logo.png" alt="StreamDek logo">StreamDek / Clean direction</header><h1>StreamDek Sans</h1><p>A professional UI foundation with restrained custom details. Balanced proportions, optical sizing and a natural rhythm at every size.</p><p style="font-size:15px">Based on <a href="https://rsms.me/inter/">Inter 4.1</a> under the <a href="OFL.txt">SIL Open Font License</a>. This is an explicitly documented derivative, with subtle R, e and t outline refinements.</p>
<section id="panel"><label>Your text<input type="text" id="sample" value="The next story starts here."></label><div class="controls"><label>Weight <output id="wvalue">400</output><input id="weight" type="range" min="300" max="800" value="400"></label><label>Size <output id="svalue">60 px</output><input id="size" type="range" min="12" max="100" value="60"></label><button id="theme">Light / dark</button></div><div id="live">The next story starts here.</div></section>
<h2>Six weights. Text and display optics.</h2>WEIGHTS
<h2>Design proofs</h2>PROOFS
<footer><a href="docs/DESIGN.md">Design and provenance</a> · <a href="docs/VALIDATION.md">Validation</a> · <a href="docs/INTEGRATION.md">Future integration</a><br>No app changes. Final device and physical TV-distance review remains pending.</footer></main>
<script>const $=id=>document.getElementById(id);function update(){const w=$('weight').value,s=$('size').value;$('live').textContent=$('sample').value;$('live').style.fontWeight=w;$('live').style.fontSize=s+'px';$('wvalue').textContent=w;$('svalue').textContent=s+' px'}['sample','weight','size'].forEach(id=>$(id).addEventListener('input',update));$('theme').onclick=()=>$('panel').classList.toggle('dark');</script></html>'''
    rows=''.join(f'<div class="weight"><small>{w} / {s}</small><div style="font-weight:{w}">The art of watching.</div></div>' for w,s in STYLES.items())
    proofs=''.join(f'<figure><img src="specimens/{p.name}" alt="{p.stem}" loading="lazy"><figcaption>{p.stem.replace("-"," ")}</figcaption></figure>' for p in sorted((ROOT/'specimens').glob('0*.png')))
    (ROOT/'index.html').write_text(doc.replace('WEIGHTS',rows).replace('PROOFS',proofs),encoding='utf-8')
    print('Proofs rendered',flush=True)
if __name__=='__main__':main()
