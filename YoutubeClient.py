import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl
from SpotifyClient import Spotify


class Youtube:
    def __init__(self):
        self.youtube_client = self.get_youtube_client()

    def get_youtube_client(self):
        """ Log Into Youtube, Copied from Youtube Data API """
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "/Users/macbook/PycharmProjects/SpotifyProject/client_secret.json" #you will have to download your own youtube client_secret

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client


#This method returns all of the users playlists in the form of a dictionary: the name and the id of the playlsit
    def get_playlists(self):

        request = self.youtube_client.playlists().list(
            part="id, snippet",
            maxResults=50,
            mine = True
        )
        response = request.execute()

        playlists  = {}
        for item in response['items']:
            id = item['id']
            title = item['snippet']['title']
            playlists[title] = id


        return playlists




    #This method gets the video from the playlist and calls the get artist/track method to extract the artist and song name
    #afer doing so this method can then get the spotify uri thats needed to export the songs into our spotfiy playlist
    def get_videos_from_playlist(self, playlist_id):

        songs_uri = []
        request = self.youtube_client.playlistItems().list(
            playlistId=playlist_id,
            part="id, snippet",
            maxResults=50
        )
        response = request.execute()
        Spotify_class = Spotify()
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']

            artist,track = self.get_artist_and_track_from_video(video_id)
            if artist and track:
                uri = Spotify_class.get_spotify_uri(track,artist)
                songs_uri.append(uri)

        return songs_uri      #The array of uris are then returned


    #This method gets the artist and the track name from the video
    def get_artist_and_track_from_video(self, video_id):
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"

        video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(
            youtube_url, download=False  # TO PREVENT YOUTUBE DL FROM DOWNLOADING THE VIDEO
        )
        artist = video['artist']
        track = video['track']


        return artist,track  #Python can return two obejects