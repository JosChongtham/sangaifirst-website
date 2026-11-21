# Sangai First Foundation — website handoff

Website for **Sangai First Foundation (SfF), Manipur**, a non-profit trust (Reg. no. 442 of 02/10/2025, Indian Trusts Act, 1882) working to protect the Sangai (brow-antlered deer) and Keibul Lamjao National Park.

Built in Claude's Design canvas; moved here to finish in Claude Code.

## What's in this folder

- `source/` — the five pages as Design-canvas files (`*.dc.html`): Home (`Main`), Discover, Our Work, About, Contact. They use a small Design runtime (`support.js`, `<x-dc>`, `{{holes}}`, `<sc-for>`, `<sc-if>`), so **they won't open as plain web pages**. `generate_pages.py` produced them: all copy, data and layout live there.
- `images/` — every image the site uses (upscaled brochure photos, founders cutouts, deer engraving).
- `reference/` — source documents: the 2024–25 brochure, the 2026 annual report (2 scanned pages), and the original founders photo.

## Static site (done)

`site/` is the finished static website: `index.html`, `discover.html`, `work.html`, `about.html`, `contact.html`, plus `assets/styles.css`, `assets/site.js` and `images/`. Upload the whole `site/` folder to any static host.

Don’t edit `site/` by hand. All copy, data and markup live in `source/build_site.py`; change it there and rebuild:

```
python3 source/build_site.py
```

Preview locally with `python3 -m http.server 8765 --directory site`. The Wikimedia Commons photos are in `images/` and credited in the Discover page footer.

## Suggested first task for Claude Code (original brief)

> Convert `source/generate_pages.py` / the `.dc.html` pages into a plain static website (HTML + CSS + a little vanilla JS for the carousels) in `site/`, with images from `images/`. Keep the design exactly: Apple HIG–style (system font, frosted-glass pill nav, light and dark mode via CSS variables, 44px tap targets, reduced-motion support), the carousels, and the newsprint founders card on About. Then download the Wikimedia Commons photos listed below into `images/`, place them as described, and add a credits line in the footer.

## Design decisions to keep

- Four light pages plus Contact; little text per page; information shown through carousels, a bar chart, stat tiles and symbol tiles.
- One accent colour (green `#008932` light / `#30D158` dark), used only for interactive things.
- Curly apostrophes and quotation marks only (’ ‘ “ ”).
- Founders card (About): retro newsprint clipping with torn edges, halftone/duotone cutout breaking out of the card. The headline and short text on the clipping were written for the site, not taken from a real newspaper.

## Photos still to add (all from Wikimedia Commons; credit required)

| Place | File | Credit · licence |
|---|---|---|
| Discover slide “Phumdi” | The_Phumdis_on_Loktak_Lake.jpg | Ishani Nath · CC BY-SA 4.0 |
| Discover slide “Keibul Lamjao” | Loktak_Lake_Manipur_02.jpg | ch_15march · CC BY 2.0 |
| “Loktak by the numbers” | Loktak_Lake_Manipur_01.jpg | ch_15march · CC BY 2.0 |
| Discover slide “Manipur” | Rasa_Lila_in_Manipuri_dance_style.jpg | Flickr · CC BY 2.0 |
| State Bird tile | Syrmaticus_humiae_104702127.jpg | Christoph Moning · CC BY 4.0 |
| State Flower tile | Shirui_Lily.jpg | Mashangva · CC BY-SA 4.0 |
| Comeback chart (optional) | Sangai_Brow-antlered_Deer_Rucervus_eldii_eldii_Manipur_by_Dr._Raju_Kasambe_(1).jpg | Raju Kasambe · CC BY-SA 4.0 |

Download at website size via `https://commons.wikimedia.org/wiki/Special:FilePath/<file>?width=1600`. Also worth a look: CC0 Sangai illustrations credited to Dr Khangembam Shamungou on Commons (search “Shamungou, Khangembam”).

## Open questions for the Foundation

1. **Contact details conflict.** The site uses the brochure's (sangaiff2024@gmail.com, +91 98561 77030, +91 80143 66698, Nambol Makha Leikai). The 2026 annual report lists sangaifirst2024@gmail.com, +91 84861 73030, +91 76290 66849. Facebook lists 087876 21316 and Ithing Sendra Chingkhong, Thanga Part-2, 795133. Confirm which is current.
2. **Name spelling:** “Shamungou” vs “Samungou” in sources; the site uses Dr Khangembam Shamungou.
3. Original, higher-resolution photos of the Foundation's own events (current ones are upscaled brochure scans).

## Key facts and sources used

- Sangai population: 6 (1953), 14 (1975), ~155 (1995), 260 (2016), **172 (2026 Forest Department census, with 375 hog deer)**. WII monitoring: 91 (2006), 76 (2019), 64 (2023). Sources: Wikipedia “Sangai”; Eastern Mirror, “Hog deer outnumber Sangai in Keibul Lamjao National Park” (July 2026); India Wildlife News (June 2026); Down To Earth, “Drowning in its home” (Dec 2025).
- Keibul Lamjao: ~40 km², sanctuary 1966, national park 1977, phumdi 0.3–1.22 m thick; Ithai Barrage (1983). Loktak: ~287 km², Ramsar site 23 March 1990, ~100,000 people in 55 hamlets. Sources: Wikipedia.
- Manipur: birthplace of modern polo (Sagol Kangjei) and Raas Lila (Manipur Tourism); state symbols (Wikipedia).
- Foundation history (annual report 2026): genesis meeting 24 Nov 2024 at Dr Shamungou's home, Nambol Makha Leikai (with Kumam Jugeshor, Salam Prasanta, Khwairakpam Budha); decided Sangai Day on 10 December (recalling the 1954 Manipur Board for Wildlife resolution, chaired by V.S. Sundram, for a 50 km² sanctuary) and founding of SfF. 1st Sangai Day 10 Dec 2024, Manipur Zoological Garden; 2nd 10 Dec 2025, Phouoibee Community Hall, Keibul Lamjao (1,054 students in 2025, 152 quiz winners). 2026: 586 students, 9 schools, 117 quiz winners, 268 in planting drives; Sangai Heritage Hub planned at Keibul Ching for 10 Dec 2026.
