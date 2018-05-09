@echo off

set pyi="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Scripts\pyinstaller.exe"

for %%f in (..\binfont\*.py) do %pyi% --onefile %%f
mkdir tmp\binfont
copy dist\*.exe tmp\binfont
rd /S /Q ..\binfont\__pycache__
rd /S /Q build
rd /S /Q dist
del /Q *.spec

for %%f in (..\lang\*.py) do %pyi% --onefile %%f
mkdir tmp\lang
copy dist\*.exe tmp\lang
rd /S /Q ..\lang\__pycache__
rd /S /Q build
rd /S /Q dist
del /Q *.spec

set d=%date:/=%
set t=%time:~0,5%
set t=%t::=%
cd tmp
..\zip -9 -r ..\frostpunk_mod_exe_%d%_%t%.zip *.*
cd ..

rd /S /Q tmp
