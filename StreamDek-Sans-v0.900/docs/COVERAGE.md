# Character and language coverage

577 mapped Unicode characters, 589 glyphs, identical across all weights and formats.

Complete printable ASCII U+0020–007E, Latin-1 Supplement U+00A0–00FF and Latin
Extended-A U+0100–017F are included. Also supplied: selected Latin Extended
Additional characters, 16 combining marks, smart quotes, dashes, ellipsis,
currency, arithmetic, arrows, common fractions, superscripts and control spaces.

Current app-string audit: all characters appearing in the eight inspected
Mobile `strings.xml` sets are mapped. This includes English, German, Spanish,
French, Italian, Dutch, Polish and Portuguese. It is a character audit, not a
linguistic or translation review. The exact resource inputs are identified in
`qa/validation.json` and DESIGN.md. Backend-supplied titles can contain other scripts.

Latin-1/Extended-A repertoire also provides the letters needed for several other
Western/Central European orthographies, but those languages have not received
native-reader review. Do not infer complete Vietnamese, IPA or pan-European
language support from selected additional glyphs. Greek, Cyrillic, Arabic,
Hebrew, Indic scripts, CJK and emoji require a platform fallback.

Combining marks: grave, acute, circumflex, tilde, macron, breve, dot above,
diaeresis, ring, double acute, caron, cedilla, ogonek, comma below, dot below,
hook above. Top/bottom attachment and stacking are supplied; NFC and NFD sample
equivalence is tested through HarfBuzz. Test unusual multi-mark combinations
before relying on them in production.

Exact mapped ranges:

U+0020–U+007E, U+00A0–U+017F, U+0192, U+0218–U+021B, U+02C7, U+02D8–U+02DB, U+02DD, U+0300–U+0304, U+0306–U+030C, U+0323, U+0326–U+0328, U+1E02–U+1E05, U+1E08–U+1E0D, U+1E10–U+1E11, U+1E14–U+1E17, U+1E1C–U+1E29, U+1E2E–U+1E33, U+1E36–U+1E39, U+1E3E–U+1E47, U+1E4C–U+1E5D, U+1E60–U+1E6D, U+1E78–U+1E93, U+1E97–U+1E99, U+1E9B, U+1E9E, U+1EA0–U+1ED9, U+1EE4–U+1EE7, U+1EF2–U+1EF9, U+2002–U+2003, U+2009, U+200B–U+200D, U+2013–U+2014, U+2018–U+201A, U+201C–U+201E, U+2020–U+2022, U+2026, U+202F–U+2030, U+2039–U+203A, U+2060, U+2070, U+2074–U+2079, U+20AC, U+2113, U+2117, U+2120, U+2122, U+2190–U+2193, U+2212, U+221A, U+221E, U+2260, U+2264–U+2265, U+FEFF

`qa/coverage.json` lists every code point, Unicode name and character. The seven
`specimens/glyphs-*.png` sheets show every mapping. Invisible spacing/control
characters naturally have no visible outline.
