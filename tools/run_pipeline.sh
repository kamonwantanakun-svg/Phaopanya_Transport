#!/usr/bin/env bash
# Rebuild every artefact in this repository from the source PDF.
#
#   ./run_pipeline.sh "/path/to/Application Documentation.PDF" [outdir]
set -euo pipefail
PDF="${1:?usage: run_pipeline.sh <pdf> [outdir]}"
OUT="${2:-.}"
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "== 1/4  pdf -> word boxes =="
pdftotext -bbox-layout "$PDF" "$WORK/bbox.xhtml"
python3 "$HERE/extract_words.py" "$WORK/bbox.xhtml" "$WORK/words3.json"

echo "== 2/4  word boxes -> records =="
(cd "$HERE" && python3 - "$WORK/words3.json" "$WORK/records.json" <<'PY'
import json, sys
sys.path.insert(0, '.')
import appsheet_parse
W = json.load(open(sys.argv[1], encoding='utf-8'))
recs, stats = appsheet_parse.parse(W)
json.dump(recs, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('records', len(recs), dict(stats))
PY
)

echo "== 3/4  verify (round-trip against the PDF) =="
(cd "$HERE" && python3 verify_roundtrip.py "$WORK/words3.json")

echo "== 4/4  records -> repository =="
python3 "$HERE/build_repo.py" "$WORK/records.json" "$OUT"
echo "done -> $OUT"
