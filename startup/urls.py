from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import genesearch.apis
import genesearch.views

# Examples:
# url(r'^$', 'startup.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', genesearch.views.index, name='index'),
    url(r'^api/getGeneNamesStartingWith', genesearch.apis.getGeneNamesStartingWith, name='getGeneNamesStartingWith'),
    url(r'^api/getGenesNamed', genesearch.apis.getGenesNamed, name='getGenesNamed'),
    url(r'^api/', genesearch.apis.noSuchRequest, name='noSuchRequest'),
    url(r'^admin/', include(admin.site.urls)),
]
