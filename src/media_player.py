from vlc import Instance, Media, State

class MediaPlayer:
    def __init__(self, video_path, fullscreen=False):
        # Initialize player
        self.player = Instance('--file-caching=10000 --fullscreen').media_player_new()
        # Initialize media
        self.media = Media(video_path)
        # Set the player's full screen mode
        self.player.set_fullscreen(fullscreen)
        # Set the player's volume
        self.player.audio_set_volume(100)

    def start(self):
        self.player.set_media(self.media)
        self.player.play()
    
    def stop(self):
        self.player.stop()

    def pause(self):
        self.player.set_pause(1)

    def resume(self):
        self.player.set_pause(0)
    
    def is_video_ended(self):
        return self.player.get_state() == State.Ended
