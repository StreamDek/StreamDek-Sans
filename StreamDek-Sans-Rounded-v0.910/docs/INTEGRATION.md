# Future integration guide — documentation only

Nothing in this guide has been applied to StreamDek. Complete the device and
design reviews in VALIDATION.md before selecting this family for release.

## Android / Compose: six static weights

For the broadest compatibility, copy the six TTF files to `res/font/` under
lowercase resource names such as `streamdek_sans_rounded_regular.ttf`. Define:

```kotlin
val StreamDekSansRounded = FontFamily(
    Font(R.font.streamdek_sans_rounded_light, FontWeight.Light),
    Font(R.font.streamdek_sans_rounded_regular, FontWeight.Normal),
    Font(R.font.streamdek_sans_rounded_medium, FontWeight.Medium),
    Font(R.font.streamdek_sans_rounded_semibold, FontWeight.SemiBold),
    Font(R.font.streamdek_sans_rounded_bold, FontWeight.Bold),
    Font(R.font.streamdek_sans_rounded_extrabold, FontWeight.ExtraBold),
)

Text(
    text = "Continue Watching",
    fontFamily = StreamDekSansRounded,
    fontWeight = FontWeight.Medium,
    fontSize = 18.sp,
    lineHeight = 26.sp,
)
```

Use imports from `androidx.compose.ui.text.font`, `androidx.compose.material3.Text`
and `androidx.compose.ui.unit.sp`. Resources above are examples to create later.
Do not register only Regular and let the renderer synthesize all other weights.
Use tabular default digits for timestamps. `fontFeatureSettings = "'zero' 1"`
in a TextStyle enables the optional slashed zero. Test fallback for titles in
non-Latin scripts, emoji, combining marks, text scaling and existing truncation.

A variable TTF is supplied for a later variation-aware implementation. The
static mapping is the documented default here; an Android API compatibility
matrix for variable settings has not been validated in the applications.

Official font-family reference:
https://developer.android.com/develop/ui/compose/text/fonts

## Web: variable WOFF2

Copy the variable WOFF2 to the chosen public asset path, then adapt this example:

```css
@font-face {
  font-family: "StreamDek Sans Rounded";
  src: url("/fonts/StreamDekSansRounded-Variable.woff2") format("woff2");
  font-style: normal;
  font-weight: 300 800;
  font-display: swap;
}

body {
  font-family: "StreamDek Sans Rounded", system-ui, sans-serif;
  font-synthesis: none;
  font-weight: 400;
  line-height: 1.5;
}
.navigation { font-weight: 500; }
.heading { font-weight: 600; }
.timestamp { font-variant-numeric: tabular-nums; }
.technical-id { font-feature-settings: "zero" 1; }
```

For static delivery, declare six `@font-face` entries with the same family name,
the individual WOFF2 URLs, and weights 300, 400, 500, 600, 700 and 800. Choose
either variable or static delivery per page to avoid ambiguous face matching.
Serve WOFF2 as `font/woff2`, permit the relevant origin if using a CDN, and
measure layout shift after swap. Preload only if the page's loading strategy
benefits from it; this artifact does not change deployment configuration.

The default figures are tabular, while `font-variant-numeric: proportional-nums`
selects proportional alternates. Do not claim italic support; no italic is shipped.

## Desktop / design tools

Choose the six static TTFs, six CFF OTFs, or one variable TTF. Install only one
edition at a time. Canonical typographic family (name ID 16) is `StreamDek Sans Rounded`.
Legacy IDs 1/2 use Windows-compatible style groups so non-Regular/Bold weights
remain individually selectable in older applications. Modern menus use IDs 16/17.
Remove an older build before installing an updated one and restart the design
tool if it caches fonts. Installation has not been performed by this task.
