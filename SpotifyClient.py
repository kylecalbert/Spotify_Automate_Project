
import requests

class Spotify():
    from secrets import spotify_token
    import requests
    # With this method, the artist and the song name will be passed in
    def get_spotify_uri(self, track, artist):
        """Search For the Song"""

        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            track,  # This is basically the string that is needed to search for the tracks for a specific artist
            artist
        )
        response = requests.get(  # to search for a song we need a get request
            query,
            headers={
                # we parse in headers of the type we wan...so we specift we want a JSON. We also need auth header, which will contain our token
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()  # this allows us to get the reponse as a JSON object we can work wtih
        songs = response_json['tracks']['items']  # we will get a list of tracks from spotify not just one from the query and we will select the first one
        if songs:
            return songs[0]['uri']

        else:
            raise Exception("no song found")

    def get_spotify_playlists(self):
        query = "https://api.spotify.com/v1/users/{}/playlists".format("tnip6kiwc75fa967fi5cgenwu")
        response = requests.get(
            query,
            headers={
                # we parse in headers of the type we wan...so we specift we want a JSON. We also need auth header, which will contain our token
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()['items']
        spotify_user_playlists = {}
        for data in response_json:
            id = data['id']
            name = data['name']
            spotify_user_playlists[name] = id

        return spotify_user_playlists

    # The put playlist name and id in a dictionary and when the user types the name, that specific playlist id will be chosen



