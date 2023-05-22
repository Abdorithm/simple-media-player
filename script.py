from customtkinter import *
from tkinter import *


import customtkinter as ctk
# from customtkinter import filedialog
from pygame import mixer
import tkinter as tk
import tkinter.ttk as ttk
import librosa
import soundfile as sf
import matplotlib.pyplot as plt
import pedalboard
from pedalboard import Pedalboard, Chorus, Reverb, Compressor, Delay, Distortion, Gain
from pedalboard.io import AudioFile
import shutil 
from pathlib import Path

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

            # board of effects  
            self.board = Pedalboard();
            # Buttons
            def_font = 'Helvetica Bold'
            btn_color = '#007a8a'
            txt_color = 'white'
            def_width = 80
            big_width = 100

            play_button = CTkButton(win, fg_color=btn_color, textvariable = self.play_restart, text_color = txt_color, width=def_width, font=(def_font, 10), hover=True, command=self.play)
            play_button.place(x=60, y=50, anchor='center')

            pause_button = CTkButton(win, fg_color=btn_color, textvariable = self.pause_resume, text_color = txt_color, width = def_width, font=(def_font, 10), hover=True, command=self.pause)
            pause_button.place(x=60, y=100, anchor='center')

            stop_button = CTkButton(win, fg_color=btn_color, text='Stop', text_color = txt_color, width = def_width, font=(def_font, 10), hover=True, command=self.stop)
            stop_button.place(x=60, y=150, anchor='center')

            next_button = CTkButton(win, fg_color=btn_color, text='Next', text_color = txt_color, width = def_width, font=(def_font, 10), hover=True, command=self.next_song)
            next_button.place(x=60, y=200, anchor='center')

            prev_button =CTkButton(win, fg_color = btn_color, text='Previous', text_color = txt_color, width = def_width, font=(def_font, 10), hover=True, command=self.prev_song)
            prev_button.place(x=60, y=250, anchor='center')

            compress_button = CTkButton(win, fg_color = btn_color, text='Compress', text_color = txt_color, width = def_width, font=(def_font, 10), hover=True, command=self.compress)
            compress_button.place(x=220, y=300, anchor='center')

            gain_button = CTkButton(win, fg_color = btn_color, text='Gain', text_color = txt_color, width = def_width, font=(def_font, 10), hover=True, command=self.gain)
            gain_button.place(x=320, y=300, anchor='center')
                
            reverb_button = CTkButton(win, fg_color = btn_color, text='Reverb', text_color = txt_color, width = def_width, font=(def_font, 10), hover=True, command=self.reverb)
            reverb_button.place(x=220, y=350, anchor='center')

            apply_effects_button = CTkButton(win, fg_color = btn_color, text='Apply Effects', text_color = txt_color, width = big_width, font=(def_font, 10), hover=True, command=self.Apply_added_effects)
            apply_effects_button.place(x=530, y = 350, anchor='center')
            
            delay_button = CTkButton(win, fg_color = btn_color, text='Delay', text_color = txt_color, width = def_width, font=(def_font, 10), hover=True, command=self.delay, anchor='center')
            delay_button.place(x=320, y=350, anchor='center')   

       

            self.playing_state = False

            # Playlist
            self.song_box = Listbox(bg="#004247", fg="cyan", borderwidth=0, width=45, selectbackground="cyan", selectforeground="#004247")
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
            self.volume_slider = CTkSlider(win, from_=0, to=1, orientation="vertical", command=self.volume)
            self.volume_slider.place(x=555, y=20)
            self.volume_frame = CTkLabel(root, text="Volume", font=('Courier Sans MS', 10))
            self.volume_frame.place(x=540, y=10)
            self.playing_state = False

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
            #Loaded song from files
            original_song = filedialog.askopenfilename(title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
            #copy original song to new song
            song_path = Path(original_song)
            song_name = song_path.stem + "_copy.mp3"
            song = shutil.copyfile(original_song, song_name)
            #Add song copy to playlist      
            self.song_box.insert(END, song)

        def add_many_songs(self):
            original_songs = filedialog.askopenfilenames(title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
            for original_song in original_songs:
                song_path = Path(original_song)
                song_name = song_path.stem + "_copy.mp3"
                song = shutil.copyfile(original_song, song_name)
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
            
        #Apply all the filters in the board to the song
        def Apply_added_effects(self):
            if(not self.board): return
            samplerate = 44100.0
            with AudioFile(self.song_box.get(ACTIVE)) as f:
                audio = f.read(f.frames)
            processed = self.board(audio, samplerate)
            with AudioFile(self.song_box.get(ACTIVE), "w", samplerate, processed.shape[0]) as f:
                f.write(processed)
            mixer.music.load(self.song_box.get(ACTIVE))
            mixer.music.play()
            
        def reverb(self):
            # Add reverb effect
            self.board.append(Reverb(room_size=0.2))
            
        def compress(self):
            # Add a compressor pedal
            self.board.append(Compressor(threshold_db=-20, ratio=5, attack_ms=10, release_ms=50))
            
        def delay(self):
            # Add a delay pedal
            self.board.append(Delay(delay_seconds=0.2))
        
        def distortion(self):
            # Add a distortion pedal
            self.board.append(Distortion(distortion=0.2))
            
            
        def gain(self):
            self.board.append(Gain(gain_db=10))
           
        #function to reset alll effects (get the original song that our playing song was copied from)
        #TO BE IMPLEMENTED 
        def reset_audio_effects():
            board = Pedalboard();

root = CTk()
MP(root)
root.mainloop()
