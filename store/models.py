from django.db import models

# Create your models here.

# ARTISTS = {
#     'francis-cabrel': {'name': 'Francis Cabrel'},
#     'lej': {'name': 'Elijay'},
#     'rosana': {'name': 'Rosana'},
#     'maria-dolores-pradera': {'name': 'María Dolores Pradera'},
#     'walidos': {'name': 'Walid KEKHIA'}
# }


# ALBUMS = [
#     {'name': 'Sarbacane', 'artists': [ARTISTS['francis-cabrel']]},
#     {'name': 'La Dalle', 'artists': [ARTISTS['lej'], ARTISTS['walidos']]},
#     {'name': 'Luna Nueva', 'artists': [ARTISTS['rosana'], ARTISTS['maria-dolores-pradera'], ARTISTS['walidos']]}
# ]

class Artist(models.Model):
    name = models.CharField('Nom', max_length=200, unique=True) ## Nom sera affiché dans le parti admin

    class Meta:
        verbose_name = "artiste"  # le nom qui sera affiche dans le parti admin

    def __str__(self):
        return self.name

class Contact(models.Model):
    email = models.EmailField('Email', max_length=100)
    name = models.CharField('Nom', max_length=200)

    class Meta:
        verbose_name = "prospect"

    def __str__(self):
        return self.name

class Album(models.Model):
    reference = models.IntegerField('Référence', null=True)
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    available = models.BooleanField('Disponible', default=True)
    title = models.CharField('Titre',max_length=200)
    picture = models.URLField("URL de l'image",)
    # realtion n à n (1 artist peut faire n Album et 1 Album peut être fait par n Artist)
    # related_name pour la relation inverse qaund nous voulons savoir tous les ablums faites par un artist
    artists = models.ManyToManyField(Artist, related_name='albums', blank=True)

    class Meta:
        verbose_name = "disque"

    def __str__(self):
        return self.title

class Booking(models.Model):
    created_at = models.DateTimeField("Date d'envoi", auto_now_add=True)
    contacted = models.BooleanField('Demande traitée ?', default=False)
    # relation 1 à n (1 Contact peut avoir plusieurs Booking, par contre un Booking n'appartient qu'un seul Contact)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE,)
    # relation 1 à 1 (1 Album peut être réservé une seule fois, et une réservation peut voir la même album qu'une seule fois)
    album = models.OneToOneField(Album, on_delete=models.CASCADE,)

    class Meta:
        verbose_name = "Réservation"

    def __str__(self):
        return self.contact.name