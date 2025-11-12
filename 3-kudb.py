#!/usr/bin/env python
from glob import glob
import kudb

kudb.connect("shiritori.db")
kudb.clear_doc()
i = 0
files = glob('out/*.csv')
for file in files:
    print("=== Processing", file)
    data = []
    with open(file, 'r', encoding="utf-8") as f:
        content = f.read()
        lines = content.splitlines()
        for line in lines:
            parts = line.split('\t')
            if len(parts) != 3:
                continue
            title = parts[0].strip()
            yomi = parts[1].strip()
            source = parts[2].strip()
            data.append({
                'title': title,
                'yomi': yomi,
                'k': source,
            })
            i += 1
            if i % 10000 == 0:
                print(f"  Processed {i} entries...", title, yomi, source)
    kudb.insert_many(data, tag_name="title")
kudb.close()
