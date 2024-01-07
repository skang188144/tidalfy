import yaml
import auth
import tidalapi

def readConfigFile(configFilePath: str):
    with open(configFilePath, 'r') as configFile:
        config = yaml.safe_load(configFile)
    return config

def readSessionFile(sessionFilePath: str):
    with open(sessionFilePath, 'r') as sessionFile:
        session = yaml.safe_load(sessionFile)
    return session

def getTracksFromPlaylist(spotifySession, playlistUri):
    tracks = spotifySession.playlist_tracks(playlist_id=playlistUri, fields='items')['items']
    return [track['track'] for track in tracks]

def transferDailyMixes(spotifySession, spotifyConfig, tidalSession, tidalConfig):
    for sourcePlaylistUriTag in spotifyConfig['daily_mixes']:
        sourcePlaylistUri = spotifyConfig['daily_mixes'][sourcePlaylistUriTag]

        if sourcePlaylistUri:
            dailyMixNumber = sourcePlaylistUriTag.strip("SPOTIPY_DAILY_MIX_").strip("_PLAYLIST_URI")
            destinationPlaylistName = "Daily Mix " + dailyMixNumber

            for tidalPlaylist in tidalSession.user.playlists():
                if tidalPlaylist.name == destinationPlaylistName:
                    tidalPlaylist.delete()

            destinationPlaylist = tidalSession.user.create_playlist("Daily Mix " + dailyMixNumber, "")

            for sourceTrack in getTracksFromPlaylist(spotifySession, sourcePlaylistUri):
                searchTrack = tidalSession.search(sourceTrack['name'] + ' ' + sourceTrack['album']['artists'][0]['name'], models=[tidalapi.media.Track])['top_hit']

                if searchTrack:
                    destinationPlaylist.add([searchTrack.id])

spotifySessionConfig = readConfigFile('spotify_session_config.yml')
tidalSessionConfig = readSessionFile('tidal_session_config.yml')

spotifySession = auth.openSpotifySession(spotifySessionConfig)
tidalSession = auth.openTidalSession(tidalSessionConfig)

transferDailyMixes(spotifySession, spotifySessionConfig, tidalSession, tidalSessionConfig)