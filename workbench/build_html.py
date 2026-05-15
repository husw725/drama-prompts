#!/usr/bin/env python3
"""Build self-contained HTML workbench from project_data.json.

Strategy: Split JSON into ~30KB chunks, each stored in a separate
<script type="application/json" class="__data_chunk__"> tag.
JS collects all chunks, concatenates, and JSON.parse's the result.
This avoids the browser limit on single large inline data blocks.
"""

import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE, 'template.html')
DATA_PATH = os.path.join(BASE, 'project_data.json')
OUT_PATH = os.path.join(BASE, 'index.html')

CHUNK_SIZE = 30000  # ~30KB per chunk

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

if not isinstance(data.get('episodes'), list) or not len(data['episodes']):
    print("[ERROR] project_data.json: missing or empty 'episodes' array", file=sys.stderr)
    sys.exit(1)

json_str = json.dumps(data, ensure_ascii=False)
print("[INFO] project_data.json: %.0fKB, %d episodes" % (len(json_str)/1024, len(data['episodes'])))

# Split JSON string into chunks
chunks = []
for i in range(0, len(json_str), CHUNK_SIZE):
    chunks.append(json_str[i:i+CHUNK_SIZE])

# Build chunk script tags
chunk_tags = []
for idx, chunk in enumerate(chunks):
    # Escape </script> sequences inside the JSON (rare but possible)
    safe_chunk = chunk.replace('</script>', '<\\/script>')
    tag = '<script type="application/json" class="__data_chunk__" id="__chunk_%d__">%s</script>' % (idx, safe_chunk)
    chunk_tags.append(tag)

chunk_html = '\n'.join(chunk_tags)
print("[INFO] Split into %d chunks (~%dKB each)" % (len(chunks), CHUNK_SIZE//1024))

# Read template
with open(TEMPLATE, 'r', encoding='utf-8') as f:
    template = f.read()

# Inject chunks into placeholder
placeholder = '<!--DATA_CHUNKS-->'
if placeholder not in template:
    print("[ERROR] Placeholder <!--DATA_CHUNKS--> not found in template.html!", file=sys.stderr)
    sys.exit(1)

html = template.replace(placeholder, chunk_html)

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("[OK] Generated %s (%.0fKB) with %d data chunks" % (
    OUT_PATH, len(html)/1024, len(chunks)))
print("    Works with file:// (double-click) and http:// (server)")
