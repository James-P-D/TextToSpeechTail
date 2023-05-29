# TextToSpeechTail
Console tail application with online/offline text-to-speech in Python

![Screenshot](https://github.com/James-P-D/TextToSpeechTail/blob/main/screenshot.png)

## Details

A 'tail' program is a small application which can be used to monitor a log file, and update the screen when new information is added to the file. In addition to displaying newly added lines, this application will all read them aloud to the user.

## Usage

```
C:\Dev\TextToSpeechTail\src\Text2SpeechTail>python Text2SpeechTail.py -h
usage: Text2SpeechTail.py [-h] [-i I] [-f] full_file_path

Tail with text-to-speech.

positional arguments:
  full_file_path

options:
  -h, --help      show this help message and exit
  -i I            line number to start from. Defaults to -1 for end-of-file
  -f              Offline text-to-speech
```

`full_file_path` specifies the path to the log file

`-i` specifies the line-number to start from. `0` for start of file, or leave blank or use `-1` for end of file.

`-f` for offline text-to-speech, which is slightly more robotic than the online version, but also slightly faster.

Example:

```
C:\Dev\TextToSpeechTail\src\Text2SpeechTail>python Text2SpeechTail.py test.txt
```