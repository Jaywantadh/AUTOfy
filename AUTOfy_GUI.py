import tkinter as tk 
from tkinter import filedialog, messagebox, simpledialog 
import threading 
from PIL import Image, ImageTk
import SpotifyClient as SC

class SpotifyApp:
    def __init__(self, root, spotify_client):
        self.root = root
        self.spotify_client = spotify_client

        self.root.title("Welcome to AutoFY!")
        self.frame = tk.Frame(root)
        self.frame.pack(pady = 20)

        self.listbox = tk.Listbox(self.frame, width = 100, height = 10)
        self.listbox.pack(side= tk.RIGHT, padx = 10)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.browse_button = tk.Button(root, text = "Import Songs From File", command= self.browse_files)
        self.browse_button.pack(pady = 10)

        self.play_button = tk.Button(root, text = "Play", command = lambda: self.control_play("play"))
        self.play_button.pack(pady = 5)

        self.pause_button = tk.Button(root, text = "Pause", command = lambda: self.control_pause("pause"))
        self.pause_button.pack(pady = 5)

        self.next_button = tk.Button(root, text = "Next", command = lambda: self.control_next("next"))
        self.next_button.pack(pady = 5)

        self.previous_button = tk.Button(root, text = "Previous", command = lambda: self.control_previous("previous"))
        self.previous_button.pack(pady = 5)

        self.current_song_button = tk.Button(root, text = "Current Song", command = self.show_current_song)
        self.current_song_button.pack(pady = 5)

        self.save_playlist_button = tk.Button(root, text = "Save Playlist", command = self.save_playlist)
        self.save_playlist_button.pack(pady = 5)

        self.load_playlist_button = tk.Button(root, text = "Load Playlist", command = self.load_playlist)
        self.load_playlist_button.pack(pady = 5)

        self.load_drag_drop_image()
        self.setup_drag_drop()

    def load_drag_drop_image(self):
        image = Image.open("Drag_Drop.png")
        image = image.resize((400,200), Image.LANCZOS)
        self.drag_drop_image = ImageTk.PhotoImage(image)
        self.drag_drop_label = tk.Label(self.root, image = self.drag_drop_image)
        self.drag_drop_label.pack(pady = 10)

    def browse_files(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt", ".csv")])
        if file_path:
            with open(file_path, 'r') as file:
                songs = file.readlines()
            for song in songs:
                 song_name = self.spotify_client.search_and_queue_song(song.strip())
                 if song_name: 
                     self.listbox.insert(tk.END, f"Queued: {song_name}")
                 else:
                     self.listbox.insert(tk.END, f"Song not Found: {song.strip()}")
    
    def setup_drag_drop(self):
        self.drag_drop_label.bind("<Button-1>", self.on_drag_drop_click)

    def on_drag_drop_click(self, event):
        song_name = simpledialog.askstring("Queue song", "Enter the song name: ")
        if song_name:
            self.queue_song(song_name)

    def queue_song(self, song_name):
        song_name = self.spotify_client.search_and_queue_song(song_name)
        if song_name:
            self.listbox.insert(tk.END, f"Queued: {song_name}")
        else:
            self.listbox.insert(tk.END, f"Song not found: {song_name}")

    def control_playback(self, action):
        self.spotify_client.control_playback(action)

    def show_current_song(self):
        current_song = self.spotify_client.get_current_playback()
        if current_song:
            messagebox.showinfo("Current Song", current_song)
        else:
            messagebox.showerror("Error", "Unable to retrieve current song.")

    def save_playlist(self):
        playlist_name = simpledialog.askstring("Save Playlist", "Enter playlist name:")
        if playlist_name:
            playlist_id = self.spotify_client.create_playlist(playlist_name)
            if playlist_id:
                track_uris = self.get_queued_track_uris()
                self.spotify_client.add_tracks_to_playlist(playlist_id, track_uris)
                messagebox.showinfo("Success", f"Playlist '{playlist_name}' saved successfully.")
            else:
                messagebox.showerror("Error", "Failed to create playlist.")

    def load_playlist(self):
        playlist_id = simpledialog.askstring("Load Playlist", "Enter playlist ID: ")
        if playlist_id:
            track_names = self.spotify_client.load_playlist(playlist_id)
            if track_names:
                self.listbox.delete(0, tk.END)
                for track_name in track_names:
                    self.listbox.insert(tk.END, f"Queued: {track_name}")
            else:
                messagebox.showerror("Error", "Failed to load playlist.")

    def get_queued_track_uris(self):
        return[self.listbox.get(idx).split()[-1] for idx in range(self.listbox.size())]
    

def main():
    root = tk.Tk()
    app =  SpotifyApp(root, SC.SpotifyClient)
    root.mainloop()

if __name__ == "__main__":
    main()

