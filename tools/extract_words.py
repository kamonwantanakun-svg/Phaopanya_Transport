# -*- coding: utf-8 -*-
"""Step 1 - read the AppSheet documentation PDF into a word/box table.

The PDF is a browser print of an HTML attribute dump.  Poppler's
`-bbox-layout` output gives every word with its position on the page, which is
all the parser needs to recover the (label cell, value cell) structure.

    pdftotext -bbox-layout "Application Documentation.PDF" bbox.xhtml
    python3 extract_words.py bbox.xhtml words3.json
"""
import json, sys
from lxml import etree

NS = {'h': 'http://www.w3.org/1999/xhtml'}


def main(src, dst):
    tree = etree.parse(src)
    pages = tree.getroot().findall('.//h:page', NS)
    out = []
    for p in pages:
        blocks = []
        for b in p.findall('h:flow/h:block', NS):
            lines = []
            for ln in b.findall('h:line', NS):
                words = [[round(float(w.get('xMin')), 1),
                          round(float(w.get('xMax')), 1),
                          round(float(w.get('yMin')), 1),
                          round(float(w.get('yMax')), 1),
                          (w.text or '')]
                         for w in ln.findall('h:word', NS)]
                lines.append(words)
            blocks.append(lines)
        out.append(blocks)
    with open(dst, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False)
    print('pages', len(out), '->', dst)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
