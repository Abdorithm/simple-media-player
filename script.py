from tkinter import *
import tkinter as tk
from tkinter import filedialog
from pygame import mixer
import tkinter.ttk as ttk


class MP:
    def __init__(self, win):
        # Initialize pygame mixer
        mixer.init()

        # Create Tkinter window
        win.geometry('600x400')
        win.configure(background='#004247')
        win.title('Music Player')
        win.resizable(0, 0)

        # StringVar to change button text later
        self.play_restart = tk.StringVar()
        self.pause_resume = tk.StringVar()
        self.play_restart.set('Play')
        self.pause_resume.set('Pause')

        # Buttons
        play_button = Button(win, bg='#007a8a',textvariable=self.play_restart, borderwidth=0, width=5, font=('Courier Sans MS', 10), command=self.play)
        play_button.place(x=60, y=50, anchor='center')

        pause_button = Button(win, bg='#007a8a',textvariable=self.pause_resume, borderwidth=0, width=5, font=('Courier Sans MS', 10), command=self.pause)
        pause_button.place(x=60, y=100, anchor='center')

        stop_button = Button(win, bg='#007a8a', text='Stop', borderwidth=0, width=5, font=('Courier Sans MS', 10), command=self.stop)
        stop_button.place(x=60, y=150, anchor='center')

        next_button = Button(win, bg='#007a8a', text='Next', borderwidth=0, width=5, font=('Courier Sans MS', 10), command=self.next_song)
        next_button.place(x=60, y=200, anchor='center')

        prev_button = Button(win, bg='#007a8a', text='Previous', borderwidth=0, width=5, font=('Courier Sans MS', 10), command=self.prev_song)
        prev_button.place(x=60, y=250, anchor='center')

        self.playing_state = False

        # Playlist
        self.song_box = Listbox(bg="black", fg="cyan", borderwidth=0, width=50, selectbackground="#007a8a", selectforeground="black")
        self.song_box.place(x=130, y=35)

        # Create Menus
        my_menu = Menu(root)
        root.config(menu=my_menu)
    
        # Adding songs
        add_song_menu = Menu(my_menu)
        my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
        add_song_menu.add_command(label="Add One Song To Playlist", command=self.add_song)
        add_song_menu.add_command(label="Add Many Songs To Playlist", command=self.add_many_songs)

        # Deleting songs
        remove_song_menu = Menu(my_menu)
        my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
        remove_song_menu.add_command(label="Delete A Song From Playlist", command=self.delete_song)
        remove_song_menu.add_command(label="Delete All Songs From Playlist", command=self.delete_all_songs)

        # Volume slider
        self.volume_slider = ttk.Scale(from_=0, to=1, orient=VERTICAL, value=1, command=self.volume, length=155)
        self.volume_slider.place(x=555, y=60)
        self.volume_frame = Label(text="Volume", borderwidth=0, bg='#004247', font=('Courier Sans MS', 10), fg="white")
        self.volume_frame.place(x=540, y=35)

    def play(self):
        if self.song_box:
            song = self.song_box.get(ACTIVE)
            # song = f'/home/abdo/Desktop/media-player-python/music/{song}'
            mixer.music.load(song)
            mixer.music.play()
            self.playing_state = False
            self.pause_resume.set('Pause')

    def pause(self):
        if not self.playing_state:
            mixer.music.pause()
            self.playing_state = True
            self.pause_resume.set('Resume')
        else:
            mixer.music.unpause()
            self.playing_state = False
            self.pause_resume.set('Pause')

    def stop(self):
        mixer.music.fadeout(1500)

    def add_song(self):
        song = filedialog.askopenfilename(title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
        # song = song.replace("/home/abdo/Desktop/media-player-python/music/", "")
        self.song_box.insert(END, song)

    def add_many_songs(self):
        songs = filedialog.askopenfilenames(title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
        for song in songs:
            # song = song.replace("/home/abdo/Desktop/media-player-python/music/", "")
            self.song_box.insert(END, song)

    def delete_song(self):
        self.song_box.delete(ANCHOR)
        mixer.music.stop()

    def delete_all_songs(self):
	    self.song_box.delete(0, END)
	    mixer.music.stop()

    def next_song(self):
        next_one = self.song_box.curselection()
        next_one = next_one[0]+1
        song = self.song_box.get(next_one)
        # song = f'/home/abdo/Desktop/media-player-python/music/{song}'
        mixer.music.load(song)
        mixer.music.play(loops=0)
        self.song_box.selection_clear(0, END)
        self.song_box.activate(next_one)
        self.song_box.selection_set(next_one, last=None)

    def prev_song(self):
        next_one = self.song_box.curselection()
        next_one = next_one[0]-1
        song = self.song_box.get(next_one)
        # song = f'/home/abdo/Desktop/media-player-python/music/{song}'
        mixer.music.load(song)
        mixer.music.play(loops=0)
        self.song_box.selection_clear(0, END)
        self.song_box.activate(next_one)
        self.song_box.selection_set(next_one, last=None)

    def volume(self, x):
        mixer.music.set_volume(self.volume_slider.get())

root = Tk()
MP(root)
root.mainloop()
