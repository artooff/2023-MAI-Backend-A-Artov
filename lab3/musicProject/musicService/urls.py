from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/songs', views.SongsView.as_view(), name='songs'),
    path('api/songs/<int:song_id>', views.SongInfoView.as_view(), name='song_info'),
    path('api/songs/search/', views.SongSearchView.as_view(), name='song_search'),
    path('api/artists', views.ArtistsView.as_view(), name='artists'),
    path('api/artists/<int:artist_id>', views.ArtistInfoView.as_view(), name='artist_info'),
    path('api/albums', views.AlbumsView.as_view(), name='albums'),
    path('api/albums/<int:album_id>', views.AlbumInfoView.as_view(), name='album_info'),
]
