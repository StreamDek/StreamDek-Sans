"""StreamDek Sans clean direction, derived from Inter 4.1 under SIL OFL 1.1.
Preserve professional construction, spacing, marks and optical-size masters.
Only documented coordinate refinements are introduced; no global rounding.
"""
from pathlib import Path
import sys,copy,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'font-build-deps'))
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.ttLib.tables._f_v_a_r import NamedInstance
from fontTools.otlLib.builder import buildStatTable
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.qu2cuPen import Qu2CuPen

STYLES={300:'Light',400:'Regular',500:'Medium',600:'SemiBold',700:'Bold',800:'ExtraBold'}
FAMILY='StreamDek Sans'
# Point indices are pinned to the official Inter 4.1 variable release. Offsets
# are small (8–20 in a 2048-unit em), affect matching inner/outer boundaries,
# and leave advance widths, accent anchors and original variation deltas intact.
# Each indexed point receives the same offset at every weight/optical size.
EDITS={
 'R':{24:(18,0),27:(18,0)}, # Slightly more forward-directed diagonal foot.
 'e':{34:(0,-8),35:(0,-16),36:(0,-16),37:(0,-8)}, # Open the lower aperture.
 't':{10:(5,2),11:(14,5),12:(20,8),13:(20,8),14:(14,5),15:(5,2)},
 't.1':{10:(5,2),11:(14,5),12:(20,8),13:(20,8),14:(14,5),15:(5,2)},
}

def names(f,style,weight,variable=False):
    legacy=FAMILY if weight in (400,700) else FAMILY+' '+style
    values={1:legacy,2:'Bold' if weight==700 else 'Regular',3:f'StreamDekSans:0.920:{style}',
      4:FAMILY+' '+style,5:'Version 0.920',6:'StreamDekSans-'+('Variable' if variable else style),
      8:'StreamDek customisation',9:'Based on Inter by Rasmus Andersson; StreamDek refinement with Codex',
      10:'Inter-derived clean UI edition. Refined R, e and t details; original optical sizes and spacing retained.',
      16:FAMILY,17:style,25:'StreamDekSans'}
    for i,v in values.items():
        f['name'].removeNames(nameID=i)
        f['name'].setName(v,i,3,1,0x409)
        f['name'].setName(v,i,1,0,0)
    # Original copyright, trademark acknowledgement and OFL records retained.
    f['head'].fontRevision=.920; f.recalcTimestamp=False
    f['OS/2'].usWeightClass=weight
    f['OS/2'].fsSelection=(f['OS/2'].fsSelection & ~((1<<5)|(1<<6))) | ((1<<5) if weight==700 else (1<<6))
    f['head'].macStyle=(f['head'].macStyle & ~1) | (1 if weight==700 else 0)

def make_otf(f,path):
    fb=FontBuilder(f['head'].unitsPerEm,isTTF=False); gs=f.getGlyphSet()
    fb.setupGlyphOrder(f.getGlyphOrder()); fb.setupCharacterMap(f.getBestCmap()); cs={}
    for n in f.getGlyphOrder():
        pen=T2CharStringPen(f['hmtx'][n][0],gs)
        gs[n].draw(Qu2CuPen(pen,max_err=.5,all_cubic=True));cs[n]=pen.getCharString()
    fb.setupCFF(f['name'].getDebugName(6),{'FullName':f['name'].getDebugName(4),'FamilyName':FAMILY,'Weight':f['name'].getDebugName(17),'version':'0.920'},cs,{})
    for table in ['hmtx','hhea','name','OS/2','GPOS','GSUB','GDEF']:
        if table in f: fb.font[table]=copy.deepcopy(f[table])
    fb.setupPost(); fb.font['head'].fontRevision=.920; fb.font['head'].macStyle=f['head'].macStyle
    fb.font.recalcTimestamp=False;fb.save(path)

def main():
    for d in ['fonts/ttf','fonts/otf','fonts/woff2','fonts/variable','fonts/display','qa','specimens','docs']:(ROOT/d).mkdir(parents=True,exist_ok=True)
    src=ROOT/'references/InterVariable.ttf'; f=TTFont(src)
    assert f['head'].unitsPerEm==2048 and f['maxp'].numGlyphs==2937
    change=[]
    for n,points in EDITS.items():
        g=f['glyf'][n]; assert not g.isComposite()
        for i,(dx,dy) in points.items():
            x,y=g.coordinates[i];g.coordinates[i]=(x+dx,y+dy)
            change.append({'glyph':n,'point':i,'before':[x,y],'after':[x+dx,y+dy]})
        g.recalcBounds(f['glyf'])
    f=instantiateVariableFont(f,{'wght':(300,400,800)},inplace=True)
    names(f,'Regular',400,True)
    f['fvar'].instances=[]
    for w,s in STYLES.items():
        ins=NamedInstance();ins.subfamilyNameID=f['name'].addName(s);ins.postscriptNameID=f['name'].addName('StreamDekSans-'+s)
        ins.coordinates={'wght':w,'opsz':14};f['fvar'].instances.append(ins)
    buildStatTable(f,[{'tag':'opsz','name':'Optical size','values':[{'value':14,'name':'Text','flags':2},{'value':32,'name':'Display'}]},
      {'tag':'wght','name':'Weight','values':[{'value':w,'name':s,**({'flags':2,'linkedValue':700} if w==400 else {})} for w,s in STYLES.items()]}])
    f.save(ROOT/'fonts/variable/StreamDekSans-Variable.ttf');f.flavor='woff2';f.save(ROOT/'fonts/variable/StreamDekSans-Variable.woff2');f.flavor=None
    for w,s in STYLES.items():
        print('Building',s,flush=True)
        t=instantiateVariableFont(f,{'wght':w,'opsz':14},inplace=False);names(t,s,w)
        t.save(ROOT/'fonts/ttf'/f'StreamDekSans-{s}.ttf')
        make_otf(t,ROOT/'fonts/otf'/f'StreamDekSans-{s}.otf')
        t.flavor='woff2';t.save(ROOT/'fonts/woff2'/f'StreamDekSans-{s}.woff2')
    for w,s in [(400,'Regular'),(500,'Medium'),(600,'SemiBold'),(700,'Bold')]:
        d=instantiateVariableFont(f,{'wght':w,'opsz':32},inplace=False);names(d,'Display'+s,w)
        d['name'].setName(FAMILY+' Display',16,3,1,0x409);d['name'].setName(FAMILY+' Display',16,1,0,0)
        d.save(ROOT/'fonts/display'/f'StreamDekSans-Display{s}.ttf')
    report={'source':'Inter 4.1','source_url':'https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'license':'SIL Open Font License 1.1','modified_points':change,'cmap_count':len(f.getBestCmap()),'glyph_count':f['maxp'].numGlyphs,'widths':'unchanged','axes':[{'tag':a.axisTag,'min':a.minValue,'default':a.defaultValue,'max':a.maxValue} for a in f['fvar'].axes]}
    (ROOT/'qa/provenance.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('DONE',len(f.getBestCmap()),'mapped characters',flush=True)
if __name__=='__main__':main()
