from pathlib import Path
import sys,json,io,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'font-build-deps'))
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import ImageFont
import uharfbuzz as hb

def shape(data,text,features=None):
    face=hb.Face(data); f=hb.Font(face); hb.ot_font_set_funcs(f)
    b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(f,b,features or {})
    assert all(x.codepoint for x in b.glyph_infos),repr(text)
    return [p.x_advance for p in b.glyph_positions]

src=TTFont(ROOT/'references/InterVariable.ttf');cmap=src.getBestCmap()
files=sorted((ROOT/'fonts').rglob('*'));files=[p for p in files if p.suffix in ['.ttf','.otf','.woff2']]
assert len(files)==24
report={'files':[],'locales':{},'interpolations':[]}
sample='StreamDek AVATAR Reroute The next story starts here. Français Português Zażółć gęślą jaźń Il1 O0 01:42:08 e\u0301'
for p in files:
    f=TTFont(p);assert f.getBestCmap()==cmap;assert f['maxp'].numGlyphs==2937
    assert 'StreamDek' in f['name'].getDebugName(1)
    assert f['name'].getDebugName(0)==src['name'].getDebugName(0)
    assert f['name'].getDebugName(13)==src['name'].getDebugName(13)
    assert ('CFF ' in f) == (p.suffix=='.otf')
    if p.suffix!='.woff2':
        shape(p.read_bytes(),sample)
        for size in [12,16,24,48]:
            font=ImageFont.truetype(str(p),size);assert font.getmask(sample).getbbox()
    report['files'].append({'file':str(p.relative_to(ROOT)),'characters':len(cmap),'glyphs':2937,'parsed':True})
vf=TTFont(ROOT/'fonts/variable/StreamDekSans-Variable.ttf')
axes={a.axisTag:[a.minValue,a.maxValue] for a in vf['fvar'].axes}
assert axes=={'opsz':[14,32],'wght':[300,800]};assert len(vf['fvar'].instances)==6
for weight in [350,550,750]:
    for opsz in [14,23,32]:
        f=instantiateVariableFont(vf,{'wght':weight,'opsz':opsz},inplace=False)
        b=io.BytesIO();f.save(b);shape(b.getvalue(),sample)
        assert ImageFont.truetype(io.BytesIO(b.getvalue()),24).getmask(sample).getbbox()
        report['interpolations'].append({'weight':weight,'opsz':opsz,'shaped_and_rasterised':True})
for loc in ['values','values-de','values-es','values-fr','values-it','values-nl','values-pl','values-pt']:
    p=Path('C:/Dev/StreamDekMobile/android/app/src/main/res')/loc/'strings.xml'
    chars=set(''.join(ET.parse(p).getroot().itertext()));missing=sorted(ord(c) for c in chars if not c.isspace() and ord(c) not in cmap)
    assert not missing,(loc,missing)
    report['locales'][loc]={'distinct_characters':len(chars),'missing':missing}
data=(ROOT/'fonts/ttf/StreamDekSans-Regular.ttf').read_bytes()
assert len(set(shape(data,'0123456789',{'tnum':1})))==1
assert sum(shape(data,'AVATAR',{'kern':1}))<sum(shape(data,'AVATAR',{'kern':0}))
base=instantiateVariableFont(src,{'wght':400,'opsz':14},inplace=False)
custom=TTFont(ROOT/'fonts/ttf/StreamDekSans-Regular.ttf')
assert dict(base['hmtx'].metrics)==dict(custom['hmtx'].metrics)
report.update({'axes':axes,'tabular_numerals':True,'kerning':True,'regular_metrics_unchanged':True,'status':'PASS'})
(ROOT/'qa/validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('PASS: 24 fonts; 8 locales; 9 intermediate instances; shaping, rasterisation, kerning and tabular figures.')
