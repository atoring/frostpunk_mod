@echo off

set pyi="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Scripts\pyinstaller.exe"

mkdir tmp
copy ..\README.md tmp
mkdir tmp\binfont
xcopy /E ..\binfont tmp\binfont
mkdir tmp\lang
xcopy /E ..\lang tmp\lang
cd tmp
del /S /Q *.bat
del /S /Q *.csv
del /S /Q *.dat
del /S /Q *.exe
del /S /Q *.lang
cd ..
copy ..\binfont\data\make_font.bat tmp\binfont\data

for %%f in (..\binfont\*.py) do %pyi% --onefile %%f
copy dist\*.exe tmp\binfont
rd /S /Q ..\binfont\__pycache__
rd /S /Q build
rd /S /Q dist
del /Q *.spec

for %%f in (..\lang\*.py) do %pyi% --onefile %%f
copy dist\*.exe tmp\lang
rd /S /Q ..\lang\__pycache__
rd /S /Q build
rd /S /Q dist
del /Q *.spec

set d=%date:/=%
set t=%time:~0,5%
set t=%t::=%
cd tmp
..\zip -9 -r ..\frostpunk_mod_%d%_%t%.zip *.*
cd ..

rd /S /Q tmp
