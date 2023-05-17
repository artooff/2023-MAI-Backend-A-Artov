# Create your views here.

from django.http import JsonResponse
from django.views import View
from musicService.models import Song, Album, Artist

import json


class SongsView(View):
    def get(self, request):
        songs = Song.objects.all()
        data = [
            {
                'id': song.id,
                'title' : song.title,
                'artist': song.artist.name,
                'album': song.album.title
            } for song in songs]
        return JsonResponse(data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        artist_name = data.get('artist')
        album_title = data.get('album')
        release_date = data.get('releaseDate')
        try:
            artist, _ = Artist.objects.get_or_create(name=artist_name)
            album, _ = Album.objects.get_or_create(title=album_title, artist=artist)
            song = Song.objects.create(title=data.get('title'), artist=artist, album=album, releaseDate=release_date)
            data = {
                'id': song.id,
                'title': song.title,
                'album': {
                    'id': song.album.id,
                    'title': song.album.title
                },
                'artist': {
                    'id': song.artist.id,
                    'name': song.artist.name
                },
                'releaseDate': song.releaseDate
            }
            return JsonResponse(data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Invalid request method'}, status=405)


class SongInfoView(View):
    def get(self, request, song_id):
        try:
            song = Song.objects.get(id=song_id)
            data = {
                'id': song.id,
                'title': song.title,
                'artist': {
                    'id': song.artist.id,
                    'name': song.artist.name
                },
                'album': {
                    'id': song.album.id,
                    'title': song.album.title
                },
                'releaseDate': song.releaseDate
            }
            return JsonResponse(data)
        except Song.DoesNotExist:
            return JsonResponse({'error': f'Song with id {song_id} does not exist'}, status=404)

    def put(self, request, song_id):
        try:
            song = Song.objects.get(id=song_id)
            data = json.loads(request.body)
            song.title = data.get('title', song.title)
            artist_name = data.get('artist', song.artist.name)
            try:
                artist = Artist.objects.get(name=artist_name)
            except Artist.DoesNotExist:
                artist = Artist.objects.create(name=artist_name, listenersCount=0)
            song.artist = artist
            album_title = data.get('album', song.album.title)
            try:
                album = Album.objects.get(title=album_title, artist=artist)
            except Album.DoesNotExist:
                album = Album.objects.create(title=album_title, year=0, songsCount=0, artist=artist)
            song.album = album
            song.releaseDate = data.get('releaseDate', song.releaseDate)
            song.save()
            updated_data = {
                'id': song.id,
                'title': song.title,
                'artist': {
                    'id': song.artist.id,
                    'name': song.artist.name
                },
                'album': {
                    'id': song.album.id,
                    'title': song.album.title
                },
                'releaseDate': song.releaseDate
            }
            return JsonResponse(updated_data)
        except Song.DoesNotExist:
            return JsonResponse({'error': f'Song with id {song_id} does not exist'}, status=404)

    def delete(self, request, song_id):
        try:
            song = Song.objects.get(id=song_id)
            song.delete()
            data = {'message': f'Successfully deleted song with id {song_id}.'}
            return JsonResponse(data)
        except Song.DoesNotExist:
            return JsonResponse({'error': f'Song with id {song_id} does not exist'}, status=404)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Invalid request method'}, status=405)

class SongSearchView(View):
    def get(self, request):
        artist = request.GET.get('artist')
        album = request.GET.get('album')

        if artist and album:
            songs = Song.objects.filter(artist__name=artist, album__title=album)
        elif artist:
            songs = Song.objects.filter(artist__name=artist)
        elif album:
            songs = Song.objects.filter(album__title=album)
        else:
            songs = Song.objects.all()

        results = {
            'count': songs.count(),
            'results': [
                {
                    'id': song.id,
                    'title': song.title,
                    'artist': song.artist.name,
                    'album': song.album.title,
                    'releaseDate': song.releaseDate.strftime('%Y-%m-%d')  # Форматируем дату в строку
                } for song in songs
            ]
        }
        return JsonResponse(results)



class ArtistsView(View):
    def get(self, request):
        artists = Artist.objects.all()
        data = [
            {
                'id': artist.id,
                'name': artist.name,
            } for artist in artists]
        return JsonResponse(data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        artist_name = data.get('name')
        try:
            artist = Artist.objects.create(name=artist_name)
            data = {
                'id': artist.id,
                'name': artist.name,
            }
            return JsonResponse(data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Invalid request method'}, status=405)


class ArtistInfoView(View):
    def get(self, request, artist_id):
        try:
            artist = Artist.objects.get(id=artist_id)
            songs = Song.objects.filter(artist=artist)
            albums = Album.objects.filter(artist=artist)
            data = {
                'id': artist.id,
                'name': artist.name,
                'albums': [
                    {
                        'id': album.id,
                        'title': album.title,
                        'songs': [song.title for song in album.song_set.all()]
                    } for album in albums
                ]
            }
            return JsonResponse(data)
        except Artist.DoesNotExist:
            return JsonResponse({'error': f'Artist with id {artist_id} does not exist'}, status=404)
    def put(self, request, artist_id):
        try:
            artist = Artist.objects.get(id=artist_id)
        except Artist.DoesNotExist:
            return JsonResponse({'error': f'Artist with id {artist_id} does not exist'}, status=404)

        data = json.loads(request.body)
        artist.name = data.get('name', artist.name)
        artist.save()

        return JsonResponse({'id': artist.id, 'name': artist.name})

    def delete(self, request, artist_id):
        try:
            artist = Artist.objects.get(id=artist_id)
            artist.delete()
            return JsonResponse({'message': f'Artist with id {artist_id} has been deleted successfully'})
        except Artist.DoesNotExist:
            return JsonResponse({'error': f'Artist with id {artist_id} does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Invalid request method'}, status=405)


class AlbumsView(View):
    def get(self, request):
        albums = Album.objects.all()
        data = [
            {
                'id': album.id,
                'title': album.title,
                'artist': album.artist.name,
                'year': album.year,
                'songsCount': album.songsCount
                #'songs': [song.title for song in album.song_set.all()]
            } for album in albums]
        return JsonResponse(data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        artist_name = data.get('artist')
        title = data.get('title')
        try:
            artist, _ = Artist.objects.get_or_create(name=artist_name)
            album = Album.objects.create(title=title, artist=artist)
            data = {
                'id': album.id,
                'title': album.title,
                'artist': {
                    'id': album.artist.id,
                    'name': album.artist.name
                }
            }
            return JsonResponse(data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Invalid request method'}, status=405)


class AlbumInfoView(View):
    def get(self, request, album_id):
        try:
            album = Album.objects.get(id=album_id)
            songs = album.song_set.all()
            data = {
                'id': album.id,
                'title': album.title,
                'artist': {
                    'id': album.artist.id,
                    'name': album.artist.name
                },
                'songs': [song.title for song in songs],
            }
            return JsonResponse(data)
        except Album.DoesNotExist:
            return JsonResponse({'error': f'Album with id {album_id} does not exist'}, status=404)
    def put(self, request, album_id):
        try:
            album = Album.objects.get(id=album_id)
            data = json.loads(request.body)
            artist_name = data.get('artist', album.artist.name)
            album_title = data.get('title', album.title)
            album.artist, _ = Artist.objects.get_or_create(name=artist_name)
            album.title = album_title
            album.save()
            response_data = {
                'id': album.id,
                'title': album.title,
                'artist': {
                    'id': album.artist.id,
                    'name': album.artist.name
                },
                'songs': [song.title for song in album.song_set.all()]
            }
            return JsonResponse(response_data)
        except Album.DoesNotExist:
            return JsonResponse({'error': f'Album with id {album_id} does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, album_id):
        try:
            album = Album.objects.get(id=album_id)
            album.delete()
            return JsonResponse({'message': f'Album with id {album_id} has been deleted.'})
        except Album.DoesNotExist:
            return JsonResponse({'error': f'Album with id {album_id} does not exist.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Invalid request method'}, status=405)

