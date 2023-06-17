import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QSlider, QFileDialog
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from pathlib import Path
import shutil
from pyqtgraph import PlotWidget
import numpy as np
import soundfile as sf
from pedalboard import Pedalboard, Reverb, Compressor, Delay, Distortion, Gain, HighpassFilter, LowpassFilter, Clipping
from pedalboard.io import AudioFile
from scipy.io import wavfile


class MusicPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.media_player = QMediaPlayer()

        self.setWindowTitle("Music Player")
        self.setGeometry(200, 200, 600, 400)
        self.setStyleSheet("background-color: #004247;")
        self.setFixedSize(1200, 800)
     

        self.playing_state = False

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.song_label = QLabel("Now Playing: None", self.central_widget)
        self.layout.addWidget(self.song_label)

        self.song_box = QListWidget(self.central_widget)
        self.song_box.setStyleSheet(
            "background-color: #004247; color: cyan; border: none; selection-background-color: cyan; selection-color: #004247;"
        )
        self.layout.addWidget(self.song_box)

        self.volume_slider = QSlider(Qt.Vertical, self.central_widget)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged[int].connect(self.media_player.setVolume)
        self.layout.addWidget(self.volume_slider)

        self.progress_slider = QSlider(Qt.Horizontal, self.central_widget)
        self.progress_slider.setMinimum(0)
        self.progress_slider.sliderReleased.connect(self.set_position)
    
        
        self.layout.addWidget(self.progress_slider)
        self.media_player.positionChanged.connect(self.update_position_and_duration)

        self.waveform_plot = PlotWidget(self.central_widget)
        self.waveform_plot.setMinimumHeight(100)
        self.layout.addWidget(self.waveform_plot)

        self.control_layout = QHBoxLayout()

        self.play_button = QPushButton("Play", self.central_widget)
        self.control_layout.addWidget(self.play_button)
        self.play_button.clicked.connect(self.play)

        self.pause_button = QPushButton("Pause", self.central_widget)
        self.control_layout.addWidget(self.pause_button)
        self.pause_button.clicked.connect(self.pause)

        self.stop_button = QPushButton("Stop", self.central_widget)
        self.control_layout.addWidget(self.stop_button)
        self.stop_button.clicked.connect(self.stop)

        self.next_button = QPushButton("Next", self.central_widget)
        self.control_layout.addWidget(self.next_button)
        self.next_button.clicked.connect(self.next_song)

        self.prev_button = QPushButton("Previous", self.central_widget)
        self.control_layout.addWidget(self.prev_button)
        self.prev_button.clicked.connect(self.prev_song)

        self.reverb_button = QPushButton("Reverb", self.central_widget)
        self.control_layout.addWidget(self.reverb_button)
        self.reverb_button.clicked.connect(self.reverb)

        self.compressor_button = QPushButton("Compressor", self.central_widget)
        self.control_layout.addWidget(self.compressor_button)
        self.compressor_button.clicked.connect(self.compress)

        self.delay_button = QPushButton("Delay", self.central_widget)
        self.control_layout.addWidget(self.delay_button)
        self.delay_button.clicked.connect(self.delay)

        self.distortion_button = QPushButton("Distortion", self.central_widget)
        self.control_layout.addWidget(self.distortion_button)
        self.distortion_button.clicked.connect(self.distortion)

        self.gain_button = QPushButton("Gain", self.central_widget)
        self.control_layout.addWidget(self.gain_button)
        self.gain_button.clicked.connect(self.gain)
        
        self.highpass_button = QPushButton("Highpass", self.central_widget)
        self.control_layout.addWidget(self.highpass_button)
        self.highpass_button.clicked.connect(self.high_pass)
        
        self.lowpass_button = QPushButton("Lowpass", self.central_widget)
        self.control_layout.addWidget(self.lowpass_button)
        self.lowpass_button.clicked.connect(self.low_pass)
        
        self.apply_effects_button = QPushButton("Apply Effects", self.central_widget)
        self.control_layout.addWidget(self.apply_effects_button)
        self.apply_effects_button.clicked.connect(self.apply_effects)

        self.layout.addLayout(self.control_layout)

        self.board = Pedalboard()
        self.playing_state = False
        self.add_menu()

        self.timer = QTimer(self)
        self.timer.setInterval(100)  # Update waveform every 100 milliseconds
        self.timer.timeout.connect(self.update_waveform)

    def add_menu(self):
        menu_bar = self.menuBar()

        add_song_menu = menu_bar.addMenu("Add Songs")
        add_one_song_action = add_song_menu.addAction("Add One Song to Playlist")
        add_one_song_action.triggered.connect(self.add_song)

        add_many_songs_action = add_song_menu.addAction("Add Many Songs to Playlist")
        add_many_songs_action.triggered.connect(self.add_many_songs)

        remove_song_menu = menu_bar.addMenu("Remove Songs")
        delete_song_action = remove_song_menu.addAction("Delete a Song from Playlist")
        delete_song_action.triggered.connect(self.delete_song)

        delete_all_songs_action = remove_song_menu.addAction("Delete All Songs from Playlist")
        delete_all_songs_action.triggered.connect(self.delete_all_songs)

    def play(self):
        if self.song_box.currentRow() >= 0:
            song = self.song_box.currentItem().text()
            self.song_label.setText(f"Now Playing: {Path(Path(song).stem).suffix}")
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(song)))
            self.media_player.play()
            self.playing_state = True
            self.timer.start()  # Start waveform visualization update

    def pause(self):
        if self.playing_state:
            self.media_player.pause()
            self.playing_state = False
            self.timer.stop()  # Stop waveform visualization update
        else:
            self.media_player.play()
            self.playing_state = True
            self.timer.start()  # Start waveform visualization update

    def stop(self):
        self.media_player.stop()
        self.playing_state = False
        self.timer.stop()  # Stop waveform visualization update

    def add_song(self):
        original_song, _ = QFileDialog.getOpenFileName(self, "Choose a Song", "", "MP3 Files (*.mp3)")
        song_name = original_song[:len(original_song) - 4] + "_copy.mp3"
        song = shutil.copyfile(original_song, song_name)
        self.song_box.addItem(song)

    def add_many_songs(self):
        original_songs, _ = QFileDialog.getOpenFileNames(self, "Choose Songs", "", "MP3 Files (*.mp3)")
        for original_song in original_songs:
            song_name = original_song[:len(original_song) - 4] + "_copy.mp3"
            song = shutil.copyfile(original_song, song_name)
            self.song_box.addItem(song)

    def delete_song(self):
        current_row = self.song_box.currentRow()
        self.song_box.takeItem(current_row)
        self.stop()

    def delete_all_songs(self):
        self.song_box.clear()
        self.stop()

    def next_song(self):
        current_row = self.song_box.currentRow()
        next_row = current_row + 1 if current_row < self.song_box.count() - 1 else 0
        self.song_box.setCurrentRow(next_row)
        self.play()

    def prev_song(self):
        current_row = self.song_box.currentRow()
        prev_row = current_row - 1 if current_row > 0 else self.song_box.count() - 1
        self.song_box.setCurrentRow(prev_row)
        self.play()

    def set_position(self):
        position = self.progress_slider.value()
        self.media_player.setPosition(position)

    def update_position_and_duration(self):
        position = self.media_player.position()
        duration = self.media_player.duration()
        self.progress_slider.setRange(0, duration)
        self.progress_slider.setValue(position)

    def update_waveform(self):
        if self.playing_state:
            current_song = self.song_box.currentItem().text()
            if current_song:
                data, samplerate = sf.read(current_song)
                duration = self.media_player.duration() / 1000  # Convert to seconds

                if duration > 0:
                    position = self.media_player.position() / 1000 # Convert to seconds

                    start_index = int((len(data) / duration) * position)
                    end_index = int((len(data) / duration) * (position + 1))

                    waveform_data = data[start_index:end_index, 0]  # Use only the first channel if stereo

                    # Normalize the waveform data to the range [-1, 1]
                    max_amplitude = np.max(np.abs(waveform_data))
                    normalized_data = waveform_data / max_amplitude

                    # Create the x-axis values for the waveform plot
                    num_samples = len(normalized_data)
                    x_values = np.linspace(0, duration, num_samples)

                    # Clear the waveform plot
                    self.waveform_plot.clear()

                    # Plot the waveform data
                    self.waveform_plot.plot(x_values, normalized_data, pen='w')


    def apply_effects(self):
        if not self.board:
            return

        position = self.media_player.position()
        self.pause()
        position = self.progress_slider.value()
        samplerate = 44100.0
        with AudioFile(self.song_box.currentItem().text()) as f:
            audio = f.read(f.frames)
        processed = self.board(audio, samplerate)
        with AudioFile(self.song_box.currentItem().text(), "w", samplerate, processed.shape[0]) as f:
            f.write(processed)

        self.progress_slider.setValue(position)
        self.media_player.setPosition(position)

        self.pause()
        # self.timer.start()  # Start waveform visualization update

    def reverb(self):
        self.board.append(Reverb(room_size=0.2))

    def compress(self):
        self.board.append(Compressor(threshold_db=-20, ratio=5, attack_ms=10, release_ms=50))

    def delay(self):
        self.board.append(Delay(delay_seconds=0.2))

    def distortion(self):
        self.board.append(Distortion())

    def gain(self):
        self.board.append(Gain(gain_db=10))
        
    #hih pass filter function
    def high_pass(self):
        self.board.append(HighpassFilter(3000))
        
    #low pass filter function
    def low_pass(self):
        self.board.append(LowpassFilter(500))
        
    def clip(self):
        self.board.append(Clipping(55))
        

    

    def reset_audio_effects(self):
        self.board = Pedalboard()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayerApp()
    player.show()
    sys.exit(app.exec_())
