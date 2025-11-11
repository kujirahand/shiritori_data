import kudb

kudb.connect("shiritori.db")

print(kudb.find(lambda r: r['title'] == "雷"))
print(kudb.find(lambda r: r['yomi'] == "カミナリ"))
print(kudb.find(lambda r: r['k'] == "カ" and len(r['yomi']) == 5, limit=3))
print(kudb.find(lambda r: r['yomi'].startswith("アナ") and len(r['yomi']) >= 4, limit=3))