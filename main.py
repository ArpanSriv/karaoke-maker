from spleeter.separator import Separator as S_Separator
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import *
from tkinter.ttk import *
import moviepy.editor as mp
import tempfile
import os

from datetime import datetime

class ErrorLogger():
    def __init__(self):
        self.logs = []

    def write(self, text):
        self.logs.append("ERR: {}: {}".format(datetime.now(), text))


    def flush(self):
        pass

    def clear(self):
        self.logs = []

    def save_to_file(self):
        desktop = os.path.expanduser("~/Desktop")
        export_path = os.path.join(desktop, 'KARAOKE LOG {}.log'.format(datetime.now()))

        with open(export_path, 'w') as f:
            for item in self.logs:
                f.write("%s\n" % item)


class PrintLogger():  # create file like object
    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref
        self.logs = []

    def write(self, text):
        self.textbox.insert(tk.END, "  " + text)  # write text to textbox
        # could also scroll to end of textbox here to make sure always visible
        self.logs.append("OUT: {}: {}".format(datetime.now(), text))

    def flush(self):  # needed for file like object
        pass

    def save_to_file(self):
        desktop = os.path.expanduser("~/Desktop")
        export_path = os.path.join(desktop, 'KARAOKE LOG {}.log'.format(datetime.now()))

        with open(export_path, 'w') as f:
            for item in self.logs:
                f.write("%s\n" % item)





    


import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("Karaoke Maker")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        status_box=tk.Text(root)
        ft = tkFont.Font(family='Arial',size=12)
        status_box["font"] = ft
        status_box["fg"] = "#333333"
        # status_box["justify"] = "center"
        # status_box["text"] = "Message"
        status_box.place(x=10,y=170,width=578,height=266)

        self.status_box = status_box

        title_label=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=22)
        title_label["font"] = ft
        title_label["fg"] = "#333333"
        title_label["justify"] = "center"
        title_label["text"] = "Karaoke Maker"
        title_label["relief"] = "flat"
        title_label.place(x=10,y=10,width=162,height=50)

        contact_label=tk.Label(root)
        contact_label["anchor"] = "e"
        ft = tkFont.Font(family='Arial',size=12)
        contact_label["font"] = ft
        contact_label["fg"] = "#333333"
        contact_label["justify"] = "center"
        contact_label["text"] = "Contact - Arpan Srivastava"
        contact_label.place(x=390,y=20,width=188,height=30)

        file_select_label=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=12)
        file_select_label["font"] = ft
        file_select_label["fg"] = "#333333"
        file_select_label["justify"] = "center"
        file_select_label["text"] = "Please select the Lyrical Video File (.mp4):"
        file_select_label.place(x=10,y=60,width=289,height=53)

        file_open_button=tk.Button(root)
        file_open_button["bg"] = "#efefef"
        ft = tkFont.Font(family='Arial',size=10)
        file_open_button["font"] = ft
        file_open_button["fg"] = "#000000"
        file_open_button["justify"] = "center"
        file_open_button["text"] = "Select File"
        file_open_button.place(x=310,y=70,width=116,height=34)
        file_open_button["command"] = self.file_open_callback

        # status_label=tk.Label(root)
        # ft = tkFont.Font(family='Arial',size=12)
        # status_label["font"] = ft
        # status_label["fg"] = "#333333"
        # status_label["justify"] = "center"
        # status_label["text"] = "Status Bar"
        # status_label.place(x=20,y=120,width=388,height=34)

        

        progress_bar=Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
        progress_bar.place(x=20,y=120,width=162+388,height=34)
        
        # Store a reference to progressbar
        self.progress_bar = progress_bar

        bug_info_label=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        bug_info_label["font"] = ft
        bug_info_label["fg"] = "#333333"
        bug_info_label["justify"] = "center"
        bug_info_label["text"] = "In case of a bug, click this button to send the logs to the developer: "
        bug_info_label.place(x=10,y=450,width=388,height=30)

        bug_send_button=tk.Button(root)
        bug_send_button["bg"] = "#efefef"
        ft = tkFont.Font(family='Arial',size=10)
        bug_send_button["font"] = ft
        bug_send_button["fg"] = "#000000"
        bug_send_button["justify"] = "center"
        bug_send_button["text"] = "Send Data"
        bug_send_button.place(x=400,y=450,width=77,height=30)
        bug_send_button["command"] = self.bug_send_callback

        self.print_logger = PrintLogger(status_box)
        self.error_logger = ErrorLogger()
        
        sys.stdout = self.print_logger
        sys.stderr = self.error_logger

        print("\n Welcome to Karaoke Maker. Please select a file to start.")

    def file_open_callback(self):
        filename = fd.askopenfilename(title="File to convert", filetypes=[
                              ("Video Files", ".mp4")])

        if filename == "":
            return

        self.filename = filename

        print("\nSelected file: {}. Starting conversion...".format(filename))

        self.progress_bar['value'] = 10
        print("\n\n(1/4): File Selected, Extracting Audio from the Video...")

        root.update()
        root.after(1000, self.separate_audio_video(filename))

        self.progress_bar['value'] = 30
        print("\n\n(2/4): Audio Extracted from file, removing vocals...")

        root.update()
        root.after(1000, self.separate_stems())

        self.progress_bar['value'] = 60
        print("\n\n(3/4): Vocals Separated, Replacing Audio in Original Video...")

        root.update()
        root.after(1000, self.replace_audio())

        self.progress_bar['value'] = 100
        print("\n\n(4/4): Clip Ready. It's on the desktop")


    def bug_send_callback(self):
        print("Saving logs to desktop...")

        self.error_logger.save_to_file()
        self.print_logger.save_to_file()

        print("Saved. Please email this file to sriv.arpan@gmail.com")

    def separate_audio_video(self, filename):
        self.original_clip = mp.VideoFileClip(filename)
        
        # Create Temp Dir
        self.temp_dir = tempfile.TemporaryDirectory()

        print("Created temp_dir: {}".format(self.temp_dir.name))

        self.audio_file_separated_path = os.path.join(self.temp_dir.name, 'audio_out.mp3')
        self.original_clip.audio.write_audiofile(self.audio_file_separated_path)

    def separate_stems(self):
        from spleeter.separator import Separator as S_Separator
        separator = S_Separator('spleeter:2stems', stft_backend='tensorflow', multiprocess=True)
        separator.separate_to_file(
            audio_descriptor=self.audio_file_separated_path, destination=os.path.join(self.temp_dir.name, 'output'))

    def replace_audio(self):
        bg_audio_clip = mp.AudioFileClip(os.path.join(self.temp_dir.name, os.path.join('output', os.path.join('audio_out', 'accompaniment.wav'))))
        new_clip = self.original_clip.set_audio(bg_audio_clip)

        path_to_desktop = os.path.expanduser("~/Desktop")

        file_basename = os.path.basename(self.filename)
        file_clean = "{} KARAOKE.mp4".format(os.path.splitext(file_basename)[0])

        new_clip.write_videofile(os.path.join(path_to_desktop, file_clean))

    def cleanup(self):
        self.temp_dir.cleanup()
        self.progress_bar['value'] = 0
        self.filename = None
        self.original_clip = None
        self.audio_file_separated_path = None

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
