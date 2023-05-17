from django.db import models


# Create your models here
class Artist(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'artist'


class Album(models.Model):
    title = models.CharField(max_length=50)
    year = models.IntegerField()
    songsCount = models.IntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    class Meta:
        db_table = 'album'


class Song(models.Model):
    title = models.CharField(max_length=50)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    releaseDate = models.DateField()

    class Meta:
        db_table = 'song'