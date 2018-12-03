from django.conf.urls import url

from . import views # import views so we use them in urls

app_name = 'store'

urlpatterns = [
    # url(r'^$', views.index),    # "store/" will call the method "index" in "views.py"
    url(r'^$', views.listing, name="listing"),    # "store/" will call the method "listing" in "views.py"
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name="detail"),    # "store/" will call the method "detail" in "views.py"
    url(r'^search/$', views.search, name="search"),    # "store/" will call the method "search" in "views.py"
    url(r'^doviz/$', views.doviz, name="doviz"),    # "store/" will call the method "doviz" in "views.py"
]