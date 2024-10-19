import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from pytube import YouTube

class YouTubeDownloader:
    def __init__(self, master):
        self.master = master
        self.master.title("YouTube Video Downloader")

        # Video URL
        self.url_label = tk.Label(master, text="YouTube Video URL:")
        self.url_label.pack(pady=5)

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack(pady=5)

        # Download Path
        self.path_label = tk.Label(master, text="Download Path:")
        self.path_label.pack(pady=5)

        self.path_entry = tk.Entry(master, width=50)
        self.path_entry.pack(pady=5)

        self.browse_button = tk.Button(master, text="Browse", command=self.browse)
        self.browse_button.pack(pady=5)

        # Download Type
        self.download_type_label = tk.Label(master, text="Download Type:")
        self.download_type_label.pack(pady=5)

        self.download_type_var = tk.StringVar(value="video")
        self.video_radio = tk.Radiobutton(master, text="Video", variable=self.download_type_var, value="video")
        self.video_radio.pack(pady=5)

        self.audio_radio = tk.Radiobutton(master, text="Audio Only", variable=self.download_type_var, value="audio")
        self.audio_radio.pack(pady=5)

        # Download Button
        self.download_button = tk.Button(master, text="Download", command=self.download)
        self.download_button.pack(pady=20)

    def browse(self):
        # Open file dialog to select download path
        download_path = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, download_path)

    def download(self):
        video_url = self.url_entry.get()
        download_path = self.path_entry.get()
        download_type = self.download_type_var.get()

        try:
            yt = YouTube(video_url)

            if download_type == "video":
                # List available video resolutions
                video_streams = yt.streams.filter(progressive=True)
                available_resolutions = [stream.resolution for stream in video_streams]

                # Ask user to select resolution
                resolution = tk.simpledialog.askstring("Select Resolution", f"Available resolutions: {available_resolutions}\nEnter your choice:")
                video_stream = video_streams.filter(res=resolution).first()

                if video_stream:
                    video_stream.download(output_path=download_path)
                    messagebox.showinfo("Success", f'Video "{yt.title}" has been downloaded successfully at {resolution}!')
                else:
                    messagebox.showwarning("Warning", "Selected resolution is not available.")
            
            elif download_type == "audio":
                audio_stream = yt.streams.filter(only_audio=True).first()
                audio_stream.download(output_path=download_path)
                messagebox.showinfo("Success", f'Audio from "{yt.title}" has been downloaded successfully!')
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main application window
root = tk.Tk()
youtube_downloader = YouTubeDownloader(root)
root.mainloop()
