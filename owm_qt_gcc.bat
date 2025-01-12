cd c:\temp

python -m nuitka ^
    --onefile ^
    --mingw64 ^
    --lto=no ^
    --enable-plugin=pyside6 ^
    --windows-console-mode=disable ^
    --windows-icon-from-ico=weather.ico ^
    --include-data-file=Darkeum.qss=Darkeum.qss ^
    owm_qt.py
pause

rem     --disable-ccache ^