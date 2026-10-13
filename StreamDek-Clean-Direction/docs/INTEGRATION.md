# Future integration guide

No app files have been changed. Use the package for review before integrating.

## Web

```css
@font-face {
  font-family: 'StreamDek Sans';
  src: url('/fonts/StreamDekSans-Variable.woff2') format('woff2');
  font-weight: 300 800;
  font-style: normal;
  font-display: swap;
}
body {
  font-family: 'StreamDek Sans', system-ui, sans-serif;
  font-optical-sizing: auto;
  font-synthesis: none;
}
.timecode { font-variant-numeric: tabular-nums; }
```

Avoid global negative tracking for body text. Use Regular for paragraphs, Medium for controls and SemiBold for headings as starting points. Keep fallback fonts for scripts outside the family's coverage. No italic styles were produced.

## Android and TV

For a straightforward first review, explicitly map the six text TTFs to weights 300–800 in the application's font family configuration. Use text optics for ordinary labels and subtitles; trial display optics for large titles only. Do not apply synthetic bold. Use `tnum` for counters/timecodes requiring stable numeral widths.

The variable TTF offers `wght` and `opsz`, but the application's font API must explicitly support and select variation axes. Do not assume automatic optical-size selection on Android merely because the font contains the axis. The supplementary display TTFs can be loaded directly by file as a separate title family.

Before rollout, review real screens at supported font scales, multiline wrapping, Polish/French/Portuguese accents, fallback scripts, dense metadata, playback timecodes and remote-focus states. Test physical TV viewing distance and platform rasterisation. The desktop proof images are not device validation.
