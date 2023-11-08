from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
from PIL import ImageTk
import moviepy.editor as mp

class VideoAudioConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("MP4 to MP3 Converter by YobraVeloper")
        self.root.geometry('600x400')
        self.root.configure(bg='white')

        # Styling
        self.custom_font = ('Helvetica', 12)

        # Background Image
        self.bg = ImageTk.PhotoImage(file='C:\Jects\Misc/bg_image.jpg')
        Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        # Labels and Instructions
        Label(self.root, text="MP4 to MP3 Converter", font=("Arial", 20), bg='white').place(x=150, y=20)
        Label(self.root, text="Select an MP4 video file to convert to MP3:", font=self.custom_font, bg='white').place(x=20, y=70)

        # Browse Button
        browse_button = Button(self.root, text="Browse Files", font=self.custom_font, command=self.browse)
        browse_button.place(x=20, y=100)

        # Output File Label
        self.output_label = Label(self.root, text='', font=self.custom_font, bg="white")
        self.output_label.place(x=20, y=150)

    def browse(self):
        self.file_name = filedialog.askopenfilename(title="Select a File", filetypes=(("Video files", "*.mp4*"),))
        if self.file_name:
            self.output_label.config(text=f"Selected File: {os.path.basename(self.file_name)}")
            self.convert(os.path.basename(self.file_name))

    def convert(self, filename):
        try:
            clip = mp.VideoFileClip(filename)
            audio_filename = f"{filename[:-4]}.mp3"
            clip.audio.write_audiofile(audio_filename)
            messagebox.showinfo("Conversion Complete", f"File '{os.path.basename(filename)}' converted to '{os.path.basename(audio_filename)}'")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = Tk()
    obj = VideoAudioConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
