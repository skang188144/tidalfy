import spotipy
import tidalapi
import yaml
import sys
import datetime
import webbrowser

def openSpotifySession(spotifySessionConfig):
    spotipyCredentialsManager = spotipy.SpotifyOAuth(username=spotifySessionConfig['SPOTIPY_USERNAME'], 
                                                     scope='playlist-read-private',
                                                     client_id=spotifySessionConfig['SPOTIPY_CLIENT_ID'], 
                                                     client_secret=spotifySessionConfig['SPOTIPY_CLIENT_SECRET'], 
                                                     redirect_uri=spotifySessionConfig['SPOTIPY_REDIRECT_URI'])
    
    try:
        spotipyCredentialsManager.get_access_token(as_dict=False)
    except spotipy.SpotifyOauthError:
        sys.exit("ERROR: There was a problem gaining Spotify authorization with your provided credentials. Please check your config file.")

    return spotipy.Spotify(oauth_manager=spotipyCredentialsManager)

def openTidalSession(tidalSessionConfig):
    tidalConfig = tidalapi.Config(quality=tidalapi.Quality.master, video_quality=tidalapi.VideoQuality.high)
    tidalSession = tidalapi.Session(tidalConfig)

    tidalTokenType = tidalSessionConfig['TIDAL_TOKEN_TYPE']
    tidalAccessToken = tidalSessionConfig['TIDAL_ACCESS_TOKEN']
    tidalRefreshToken = tidalSessionConfig['TIDAL_REFRESH_TOKEN']
    tidalTokenExpiryTime = tidalSessionConfig['TIDAL_TOKEN_EXPIRY_TIME']

    if tidalTokenType and tidalAccessToken and tidalRefreshToken and tidalTokenExpiryTime:
        try:
            if tidalSession.load_oauth_session(token_type=tidalTokenType, 
                                               access_token=tidalAccessToken,
                                               refresh_token=tidalRefreshToken,
                                               expiry_time=datetime.datetime.strptime(tidalTokenExpiryTime, "%m/%d/%Y, %H:%M:%S")):
                return tidalSession
        except Exception as exception:
            print("ERROR: There was a problem gaining TIDAL authorization with your previous credentials. Please check your config file. \n" + str(exception))    
    else:
        tidalLogin, tidalLoginFuture = tidalSession.login_oauth()
        print('PROMPT: Please login with your web browser: ' + tidalLogin.verification_uri_complete)
        tidalLoginUri = tidalLogin.verification_uri_complete
        webbrowser.open(tidalLoginUri)
        tidalLoginFuture.result()

    tidalSession.token_refresh(tidalSession.refresh_token)

    with open('tidal_session_config.yml', 'w') as tidalSessionFile:
        yaml.dump({'TIDAL_TOKEN_TYPE': tidalSession.token_type,
                   'TIDAL_ACCESS_TOKEN': tidalSession.access_token,
                   'TIDAL_REFRESH_TOKEN': tidalSession.refresh_token,
                   'TIDAL_TOKEN_EXPIRY_TIME': tidalSession.expiry_time}, tidalSessionFile)
    
    return tidalSession