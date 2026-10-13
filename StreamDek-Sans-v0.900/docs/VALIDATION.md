# Validation record

Build 0.900, 11 October 2026. Technical tests: **PASS**. Design status: **review
candidate**, with device and human-review gates still open.

## Completed checks

- All 20 deliverable files parsed, all tables decompiled and recompiled with
  fontTools. TTF has real TrueType outlines; OTF has real CFF charstrings;
  WOFF2 is compressed font data, not a renamed file.
- Every file has the same 577-character mapping and 589 glyphs. Printable ASCII,
  Latin-1 and Latin Extended-A are complete. No missing characters were found
  in the eight current Mobile locale resource files.
- Typographic family is StreamDek Sans. Style/weight values, embedding flags,
  fixed vertical metrics and PostScript names were checked. The package uses
  legacy RIBBI style groups for old Windows font menus.
- HarfBuzz checks passed for kerning (AVATAR), tabular digits, proportional
  digits, optional slashed zero, combining-mark attachment and NFC/NFD sample
  equivalence. All tested samples shaped without a .notdef glyph.
- Every glyph's bounds were checked against ascent 1100 / descent −300.
- All static TTF/OTF files were rasterized through Pillow/FreeType at 12, 16,
  24 and 48 px. The full specimen set includes native-pixel 12–32 px proofs,
  large display headings, light/dark backgrounds and a 1920×1080 TV composition.
- Variable axis is wght 300–800, default 400, with six named styles. Eleven
  weights at 50-unit intervals instantiated and rasterized. All glyph coordinates
  at each of the six master locations matched the authored masters within
  one font unit.
- All 20 files loaded through the browser FontFace API in Windows Microsoft
  Edge 155.0.4283.45. No browser font/JavaScript errors were reported.
  The interactive specimen's text, 725 weight, 36 px size, zero option and
  light/dark control were exercised. A 390 px viewport had no horizontal overflow.
- Main specimen layouts and glyph-sheet contact proofs were visually reviewed
  during development. This is not an exhaustive typographer's review of every
  glyph at every weight, size and language combination.

Raw results: `qa/validation.json` and `qa/browser-validation.json`. Browser
screenshots: `qa/edge-desktop.png` and `qa/edge-mobile.png`. File hashes appear
in the validation record and SHA256SUMS.txt.

## Open release gates

1. Review letterforms and spacing with the StreamDek owner; follow with a
   native-reader and professional type-design review for final optical polish.
2. Inspect the 1080p proof on target TV hardware at actual viewing distance.
   No physical TV-distance readability test has been performed.
3. Validate on target Android rasterizers, Firefox and Safari/CoreText, desktop
   font menus, accessibility text scaling and real fallback text. Chromium and
   FreeType acceptance do not establish identical cross-platform rendering.
4. Review 12–14 px text carefully. The family has no TrueType bytecode hinting;
   small Light text and very fine details are intentionally not approved for
   tiny labels. Modern antialiasing and gasp flags are the current approach.
5. Finalize the recipient's distribution notice and naming/trademark clearance.
   Original build provenance is documented; global legal uniqueness is not
   certified by outline generation or technical testing.

No Android/TV application installation, UI integration, font-manager
installation, publication or source-repository change was performed.

## Files

| File | Bytes | Glyphs |
|---|---:|---:|
| fonts\otf\StreamDekSans-Bold.otf | 337,104 | 589 |
| fonts\otf\StreamDekSans-ExtraBold.otf | 327,992 | 589 |
| fonts\otf\StreamDekSans-Light.otf | 353,684 | 589 |
| fonts\otf\StreamDekSans-Medium.otf | 345,316 | 589 |
| fonts\otf\StreamDekSans-Regular.otf | 349,988 | 589 |
| fonts\otf\StreamDekSans-SemiBold.otf | 338,656 | 589 |
| fonts\ttf\StreamDekSans-Bold.ttf | 388,880 | 589 |
| fonts\ttf\StreamDekSans-ExtraBold.ttf | 380,612 | 589 |
| fonts\ttf\StreamDekSans-Light.ttf | 403,488 | 589 |
| fonts\ttf\StreamDekSans-Medium.ttf | 396,808 | 589 |
| fonts\ttf\StreamDekSans-Regular.ttf | 400,804 | 589 |
| fonts\ttf\StreamDekSans-SemiBold.ttf | 390,024 | 589 |
| fonts\variable\StreamDekSans-Variable.ttf | 2,582,620 | 589 |
| fonts\variable\StreamDekSans-Variable.woff2 | 255,796 | 589 |
| fonts\woff2\StreamDekSans-Bold.woff2 | 40,472 | 589 |
| fonts\woff2\StreamDekSans-ExtraBold.woff2 | 40,804 | 589 |
| fonts\woff2\StreamDekSans-Light.woff2 | 39,508 | 589 |
| fonts\woff2\StreamDekSans-Medium.woff2 | 40,008 | 589 |
| fonts\woff2\StreamDekSans-Regular.woff2 | 39,276 | 589 |
| fonts\woff2\StreamDekSans-SemiBold.woff2 | 40,132 | 589 |
