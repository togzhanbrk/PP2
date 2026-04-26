import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = music_folder

        self.playlist = []
        for file in os.listdir(music_folder):
            if file.endswith(".mp3") or file.endswith(".wav"):
                self.playlist.append(file)

        self.current_index = 0
        self.is_playing = False

        if len(self.playlist) > 0:
            self.load_track()

    def load_track(self):
        path = os.path.join(self.music_folder, self.playlist[self.current_index])
        pygame.mixer.music.load(path)

    def play(self):
        if len(self.playlist) == 0:
            return

        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if len(self.playlist) == 0:
            return

        self.current_index += 1

        if self.current_index >= len(self.playlist):
            self.current_index = 0

        self.load_track()
        self.play()

    def previous_track(self):
        if len(self.playlist) == 0:
            return

        self.current_index -= 1

        if self.current_index < 0:
            self.current_index = len(self.playlist) - 1

        self.load_track()
        self.play()

    def get_current_track(self):
        if len(self.playlist) == 0:
            return "No music files"

        return self.playlist[self.current_index]