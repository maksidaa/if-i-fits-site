# Website language work

Updated November 7, 2026.

Spanish, Brazilian Portuguese, Japanese, Korean and Simplified Chinese versions of the home, support and privacy pages are prepared. Language links connect each page to its equivalents. They work without JavaScript.

This is a language-only change. Existing English content, figures, dates, screenshot images and layout remain the source. This includes the existing “coming soon” and seven-cat wording: Claude owns any factual or release-copy corrections. The update folders under `ota/` are untouched. Nothing here has been deployed.

The English pages at the root are the source. `locales/` holds their translations. Run `python3 scripts/build-locales.py` after changing a translation, then `python3 scripts/check-locales.py`. The build stops if an English phrase has no translation. The checks cover every page's language, language links, local files and preservation of the original English content. Rebuilding does not publish the site.

The game's matching language change is in `maksidaa/if-i-fits`. Publish the support pages alongside the approved language release so its localized support URLs resolve. Before publishing, review the translations with native speakers and follow the project's existing website approval gate.

For Wally: five website translations are ready for review, with English retained. The content and layout were preserved. Claude should handle the next release's factual copy and coordinate deployment; no live site or game update was made here.
