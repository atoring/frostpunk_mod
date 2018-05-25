@echo off

set git="C:\Program Files\Git\bin\git.exe"
set bin=frostpunk_mod

%git% show --format=%%cd --date=format:%%Y%%m%%d_%%H%%M -s>tmp
set /p dt=<tmp
del /Q tmp

mkdir tmp
copy %bin%.exe tmp
copy ..\README.md tmp
copy ..\LICENSE tmp
xcopy ..\frostpunk_mod\sysdic tmp\sysdic /I
mkdir tmp\data
copy ..\frostpunk_mod\data\notosanscjksc-medium.otf.binfont.zip tmp\data
cd tmp
..\zip -9 -r ..\frostpunk_mod_%dt%.zip *.*
cd ..
rd /S /Q tmp
