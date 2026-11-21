"""Pick programme photos from the Facebook export and write them into images/work/.

Input  (private, not in the repo): reference/facebook/posts.json, raw/p###-n.jpg and colorfulness.tsv
       (made with: swiftc source/colorfulness.swift -o reference/facebook/colorfulness;
        reference/facebook/colorfulness reference/facebook/raw/*.jpg > reference/facebook/colorfulness.tsv),
       collected from https://www.facebook.com/profile.php?id=61573232295835 (301 posts, Feb 2025 – Nov 2026).
Output: images/work/<event>-<n>.jpg (max 1000 px) and source/fb_work.json
        ({card date: {"photos": [...], "fb": [post indices]}}), which build_site.py reads.

    python3 source/import_facebook.py
"""
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FB = os.path.join(ROOT, 'reference', 'facebook')
OUT = os.path.join(ROOT, 'images', 'work')
MAX_PER_EVENT = 8
MAX_CLIPPINGS = 2      # newspaper scans per event, shown after the photos
CLIPPING_BELOW = 0.12  # mean saturation under this = newsprint/document (see colorfulness.swift)
# Never publish: quiz-result sheets with students' addresses and phone numbers.
EXCLUDE = {'p215-4.jpg', 'p293-0.jpg', 'p295-0.jpg', 'p051-4.jpg', 'p046-0.jpg', 'p002-0.jpg', 'p009-0.jpg', 'p077-0.jpg', 'p231-1.jpg', 'p278-1.jpg'}

# Card date (as shown on the Our Work cards) -> Facebook post indices, newest first.
EVENTS = {
    # 2026
    '2 Nov': [0, 3, 10, 11, 12, 13, 14],
    '18 Oct': [1, 16, 24, 27, 28, 29, 30, 31, 32],
    '17 Oct': [6, 25, 33, 34, 35, 36, 37, 38, 40],
    '12 Oct': [5, 39, 41, 42, 43, 44],
    '29 Sep': [4, 46, 48, 49, 50, 51],
    '26 Sep': [2, 47, 52, 53, 54, 55],
    '8 Aug': [56, 57, 58, 59, 60, 61],
    '18 Jul': [7, 62, 63, 64, 65, 67, 68, 69, 70],
    '11 Jul': [71, 72, 73, 74],
    '25 Jun': [8, 78, 79, 80, 81, 84, 86, 87, 88],
    '14 Jun': [82, 83, 85, 89, 90, 91, 92, 93, 94],
    '9 Feb': [9, 77, 104, 105, 106, 107, 108, 109, 110, 112, 113],
    # 2024–25
    '10 Dec 2025': [116, 117, 118, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 131, 132, 133, 134, 135, 138],
    '29 Nov 2025': [139, 140, 142, 143],
    '18 Nov 2025': [144, 145, 146, 147, 149],
    '9 Nov 2025': [150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 164],
    '27 Oct 2025': [168, 169, 170, 171, 172],
    '15 Sep 2025': [174, 175, 176, 178, 179, 181, 182, 183, 184],
    '16 Aug 2025': [187, 188, 189, 190, 191, 192, 193, 194, 195, 196],
    '12 Jul 2025': [201, 202, 203, 205, 206, 207, 208],
    '28 Jun 2025': [209, 210, 211, 212],
    '7 Jun 2025': [213, 214, 215, 216, 217, 218, 219],
    '12 May 2025': [220, 221, 225, 226],
    '10 May 2025': [222, 223, 224, 227, 228, 229, 230, 231],
    '2 May 2025': [233, 234, 235, 236, 237],
    '19 Apr 2025': [247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264],
    '8 Mar 2025': [269, 270, 271, 272, 273, 274, 275, 276, 277, 278],
    '22 Feb 2025': [281, 282, 283, 293, 298],
    '28 Jan 2025': [295, 299],
    '10 Dec 2024': [284, 285, 286, 287, 288, 289, 290, 291, 292, 294, 296, 297],
}


def slug(date):
    return re.sub(r'[^a-z0-9]+', '-', date.lower()).strip('-')


def main():
    posts = json.load(open(os.path.join(FB, 'posts.json'), encoding='utf-8'))
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
    colour = {}
    for line in open(os.path.join(FB, 'colorfulness.tsv'), encoding='utf-8'):
        v, path = line.rstrip('\n').split('\t')
        colour[os.path.basename(path)] = float(v)
    result = {}
    for date, idxs in EVENTS.items():
        photos, videos, clippings, seen = [], [], [], set()
        # Photo posts with the most pictures first (albums are the richest), then video stills.
        for i in sorted(idxs, key=lambda i: -(len(posts[i]['imgs']) + int(posts[i]['more'] or 0) * 0.1)):
            for n, url in enumerate(posts[i]['imgs']):
                img_id = re.search(r'/(\d+)_', url)
                key = img_id.group(1) if img_id else url
                if key in seen:
                    continue
                seen.add(key)
                fname = f'p{i:03d}-{n}.jpg'
                src = os.path.join(FB, 'raw', fname)
                if fname in EXCLUDE or not os.path.exists(src) or os.path.getsize(src) < 5000:
                    continue
                if colour.get(fname, 1) < CLIPPING_BELOW:
                    clippings.append(src)
                else:
                    (videos if 't15.' in url else photos).append(src)
        chosen = (photos + videos)[:MAX_PER_EVENT - min(MAX_CLIPPINGS, len(clippings))] + clippings[:MAX_CLIPPINGS]
        chosen = chosen[:MAX_PER_EVENT]
        names = []
        for k, src in enumerate(chosen, 1):
            name = f'{slug(date)}-{k}.jpg'
            subprocess.run(['sips', '-Z', '1000', '-s', 'format', 'jpeg', '-s', 'formatOptions', '55',
                            src, '--out', os.path.join(OUT, name)], check=True, capture_output=True)
            names.append('images/work/' + name)
        result[date] = {'photos': names, 'clippings': [n for n, src in zip(names, chosen) if src in clippings],
                        'src': [os.path.basename(c) for c in chosen], 'fb': idxs}
        print(f'{date:12s} {len(photos):3d} photos {len(videos):3d} stills {len(clippings):3d} clippings -> {len(names)}')
    json.dump(result, open(os.path.join(HERE, 'fb_work.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
