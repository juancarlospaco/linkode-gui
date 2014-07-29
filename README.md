linkode-gui
===========

- linkode.org desktop client.
- Python 3 Qt 5, single-file, no dependencies, easy use,  GPLv3+ Licences.
- Google Docs like Auto-Save, 100% automatic *(still has a button on full UX mode)* .
- .editorconfig support *( http://editorconfig.org/#overview )*.
- .color support *(Uses Ninja-IDE Editor Themes http://ninja-ide.org/schemes )*.
- Code autocomplete, Syntax highlighting, Code Fold, Indentation Guides, Line Number, Line Markers.
- Undo, Redo, Cut, Copy, Paste, Zoom-In, Zoom-Out, Zoom-to, Zoom-Reset, file open, file save.
- UPPER case, lower case, Title case, Capitalize case, RaNdOm case.
- Window sizes and positioning adjustment helper.
- 2 UX modes, Simple *(ala Elementary)* or Full *(ala KDE)*


![screenshot](https://raw.githubusercontent.com/juancarlospaco/linkode-gui/master/temp.jpg)


# Try it !:

```
wget -O - https://raw.githubusercontent.com/juancarlospaco/linkode-gui/master/linkode-gui.py | python3
```


# Install permanently on the system:

```
sudo apt-get install python3-pyqt5  # OR  sudo yum install python3-qt5  OR  sudo pacman -S python-pyqt5
sudo wget -O /usr/bin/linkode-gui https://raw.githubusercontent.com/juancarlospaco/linkode-gui/master/linkode-gui.py
sudo chmod +x /usr/bin/linkode-gui
linkode-gui
```


# Requisites:

- [Python 3.x](https://www.python.org "Python Homepage")
- [PyQt 5.x](http://www.riverbankcomputing.co.uk/software/pyqt/download5 "PyQt5 Homepage")


# Why a Client ?:

- No graphical client, theres a command line only Linux only tool with no Clipboard integration.
- Need something like [Gisto](http://www.gistoapp.com "Gisto App for Gists") but instead of NodeJS to use Python3, because its better.
- NodeJS starts a Chromium everytime you do a pastebin *(>350Mb RAM)*, JS is slow *(GUI spinners)*
- Linkode Web editor was ~300px tall, no Clipboard integration, lacks features of this client.
- No root needed to install, compilable to Binary with [Nuitka](http://nuitka.net "Nuitka Python3 to Binary translator"), finally because I can :octocat:


Donate:
-------

- If you want to Donate please [click here](http://www.icrc.org/eng/donations/index.jsp) or [click here](http://www.atheistalliance.org/support-aai/donate) or [click here](http://www.msf.org/donate) or [click here](http://richarddawkins.net/) or [click here](http://www.supportunicef.org/)
