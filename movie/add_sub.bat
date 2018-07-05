@echo off

rem ffmpeg.exe -i intro_wide.ogv -vf "subtitles=intro_wide.ja.vtt:fontsdir=./:force_style='Fontsize=24,FontName=源真ゴシック Medium'" -vcodec hevc_nvenc -b:v 18138k -acodec copy intro_wide_ja.mp4
ffmpeg.exe -i intro_wide.ogv -vf "subtitles=intro_wide.ja.vtt:fontsdir=./:force_style='Fontsize=24,FontName=源真ゴシック Medium'" -vcodec theora -b:v 19400k -acodec copy intro_wide_ja.ogv
