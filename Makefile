
FLAGS = --noconfirm --onefile --windowed
ICON = --icon "icon.ico" --add-data "F:\Assignment\PyMath\icon.ico;."
IMGPATHS = --add-data  "*.png;."
NAME = main
EXCLUDE = --exclude-module scipy.stats.distributions
HOOKS = --additional-hooks-dir=hooks

compile:
	pyinstaller $(FLAGS) $(ICON) $(IMGPATHS) main.py

clean:
	rm -r build main.spec dist