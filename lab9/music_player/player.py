import os
import pygame


class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        self.playlist = self.load_playlist()
        self.current_index = 0

    def load_playlist(self):
        formats = (".mp3", ".wav")
        files = []

        if not os.path.exists(self.music_folder):
            print("Music folder not found")
            return files

        for file in os.listdir(self.music_folder):
            if file.lower().endswith(formats):
                files.append(os.path.join(self.music_folder, file))

        files.sort()
        return files

    def get_current_track(self):
        if not self.playlist:
            return None
        return self.playlist[self.current_index]

    def play(self):
        if not self.playlist:
            print("No music files found")
            return

        track = self.get_current_track()

        try:
            pygame.mixer.music.load(track)
            pygame.mixer.music.play()
            print("Playing:", os.path.basename(track))
        except Exception as e:
            print("ERROR:", e)

    def stop(self):
        pygame.mixer.music.stop()
        print("Stopped")

    def next(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def previous(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    # ⏱️ NEW FUNCTION (IMPORTANT)
    def get_position(self):
        pos_ms = pygame.mixer.music.get_pos()

        if pos_ms == -1:
            return 0

        return pos_ms // 1000  # seconds