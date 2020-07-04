from YoutubeClient import Youtube, Spotify
from exceptions import ResponseException
import requests
import json

#This is a spotify project which automatically adds a users songs from their youtube playlist
#to a spotify playlist of thier choice


class userChoice():
    from secrets import spotify_token

    youtube_client_obj  = Youtube()
    spotify_client_obj = Spotify()

#This method allows the user to enter the youtube playlist they want to export from
#The playlist name and id are put in a dictionary and if the user enters the playlist name the id will be returned
#The playlist id will then be used to retrieve the songs from that specific playlist which will then be returned
    def youtube_playlist_choice(self):

        youtube_playlist_id = ""
        youtube_playlists = self.youtube_client_obj.get_playlists()
        print("Below are the youtube playlists:")
        for keys in youtube_playlists.keys():
            print(keys)
        user_playlist_choice = input("Please enter the youtube playlist you want to add from:")
        if (youtube_playlists.get(user_playlist_choice)):
            youtube_playlist_id = youtube_playlists.get(user_playlist_choice)
        playlist_songs = self.youtube_client_obj.get_videos_from_playlist(youtube_playlist_id)
        return playlist_songs

#Similarly to above this method retrieves the playlist ID of the users chosen spotify playlist
    def spotify_playlist_choice(self):
        spotify_playlist_id = ""
        spotify_playlists = self.spotify_client_obj.get_spotify_playlists()
        print("Below are the spotify playlists:")

        for keys in spotify_playlists.keys():
            print(keys)
        user_playlist_choice = input("Please enter the spotify playlist you want to add to:")
        if (spotify_playlists.get(user_playlist_choice)):
            spotify_playlist_id = spotify_playlists.get(user_playlist_choice)
        return spotify_playlist_id


#As we have the spotify playlist id and the songs, we can then add the songs to that specific playlist
    def add_songs_to_spotify(self):
        songs = self.youtube_playlist_choice()
        spotify_playlist_id = self.spotify_playlist_choice()
        request_data = json.dumps(songs)
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            spotify_playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

        # check for valid response status
        if response.status_code != 200:
            raise ResponseException(response.status_code)

        response_json = response.json()
        return response_json



#This will run the program
main = userChoice()
main.add_songs_to_spotify()

