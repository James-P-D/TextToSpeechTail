from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
from playsound import playsound  # pip install playsound==1.2.2
import os
import argparse
from pathlib import Path

class FileModifiedHandler(FileSystemEventHandler):
    _TEMP_FILE_NAME = 'temp.mp3'

    def __init__(self, path, file_name, line_index, offline):
        self.path = path
        self.file_name = file_name
        self.line_index = line_index
        self.offline = offline
        if self.line_index == -1:
            # If we're told to start reciting from line -1, read the whole file, but don't
            # play. This will simply seek to the end of the file and set line_index to 
            # the bottom.
            self.read_from_file()            
        else:
            # ...otherwise set the line_index to whatever position requested, and
            # play from there
            self.line_index = line_index - 1
            self.play(self.read_from_file())

        self.observer = Observer()
        self.observer.schedule(self, path, recursive=False)
        self.observer.start()
        self.observer.join()

    def read_from_file(self):
        import os
        lines = None
        if os.name == 'nt':
            import msvcrt
            import win32file
            # On Windows, open(file_name "r") annoyingly locks the file unnecessary
            # which would prevent other processes from loggin to it. Instead, we
            # have to use win32file.CreateFile() with an excessive number of args
            py_handle = win32file.CreateFile(
                os.path.join(self.path, self.file_name),
                win32file.GENERIC_READ,
                win32file.FILE_SHARE_DELETE | win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
                None,
                win32file.OPEN_EXISTING,
                win32file.FILE_ATTRIBUTE_NORMAL,
                None)

            with os.fdopen(msvcrt.open_osfhandle(py_handle.handle, os.O_RDONLY)) as file_descriptor:
                lines = file_descriptor.readlines()
        else:
            with open(self.file_name, "r") as file:
                lines = [line.rstrip() for line in file.readlines()]

        # If there are fewer lines in the file than line_index, then log file has
        # been reset, so seek back to the first line by setting line_index to zero
        if (self.line_index != -1) and (len(lines) < self.line_index):
            self.line_index = 0

        # Get only the lines we haven't recited yet
        new_lines = lines[self.line_index:]
        self.line_index = len(lines)
        all_lines = "".join(new_lines)
        return all_lines

    def play(self, all_lines):
        if len(all_lines) > 0:
            print(all_lines)
            if self.offline:
                try:
                    import pyttsx3
                    engine = pyttsx3.init()
                    engine.say(all_lines)
                    engine.runAndWait()
                except:
                    print("Error using pyttsx3")
            else:
                try:
                    import gtts
                    tts = gtts.gTTS(all_lines)
                    tts.save(self._TEMP_FILE_NAME)
                    playsound(self._TEMP_FILE_NAME)
                    os.remove(self._TEMP_FILE_NAME)
                except:
                    print("Error using gtts")

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(self.file_name):
            self.play(self.read_from_file())

def main():
    parser = argparse.ArgumentParser(description='Tail with text-to-speech.')
    parser.add_argument('full_file_path')
    parser.add_argument('-i',
                        default=-1,
                        type=int,
                        help="line number to start from. Defaults to -1 for end-of-file")
    parser.add_argument('-f',
                        action='store_true',
                        help="Offline text-to-speech")
    args = parser.parse_args()

    if (not os.path.isfile(args.full_file_path)):
        print(f"Unable to find file: {args.full_file_path}")
        sys.exit(1)
    p = Path(args.full_file_path)

    FileModifiedHandler(str(p.parent), p.name, args.i, args.f)

if __name__ == '__main__':
    main()