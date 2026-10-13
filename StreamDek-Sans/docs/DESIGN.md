# Design specification

## Evidence from StreamDek

The read-only study used the canonical `C:/Dev/StreamDekMobile` checkout:

- `android/app/src/main/res/drawable-nodpi/streamdek_logo_transparent.png`:
  rounded-square enclosure, softened triangular play aperture, tapering swept
  curves and a cyan-to-blue gradient.
- `android/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml`: adaptive-icon
  composition and separate foreground/monochrome treatment.
- `ThemePalette.kt`: neutral default, dark ink `#0B0B0F`, surfaces `#111111` and
  `#1D1D1D`, foreground `#F5F7FB`; light background `#F5F4F0`; restrained accent
  colours such as Aurora `#34CEDA`.
- `StreamDekNativeApp.kt`: rounded navigation selection, circles, rounded cards
  and Material rounded controls. `ThemePicker.kt` uses a rounded PlayArrow.
- Main UI text uses Material theme typography. No dedicated custom UI font
  family was found in this read-only scan; explicit monospace use is confined to
  the inspected markdown renderer. This is a bounded source observation, not a
  runtime font-resolution audit of every screen or every StreamDek client.
- Eight string-resource locales: English, German, Spanish, French, Italian,
  Dutch, Polish and Portuguese.

The font echoes the enclosure's steady curves and the play cutout's controlled
corners. The logo's sweeping marks inspire the open c/e/s terminals and g tail;
they are not pasted into glyph outlines. Neutral specimens keep content primary.

## Outline design

New coordinates define the entire family. No reference font is read by
`build.py`. Latin forms have broad counters, restrained stroke contrast, a
double-storey a and single-storey descending g. The e has a level crossbar and
open lower-right aperture. Curves use authored cubic skeletons, sampled and
expanded into filled outlines with gently rounded shoulders. These are real
font contours, not a CSS stroke or synthetic bold.

I has short horizontal bars; l has a curved foot; 1 has an angled flag and base.
O is broad and open; 0 is narrower with a centre dot. The optional `zero`
feature substitutes a slash for the dot. The large x-height serves compact labels.

## Metrics and weights

| Property | Value |
|---|---|
| Units per em | 1000 |
| Nominal cap / x-height | 700 / 520 |
| Typographic & hhea ascent / descent | 1100 / −300 |
| Line gap | 0 |
| Width | Normal, proportional letters |
| Numerals | Lining, 600-unit tabular by default |
| Space | 285 units |
| Weight axis | 300–800, default 400 |
| Main stroke per master | 48, 66, 82, 98, 114, 130 units |

The generous line metrics protect stacked Latin accents and descenders. They
will produce a taller default line box than some platform UI fonts; future
integration should explicitly set and test line height. Round shapes have
optical overshoot. Ascender and descender construction follows the glyph's
parametric scale; it is not an optical-size axis.

All six authored masters participate in the variable font. Weight changes modify
stroke construction and counter size while preserving advance widths. Static
outlines have overlaps removed; compatible source/variable contours retain
overlaps with the TrueType overlap flag. Source geometry is polygonal after
curve sampling, with gentle corner rounding. The editable generator is the
authoritative source, supported by TTF masters and a designspace file.

## Spacing and features

Optical sidebearings are encoded per letter width. Class kerning covers 21 key
pair classes, including accent derivatives: AV/AW/AY, Ta/To, YA/Yo, LT/LY,
punctuation after P/r/v and round-to-diagonal combinations. Kerning is deliberately
moderate for interface text. This is a useful initial kerning set, not an
exhaustive foundry-level multilingual kerning audit.

- `kern`: class-based pair adjustments.
- `mark`, `mkmk`: top/bottom mark attachment and stacked marks.
- `tnum`: tabular figures (also the default).
- `pnum`: proportional figure alternates, especially narrower 1.
- `zero`: slashed zero alternative.

No italic, optical-size axis, small caps or arbitrary fraction substitution is
claimed. Precomposed ¼ ½ ¾ and several superscripts are supplied.

## Rendering and intended roles

Modern antialiased rasterization is the current rendering strategy. TrueType
`gasp` settings allow grayscale/symmetric smoothing. There are no hand-tuned
TrueType bytecode instructions; CFF files are also unhinted. A `gasp` table is
not a substitute for device testing. Inspect thin diagonals at low pixel sizes.

Starting points for review: Regular 16–20 px body; Medium 14–16 px labels;
SemiBold 20–32 px section titles; Light for large display text only; Bold and
ExtraBold for short headings. On a 1080p TV proof, labels are 28–36 px and the
display title is 96 px. These are specimen settings, not tested accessibility
guarantees. Avoid 300 for tiny labels and long descriptions.

## Reference boundary

Google Sans is shown at equal pixel size, without modifying its outlines. It is
not a build input. Reference: https://github.com/googlefonts/googlesans and the
bundled OFL file. SF Pro Rounded's rounded-system direction was consulted via
Apple's official overview: https://developer.apple.com/fonts/ . Apple's published
license limits non-Apple mockup use, so no Apple font file or rendered comparison
is included. The interactive specimen links to the official reference instead.
