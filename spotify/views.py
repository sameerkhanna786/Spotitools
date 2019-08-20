from .forms import SettingsForm
from django.shortcuts import render, HttpResponseRedirect
import spotipy
import spotipy.util as util
from spotipy import oauth2
from goto import with_goto
from random import shuffle

scopes = 'user-library-read user-library-modify playlist-modify playlist-read'
client_id = "67a37b00fbf4468883cb05a3aca70bf7"
client_secret = "912a5788339f4866949102dcd5b38acf"
redirect_uri='http://127.0.0.1:8000/spotify/after-sign-in/'
sp_oauth = oauth2.SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scopes)
sp = spotipy.Spotify()
is_authenticated = False
context = {}
allSongs = []
listGen = False
form = SettingsForm()

@with_goto
def generate_song_list():
    global listGen
    global sp
    global context
    global allSongs
    if listGen:
        return
    listGen = True
    results = sp.current_user_saved_tracks()
    context = {
        'results': [],
        'title': 'Songs',
        'show': True,
    }
    label .begin
    for track in results['items']:
        item = track['track']
        dic = {}
        dic['album'] = item['album']['name']
        dic['image'] = item['album']['images'][0]['url']
        dic['name'] = item['name']
        dic['duration'] = item['duration_ms']
        dic['explicit'] = item['explicit']
        dic['popularity'] = item['popularity']

        artists = ""
        for i in range(0, len(item['artists'])):
            if i != len(item['artists']) - 1:
                artists = artists + item['artists'][i]['name'] + ", "
            else:
                artists = artists + item['artists'][i]['name']
        dic['artists'] = artists

        features = sp.audio_features([item['id']])[0]
        for key in features.keys():
            dic[key] = features[key]

        allSongs.append(dic)
    """
    while results['next']:
        results = sp.next(results)
        goto .begin
    """
    context['results'] = allSongs
    return context

def remove(lst, key, minVal, maxVal):
    if minVal:
        lst = [song for song in lst if song[key] >= minVal]
    if maxVal:
        lst = [song for song in lst if song[key] <= maxVal]
    return lst

def filter(
    explicit, clean, 
    minPop, maxPop, 
    minDur, maxDur, 
    minE, maxE,
    minAcousticness, maxAcousticness,
    minDanceability, maxDanceability,
    minInstrumentalness, maxInstrumentalness,
    minLiveness, maxLiveness,
    minLoudness, maxLoudness,
    minSpeechiness, maxSpeechiness,
    minValence, maxValence,
    minTempo, maxTempo,
    randomize,
    playlist_name
    ):
    global allSongs
    global context
    global sp
    lst = []
    for song in allSongs:
        if explicit and song['explicit'] == True:
            lst.append(song)
        elif clean and song['explicit'] == False:
            lst.append(song)
    lst = remove(lst, 'popularity', minPop, maxPop)
    lst = remove(lst, 'duration', minDur, maxDur)
    lst = remove(lst, 'energy', minE, maxE)
    lst = remove(lst, 'acousticness', minAcousticness, maxAcousticness)
    lst = remove(lst, 'danceability', minDanceability, maxDanceability)
    lst = remove(lst, 'instrumentalness', minInstrumentalness, maxInstrumentalness)
    lst = remove(lst, 'liveness', minLiveness, maxLiveness)
    lst = remove(lst, 'loudness', minLoudness, maxLoudness)
    lst = remove(lst, 'speechiness', minSpeechiness, maxSpeechiness)
    lst = remove(lst, 'valence', minValence, maxValence)
    lst = remove(lst, 'tempo', minTempo, maxTempo)

    if randomize:
        shuffle(lst)

    if playlist_name:
        username = sp.me()['id']

        def get_playlist(sp, u_name, p_name):
            playLists = sp.user_playlists(u_name)
            for l in playLists['items']:
                if l['name'] == p_name:
                    return l['id']
            print(p_name + " not found; creating playlist.")
            sp.trace = False
            return sp.user_playlist_create(u_name, p_name)['id']

        def add_tracks(sp, u_name, p_name, trackIds):
            Id = get_playlist(sp, u_name, p_name)
            for i in range(0, len(trackIds), 99):
                lst = trackIds[i:i+99]
                res = sp.user_playlist_add_tracks(u_name, Id, lst)

        tracks = []
        for song in lst:
            tracks.append(song['id'])

        add_tracks(sp, username, playlist_name, tracks)

    context['results'] = lst

def start(request):
    return render(request, 'spotify/start.html', {})

def show_albums(request):
    return render(request, 'spotify/start.html', {})

def form(request):
    global form
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SettingsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            context['show'] = form.cleaned_data['show_albums']
            filter(
                form.cleaned_data['explicit'], form.cleaned_data['clean'], 
                form.cleaned_data['minPop'], form.cleaned_data['maxPop'],
                form.cleaned_data['minDur'], form.cleaned_data['maxDur'],
                form.cleaned_data['minE'], form.cleaned_data['maxE'],
                form.cleaned_data['minAcousticness'], form.cleaned_data['maxAcousticness'],
                form.cleaned_data['minDanceability'], form.cleaned_data['maxDanceability'],
                form.cleaned_data['minInstrumentalness'], form.cleaned_data['maxInstrumentalness'],
                form.cleaned_data['minLiveness'], form.cleaned_data['maxLiveness'],
                form.cleaned_data['minLoudness'], form.cleaned_data['maxLoudness'],
                form.cleaned_data['minSpeechiness'], form.cleaned_data['maxSpeechiness'],
                form.cleaned_data['minValence'], form.cleaned_data['maxValence'],
                form.cleaned_data['minTempo'], form.cleaned_data['maxTempo'],
                form.cleaned_data['randomize'],
                form.cleaned_data['playlist_name']
                )

    return HttpResponseRedirect('/spotify/')

def home(request):
    global sp
    global context
    global listGen
    global is_authenticated
    global form
    if not is_authenticated:
        return sign_in(request)
    if not listGen:
        generate_song_list()
        return home(request)
    context['form'] = form
    return render(request, 'spotify/home.html', context)

def sign_in(request):
    global is_authenticated
    global sp
    if is_authenticated:
        return home(request)
    sp_oauth = oauth2.SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scopes)
    token_info = sp_oauth.get_cached_token() 
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        return HttpResponseRedirect(auth_url)
    sp = spotipy.Spotify(auth=token)
    is_authenticated = True
    return home(request)


def after_sign_in(request):
    global is_authenticated
    global sp
    results = {}
    token = 'http://127.0.0.1:8000/spotify/after-sign-in/?{}'.format(request.GET.urlencode())
    code = sp_oauth.parse_response_code(token)
    token_info = sp_oauth.get_access_token(code)
    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        is_authenticated = True
    return HttpResponseRedirect('/spotify/')

