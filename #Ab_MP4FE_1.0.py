#Ab_MP4FE_0.18
#Global
import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
from PIL import Image, ImageTk
stop_extraction = False
def select_video_path():
    global video_path
    video_path = filedialog.askopenfilename(title="Select a video file", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
    if video_path:
        video_path_label.config(text=f"Video path: {video_path}")
def select_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory(title="Select output folder")
    if output_folder:
        output_folder_label.config(text=f"Output folder: {output_folder}")
def extract_frames():
    global stop_extraction
    if video_path and output_folder:
        frames_folder = os.path.join(output_folder, "frames")
        os.makedirs(frames_folder, exist_ok=True)
        video_object = cv2.VideoCapture(video_path)
        total_frames = int(video_object.get(cv2.CAP_PROP_FRAME_COUNT))
        progress_bar['maximum'] = total_frames
        stop_extraction = False
        for frames in range(total_frames):
            if stop_extraction:
                break
            extract, frame = video_object.read()
            if not extract:
                break
            cv2.imwrite(os.path.join(frames_folder, f'frame_{frames}.png'), frame)
            progress_bar['value'] = frames + 1
            progress_bar.update()
        video_object.release()
        messagebox.showinfo("Extraction complete.", f"{frames+1} out of {total_frames} frames successfully extracted.")
def open_video_path_folder():
    if video_path:
        subprocess.Popen(['explorer', '/select,', os.path.normpath(video_path)])
def open_output_folder():
    if output_folder:
        subprocess.Popen(['explorer', os.path.normpath(output_folder)])
def close_program():
    root.destroy()
def on_drag(event):
    root.geometry(f"+{root.winfo_pointerx() - x}+{root.winfo_pointery() - y}")
def on_drag_start(event):
    global x, y
    x, y = event.x, event.y
def stop_extraction_process():
    global stop_extraction
    stop_extraction = True
#Main
root = tk.Tk()
root.title("MP4 frame extractor")
root.overrideredirect(True)
root.configure(background='#201c1c')
root.geometry("540x340")
frame = tk.Frame(root, bg='#201c1c')
frame.pack(padx=20, pady=20)
video_path = ""
output_folder = ""
open_video_icon_img = Image.open("D:\\Desktop\\Progra\\2023\\VideoFrameExtractor\\Open-File-Folder-Flat-icon.png")
open_video_icon_img = open_video_icon_img.resize((20, 20))
open_video_icon = ImageTk.PhotoImage(open_video_icon_img)
open_output_icon_img = Image.open("D:\\Desktop\\Progra\\2023\\VideoFrameExtractor\\Open-File-Folder-Flat-icon.png")
open_output_icon_img = open_output_icon_img.resize((20, 20))
open_output_icon = ImageTk.PhotoImage(open_output_icon_img)
video_button = tk.Button(frame, text="Select video", command=select_video_path, bg='#201c1c', fg='white')
video_button.grid(row=0, column=0, sticky='w', pady=10, padx=10)
video_path_label = tk.Label(frame, text="Video path: ", bg='#201c1c', fg='white')
video_path_label.grid(row=1, column=0, sticky='w')
output_button = tk.Button(frame, text="Select output folder", command=select_output_folder, bg='#201c1c', fg='white')
output_button.grid(row=2, column=0, sticky='w', pady=10, padx=10)
output_folder_label = tk.Label(frame, text="Output folder: ", bg='#201c1c', fg='white')
output_folder_label.grid(row=3, column=0, sticky='w')
open_video_path_button = tk.Button(frame, image=open_video_icon, command=open_video_path_folder, bg='#201c1c', borderwidth=0)
open_video_path_button.grid(row=1, column=1, sticky='e', pady=10, padx=10)
open_output_folder_button = tk.Button(frame, image=open_output_icon, command=open_output_folder, bg='#201c1c', borderwidth=0)
open_output_folder_button.grid(row=3, column=1, sticky='e', pady=10, padx=10)
start_button = tk.Button(frame, text="Extract", command=extract_frames, bg='#201c1c', fg='white')
start_button.grid(row=5, column=0, pady=5, columnspan=2)
close_button = tk.Button(root, text="Exit", command=close_program, bg='#201c1c', fg='white')
close_button.pack(padx=20, pady=0)
progress_bar = ttk.Progressbar(frame, orient='horizontal', length=300, mode='determinate')
progress_bar.grid(row=6, column=0, columnspan=2, pady=10)
root.bind("<B1-Motion>", on_drag)
root.bind("<Button-1>", on_drag_start)
stop_button = tk.Button(frame, text="Stop", command=stop_extraction_process, bg='#201c1c', fg='white')
stop_button.grid(row=5, column=0, pady=5, columnspan=2,sticky='e')
root.mainloop()