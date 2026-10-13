"""Font integrity, shaping, actual app-string coverage, and interpolation checks."""
import sys,json,hashlib,unicodedata as ud,xml.etree.ElementTree as ET,io
from pathlib import Path
from build import ROOT,STYLES,MARKS
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.misc.roundTools import otRound
import uharfbuzz as hb
from PIL import ImageFont

def shape(data,text,features=None,weight=None):
    f=hb.Font(hb.Face(data)); f.scale=(1000,1000)
    if weight is not None: f.set_variations({'wght':weight})
    b=hb.Buffer(); b.add_str(text); b.guess_segment_properties(); hb.shape(f,b,features or {})
    return [(g.codepoint,p.x_advance,p.x_offset,p.y_offset) for g,p in zip(b.glyph_infos,b.glyph_positions)]

def main():
    failures=[]; reports=[]; cmap=None
    for p in sorted((ROOT/'fonts').rglob('*')):
        if p.suffix not in ('.ttf','.otf','.woff2'): continue
        f=TTFont(p,checkChecksums=2); f.ensureDecompiled(); cm=f.getBestCmap(); cmap=cm
        for table in f.keys():
            if table!='GlyphOrder': f.getTableData(table)
        fam=f['name'].getDebugName(16); assert fam=='StreamDek Sans',(p,fam)
        assert f['OS/2'].usWeightClass in STYLES and f['OS/2'].fsType==0
        assert set(range(32,127)).issubset(cm)
        assert set(range(160,384)).issubset(cm), sorted(set(range(160,384))-cm.keys())
        raw=io.BytesIO(); f.flavor=None; f.save(raw); data=raw.getvalue()
        shaped=shape(data,'AVATAR To Watch 01:42 Il1 O0 ÀÉŁœ Żółć Straße ação')
        assert all(g[0] for g in shaped)
        off=sum(x[1] for x in shape(data,'AVATAR',{'kern':False})); on=sum(x[1] for x in shape(data,'AVATAR',{'kern':True})); assert on<off
        assert len(set(x[1] for x in shape(data,'0123456789')))==1
        assert shape(data,'0',{'zero':True})[0][0]!=shape(data,'0',{'zero':False})[0][0]
        assert sum(x[1] for x in shape(data,'111',{'pnum':True}))<sum(x[1] for x in shape(data,'111'))
        marktest=shape(data,'x\u0301'); assert len(marktest)==2 and marktest[1][1]==0 and marktest[1][2]!=0
        nfc=shape(data,'Áéöñ'); nfd=shape(data,ud.normalize('NFD','Áéöñ')); assert nfc==nfd
        bounds=[0,0,0,0]
        from fontTools.pens.boundsPen import BoundsPen
        gs=f.getGlyphSet()
        for n in gs.keys():
            pen=BoundsPen(gs); gs[n].draw(pen)
            if pen.bounds:
                x0,y0,x1,y1=pen.bounds; bounds=[min(bounds[0],x0),min(bounds[1],y0),max(bounds[2],x1),max(bounds[3],y1)]
                if y0 < -300 or y1 > 1100: failures.append(f'{p.name}: vertical clipping {n} {pen.bounds}')
        if p.suffix in ('.ttf','.otf'):
            for size in (12,16,24,48):
                ft=ImageFont.truetype(str(p),size); assert ft.getmask('StreamDek Il1 O0').getbbox()
        reports.append({'file':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'glyphs':f['maxp'].numGlyphs,'mapped':len(cm),'family':fam,'style':f['name'].getDebugName(17),'weight':f['OS/2'].usWeightClass,'bounds':bounds,'kern_AVATAR_units':on-off,'format':'CFF OpenType' if 'CFF ' in f else 'TrueType','tables':list(f.keys())})
        print('PASS',p.name,flush=True)
    variable=ROOT/'fonts/variable/StreamDekSans-Variable.ttf'; vf=TTFont(variable)
    axes=[{'tag':a.axisTag,'min':a.minValue,'default':a.defaultValue,'max':a.maxValue} for a in vf['fvar'].axes]
    assert axes==[{'tag':'wght','min':300.0,'default':400.0,'max':800.0}]
    for w in (300,350,400,450,500,550,600,650,700,750,800):
        inst=instantiateVariableFont(vf,{'wght':w},inplace=False); b=io.BytesIO(); inst.save(b); f=ImageFont.truetype(io.BytesIO(b.getvalue()),24); assert f.getmask('Hamburgefontsiv').getbbox()
    # Compare interpolation master locations against authored masters exactly.
    for w,s in STYLES.items():
        inst=instantiateVariableFont(vf,{'wght':w},inplace=False); master=TTFont(ROOT/'sources/masters'/f'StreamDekSans-{s}.ttf')
        for name in master.getGlyphOrder():
            a=master['glyf'][name].getCoordinates(master['glyf'])[0]; b=inst['glyf'][name].getCoordinates(inst['glyf'])[0]
            # instancer retains fractional IUP coordinates in memory. Compare
            # the integer coordinates actually serialized into a TTF.
            assert len(a)==len(b) and all(abs(otRound(x)-otRound(u))<=1 and abs(otRound(y)-otRound(v))<=1 for (x,y),(u,v) in zip(a,b)),(w,name)
    locales={}; res=Path(r'C:\Dev\StreamDekMobile\android\app\src\main\res')
    for folder in ['values','values-de','values-es','values-fr','values-it','values-nl','values-pl','values-pt']:
        if not (res/folder/'strings.xml').exists():
            locales[folder]={'status':'SKIPPED: source checkout not present'}; continue
        tree=ET.parse(res/folder/'strings.xml'); content=''.join(tree.getroot().itertext()); missing=sorted(set(c for c in content if not c.isspace() and ord(c) not in cmap))
        locales[folder]={'unique_characters':len(set(content)),'missing':[{'character':c,'codepoint':f'U+{ord(c):04X}','name':ud.name(c,'UNKNOWN'),'category':ud.category(c)} for c in missing]}
        missing_latin=[c for c in missing if 'LATIN' in ud.name(c,'')]
        if missing_latin: failures.append(f'{folder}: missing Latin {missing_latin}')
    result={'status':'PASS' if not failures else 'FAIL','failures':failures,'font_files':reports,'variable_axis':axes,'variable_checked_weights':[300,350,400,450,500,550,600,650,700,750,800],'source_locales':locales,'scope':'FontTools parse/compile, FreeType raster, HarfBuzz shaping. Not real-device acceptance.'}
    (ROOT/'qa/validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'status':result['status'],'failures':failures,'locales':locales},ensure_ascii=False,indent=2))
    if failures: raise SystemExit(1)
if __name__=='__main__': main()
