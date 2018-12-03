from django.contrib import admin
from django.utils.safestring import mark_safe
# permet d'obtenir d'une URL à partir d'un nom d'une vue
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

# Les noms de vues de l'interface d'administration porte la forme suivante
# admin:{{ nom_appliaction }}_{{ nom_modèle}}_change
# exemple : admin:store_booking_change

from .models import Booking, Contact, Album, Artist

# ancien mode di'utilisation de base
# admin.site.register(Booking)

class AdminURLMixin(object):
    
    def get_admin_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__) 
        return reverse("admin:store_%s_change" % (content_type.model), args=[obj.id])


# BookingInLine qui herite de la class admin.TabularInLine qui permet d'afficher des informations sur plusieurs lignes
class BookinInline(admin.TabularInline, AdminURLMixin):  
    readonly_fields = ["created_at", "contacted", "album_link"]
    model = Booking
    # les champs à afficher
    fieldsets = [
        (None, {'fields': ['album_link', 'contacted']})
        ]                                               # list columns
    extra = 0                                           # permet d'afficher qu'une seule ligen
    verbose_name = "Réservation"                        # permet de changer le nom dans l'affichage            
    verbose_name_plural = "Réservations"
    
    def has_add_permission(self, request):              # permet d'interdir d'ajouter de nouvelle reservation
        return False
    
    def album_link(self, booking):              # Mixin ajouter des fonctionalités à une classe à partir d'une autre classe
        url = self.get_admin_url(booking.album)
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.album.title))

class AlbumArtistInline(admin.TabularInline):  
    model = Album.artists.through
    extra = 1
    verbose_name = "Disque"
    verbose_name_plural = "Disques"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):    # permet d'affiche des informations concernant sur l'instance mais sur l'objet
    inlines = [BookinInline, ]          # inlines permet d'afficher des informations sur plusieurs lignes

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):   
    inlines = [AlbumArtistInline, ]          

@admin.register(Album)
class ArtistAdmin(admin.ModelAdmin):   
    search_fields = ['reference', 'title']    # l'attribut de classe search_fields permet de faire de recherche sur ces champs    

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin, AdminURLMixin):   
    readonly_fields = ["created_at", "contact_link", "album_link"] 
    fields = ["created_at", "album_link", "contacted"] 
    list_filter = ['created_at', 'contacted']   # l'attribut de classe list_filter permet d'ajouter des filters  sur ces champs    

    def has_add_permission(self, request):
        return False

    def contact_link(self, booking):              # Mixin ajouter des fonctionalités à une classe à partir d'une autre classe
        url = self.get_admin_url(booking.contact)
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.contact.name))

    def album_link(self, booking):              # Mixin ajouter des fonctionalités à une classe à partir d'une autre classe
        url = self.get_admin_url(booking.album)
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.album.title))
    