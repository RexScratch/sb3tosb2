PREFIX = /usr/local

.PHONY: install

install: $(PREFIX)/bin/sb3tosb2

uninstall:
	rm -f $(PREFIX)/bin/sb3tosb2

$(PREFIX)/bin/sb3tosb2: sb3tosb2.py
	echo "#!/usr/bin/env python3" > $@
	cat $< >> $@
	chmod +x $@
