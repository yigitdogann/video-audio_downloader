import customtkinter as ctk
import yt_dlp
from tkinter import messagebox, filedialog
import os

# appearance settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# main window
root = ctk.CTk()
root.title("Video ve Ses İndirici")
root.geometry("550x300")
root.resizable(False, False)

# desktop chose as default
destination = os.path.join(os.path.expanduser("~"), "Desktop")

# choose a folder for upcoming downloads
def select_folder():
    global destination
    chose = filedialog.askdirectory()
    if chose:
        destination = chose
        folder_label.configure(text=f"📂 {destination}")

# download
def download():
    link = get_link.get().strip()
    which_format = format_pick.get()

    if not link:
        messagebox.showerror("Hata", "Lütfen bir link girin!")
        return

    try:
        if which_format == "MP3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(destination, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:  # MP4
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(destination, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
            }

        update_label.configure(text="📥 İndiriliyor...")
        root.update_idletasks()

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        update_label.configure(text="İndirme tamamlandı.")
        messagebox.showinfo("Başarılı", f"İndirme tamamlandı!\nKlasör: {destination}")

    except Exception as e:
        messagebox.showerror("Hata", str(e))
        update_label.configure(text="İndirme başarısız!")

# Link label
link_label = ctk.CTkLabel(root, text="Video Linki:", font=("Arial", 16))
link_label.pack(pady=10)

# Link input
get_link = ctk.CTkEntry(root, width=400, height=35, font=("Arial", 14))
get_link.pack()

# box for format and destination
choosing_frame = ctk.CTkFrame(root)
choosing_frame.pack(pady=15)

# Format
format_pick = ctk.CTkComboBox(choosing_frame, values=["MP4", "MP3"], width=120, height=35, font=("Arial", 14))
format_pick.set("MP4")
format_pick.grid(row=0, column=0, padx=10)

# destination button
destination_btn = ctk.CTkButton(choosing_frame, text="Klasör Seç", width=150, height=35, command=select_folder)
destination_btn.grid(row=0, column=1, padx=10)

# destination folder label
folder_label = ctk.CTkLabel(root, text=f"📂 {destination}", font=("Arial", 12))
folder_label.pack()

# download button
download_button = ctk.CTkButton(root, text="İndir", width=150, height=40, font=("Arial", 16), command=download)
download_button.pack(pady=15)

# update label
update_label = ctk.CTkLabel(root, text="", font=("Arial", 14))
update_label.pack()

root.mainloop()