from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError
import os
import json

# from .models import ALBUMS        # This data exist in models.py
from .models import Album, Artist, Contact, Booking
from .forms import ContactForm, ParagraphErrorList

def index(request):    
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]  # -created_at c'est ordre inverse   
    context = {
        'albums': albums,
    }
    return render(request, 'store/index.html', context)

def listing(request):
    page = request.GET.get("page")
    albums_list = Album.objects.filter(available=True)
    paginator = Paginator(albums_list, 9)
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        albums = paginator.page(paginator.num_pages)
    context = {
        'albums': albums,
        'paginate': True
    }    
    return render(request, 'store/listing.html', context)

# @transaction.atomic  un exemple d'utilistion de transaction pour l'ensemble des requêtes dans la fonction
def detail(request, album_id):
    # album = Album.objects.get(pk=album_id)
    album = get_object_or_404(Album, pk=album_id)
    artists_name = ", ".join([artist.name for artist in album.artists.all()])
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture,
    } 
    if request.method == 'POST':
        form = ContactForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            try:
                with transaction.atomic():
                    contact = Contact.objects.filter(email=email)       # retourne un objet de type QuerySet
                    if not contact.exists():
                        # If a contact is not registered, create a new one.
                        contact = Contact.objects.create(
                            email=email,
                            name=name
                        )
                    else:
                        contact = contact.first()  # parce que à ce stade contact est un QuerySet
                    # If no album matches the id, it means the form must have been tweaked
                    # so returning a 404 is the best solution.
                    album = get_object_or_404(Album, id=album_id)
                    booking = Booking.objects.create(
                        contact=contact,
                        album=album
                    )

                    # Make sure no one can book the album again.
                    album.available = False
                    album.save()
                    context = {
                        'album_title': album.title
                    }
                    return render(request, 'store/merci.html', context)
            except IntegrityError:
                form.errors['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requête."
    else:   
        form = ContactForm()

    context['form'] = form
    context['errors'] = form.errors.items()
    return render(request, 'store/detail.html', context)

def search(request):
    # obj = str(request.GET)
    # query = request.GET['query']
    # message = "propriété GET : {} et requête : {}".format(obj, query)
    # return HttpResponse(message)

    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)     # le titre contient le query icontains insensible à la case

        if not albums.exists():
            # la requete va chercher dans la table Artist dont le nom contient query et elle retourne une objet de type Album
            albums = Album.objects.filter(artists__name__icontains=query)  

    title = "Résultats pour la requête %s "%query
    context = {
        'albums': albums,
        'title': title
    }    
    return render(request, 'store/search.html', context)

def doviz(request):
    # os.system('heroku run rm -f store/static/store/json/doviz.json')
    # os.system('heroku run scrapy runspider store/doviz.py -o store/static/store/json/doviz.json')
    os.system('scrapy runspider -t json store/doviz.py -o - > store/static/store/json/doviz.json')

    with open('store/static/store/json/doviz.json') as f:
        dataDoviz = json.load(f)
        prixDoviz = round(float(dataDoviz[0]["prixdoviz"].replace(',', '.')), 5)
        prixKuveyt = round(float(dataDoviz[0]["prixkuveyt"].replace(',', '.')), 5)
    
    context = {
        # 'total_base_euro': "{:,.{}f}".format(235250, 2).replace(',', ' '),
        # 'total_base_euro': format(235250, ',.2f').replace(',', ' '),
        'total_base_euro': 235250,
        'total_base_tl': 1396341.34,

        # 'prixEuro': format(prixKuveyt, ',.4f').replace(',', ' '),
        'prixEuro': prixKuveyt, 
        'total_new_kuveyt': 1396341.34/prixKuveyt,
        'finalRes_kuveyt': 1396341.34/prixKuveyt - 235250,
        
        'prixDoviz': prixDoviz,
        'total_new_doviz': 1396341.34/prixDoviz, 
        'finalRes_doviz': 1396341.34/prixDoviz - 235250,
    }
    return render(request, 'store/doviz.html', context)
