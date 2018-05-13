@echo off

set git="C:\Program Files\Git\bin\git.exe"

cd ..
%git% archive --format=zip --output=./compile/tmp.zip HEAD
cd compile

mkdir tmp
unzip -d ./tmp/ ./tmp.zip
del /Q tmp.zip

for %%f in (..\dat\*.exe) do copy %%f tmp\dat
for %%f in (..\binfont\*.exe) do copy %%f tmp\binfont
for %%f in (..\lang\*.exe) do copy %%f tmp\lang
for %%f in (..\general\*.exe) do copy %%f tmp\general

set d=%date:/=%
set t=%time: =0%
set t=%t:~0,5%
set t=%t::=%
cd tmp
..\zip -9 -r ..\frostpunk_mod_%d%_%t%.zip *.*
cd ..

rd /S /Q tmp
