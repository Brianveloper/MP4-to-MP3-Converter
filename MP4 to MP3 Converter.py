from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
import os
from PIL import ImageTk
import moviepy.editor as mp
import subprocess

class VideoAudioConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to Audio Converter")
        self.root.geometry('600x400')
        self.root.configure(bg='#3498db')

        self.custom_font = ('Helvetica', 12)

        self.output_label = Label(self.root, text='', font=self.custom_font, bg='#3498db', fg='white')
        self.output_label.pack(pady=20)
        self.converted_file = None

        self.create_ui()

        # Audio Format Options
        self.audio_format = StringVar(value="mp3")
        format_label = Label(self.root, text="Select Audio Format:", font=self.custom_font, bg='#3498db', fg='white')
        format_label.pack()
        mp3_radio = Radiobutton(self.root, text="MP3", variable=self.audio_format, value="mp3", font=self.custom_font, bg='#3498db', fg='white')
        mp3_radio.pack()
        wav_radio = Radiobutton(self.root, text="WAV", variable=self.audio_format, value="wav", font=self.custom_font, bg='#3498db', fg='white')
        wav_radio.pack()
        flac_radio = Radiobutton(self.root, text="FLAC", variable=self.audio_format, value="flac", font=self.custom_font, bg='#3498db', fg='white')
        flac_radio.pack()

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.root, mode='determinate', length=200)
        self.progress_bar.place(x=20, y=200)

    def create_ui(self):
        label = Label(self.root, text="Video to Audio Converter", font=("Arial", 20), bg='#3498db', fg='white')
        label.pack(pady=20)

        label = Label(self.root, text="Select a video file to convert to audio:", font=self.custom_font, bg='#3498db', fg='white')
        label.pack()

        browse_button = Button(self.root, text="Browse Files", font=self.custom_font, command=self.browse, bg='#e74c3c', fg='white')
        browse_button.pack(pady=10)

        convert_button = Button(self.root, text="Convert", font=self.custom_font, command=self.convert, bg='#2ecc71', fg='white')
        convert_button.pack(pady=10)

        view_button = Button(self.root, text="View Converted File", font=self.custom_font, command=self.view_converted_file, bg='#f1c40f', fg='white')
        view_button.pack(pady=10)

        for button in (browse_button, convert_button, view_button):
            button.bind("<Enter>", lambda event, b=button: self.on_hover(event, b))
            button.bind("<Leave>", lambda event, b=button: self.on_leave(event, b))

    def on_hover(self, event, button):
        button.config(bg='#d35400')  # Change to a different color when hovered

    def on_leave(self, event, button):
        button.config(bg='#e74c3c')  # Change back to the original color when the mouse leaves

    def browse(self):
        self.file_name = filedialog.askopenfilename(title="Select a File", filetypes=(("Video files", "*.mp4*"),))
        if self.file_name:
            self.output_label.config(text=f"Selected File: {self.file_name}")

    def convert(self):
        if not self.file_name:
            messagebox.showerror("Error", "Please select a file to convert.")
            return
        try:
            clip = mp.VideoFileClip(self.file_name)

            # Reduce resolution
            clip = clip.resize(height=720)  # Change the height as needed

            # Change the frame rate by creating a subclip with the desired duration
            new_duration = clip.duration * (25 / clip.fps)
            clip = clip.subclip(0, new_duration)

            audio_format = self.audio_format.get()
            audio_filename = f"{os.path.splitext(self.file_name)[0]}.{audio_format}"
            if not os.path.exists(audio_filename):
                total_frames = int(clip.fps * clip.duration)
                for i, _ in enumerate(clip.iter_frames(fps=clip.fps), 1):
                    self.update_progress(i / total_frames * 100)
                clip.audio.write_audiofile(audio_filename, codec=audio_format)
                self.converted_file = audio_filename
                self.progress_bar["value"] = 0  # Reset progress bar
                messagebox.showinfo("Conversion Complete", f"File '{os.path.basename(self.file_name)}' converted to '{os.path.basename(audio_filename)}'")
            else:
                confirm = messagebox.askokcancel("File Exists", f"'{os.path.basename(audio_filename)}' already exists. Do you want to overwrite it?")
                if confirm:
                    clip.audio.write_audiofile(audio_filename, codec=audio_format)
                    self.converted_file = audio_filename
                    messagebox.showinfo("Conversion Complete", f"File '{os.path.basename(self.file_name)}' converted to '{os.path.basename(audio_filename)}'")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_progress(self, value):
        self.progress_bar["value"] = value
        self.root.update_idletasks()

    def view_converted_file(self):
        if self.converted_file:
            subprocess.Popen([self.converted_file], shell=True)
        else:
            messagebox.showerror("Error", "No converted file to view. Please convert a file first.")

def main():
    root = ThemedTk(theme="arc")  # Create a themed Tkinter window
    obj = VideoAudioConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
