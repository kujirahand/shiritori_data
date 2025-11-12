# Makefile
# Usage:
#   make all
#   make clean
.PHONY: all clean

all:
	python3 1-data2src.py
	python3 2-make.py
	python3 3-kudb.py
	sh 4-make_archive.sh

clean:
	rm -f out.zip shiritori.db shiritori.db.zip

