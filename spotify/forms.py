from django import forms
from . models import Settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator


class SettingsForm(forms.Form):
    show_albums = forms.BooleanField(label = 'Show Albums + Parameters', required=False)

    explicit = forms.BooleanField(label = 'Explicit Songs', required=False)
    clean = forms.BooleanField(label = 'Clean Songs', required=False)

    randomize = forms.BooleanField(label = 'Truly Randomize Songs', required=False)

    playlist_name = forms.CharField(label = 'Playlist to save songs', required=False)

    minPop = forms.IntegerField(label = 'Minimum Popularity (0 to 100)', initial = 0, validators=[MinValueValidator(0), MaxValueValidator(100)], required=False)
    maxPop = forms.IntegerField(label = 'Maximum Popularity (0 to 100)', initial = 100, validators=[MinValueValidator(0), MaxValueValidator(100)], required=False)
    
    minDur = forms.IntegerField(label = 'Minimum Duration (>0)', validators=[MinValueValidator(0)], required=False)
    maxDur = forms.IntegerField(label = 'Maximum Duration (>0)', validators=[MinValueValidator(0)], required=False)
    
    minE = forms.FloatField(label = 'Minimum Energy (0.0 to 1.0)', validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)
    maxE = forms.FloatField(label = 'Maximum Energy (0.0 to 1.0)', validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)
    
    minAcousticness = forms.FloatField(label = 'Minimum Acousticness (0.0 to 1.0)', validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)
    maxAcousticness = forms.FloatField(label = 'Maximum Acousticness (0.0 to 1.0)', validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)
    
    minDanceability = forms.FloatField(label = 'Minimum Danceability (0.0 to 1.0)', validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)
    maxDanceability = forms.FloatField(label = 'Maximum Danceability (0.0 to 1.0)', validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)
    
    minInstrumentalness = forms.FloatField(label = 'Minimum Instrumentalness (0.0 to 1.0)', validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)
    maxInstrumentalness = forms.FloatField(label = 'Maximum Instrumentalness (0.0 to 1.0)', validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)
    
    minLiveness = forms.FloatField(label = 'Minimum Liveness (0.0 to 1.0)', validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)
    maxLiveness = forms.FloatField(label = 'Maximum Liveness (0.0 to 1.0)', validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)

    minLoudness = forms.FloatField(label = 'Minimum Loudness (-60.0 to 0.0)', validators=[MinValueValidator(-60.0), MaxValueValidator(0.0)], required=False)
    maxLoudness = forms.FloatField(label = 'Maximum Loudness (-60.0 to 0.0)', validators=[MinValueValidator(-60.0), MaxValueValidator(0.0)], required=False)

    minSpeechiness = forms.FloatField(label = 'Minimum Speechiness (0.0 to 1.0)', validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)
    maxSpeechiness = forms.FloatField(label = 'Maximum Speechiness (0.0 to 1.0)', validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)


    minValence = forms.FloatField(label = 'Minimum Valence (0.0 to 1.0)', validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)
    maxValence = forms.FloatField(label = 'Maximum Valence (0.0 to 1.0)', validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)

    minTempo = forms.FloatField(label = 'Minimum Tempo (>0.0)', validators=[MinValueValidator(0.0)], required=False)
    maxTempo = forms.FloatField(label = 'Maximum Tempo (>0.0)', validators=[MinValueValidator(0.0)], required=False)
    
    
    class Meta:
        model = Settings
        fields = '__all__'