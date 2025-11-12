#!/bin/sh

# outディレクトリを圧縮してout.zipを作成
rm -f out.zip
if [ -d "out" ]; then
    echo "Compressing out directory to out.zip..."
    zip -r out.zip out/
    echo "Archive created: out.zip"
else
    echo "Error: out directory not found"
    exit 1
fi

# shiritori.dbを圧縮してshiritori.db.zipを作成
rm -f shiritori.db.zip
if [ -f "shiritori.db" ]; then
    echo "Compressing shiritori.db to shiritori.db.zip..."
    zip shiritori.db.zip shiritori.db
    echo "Archive created: shiritori.db.zip"
else
    echo "Error: shiritori.db file not found"
    exit 1
fi

