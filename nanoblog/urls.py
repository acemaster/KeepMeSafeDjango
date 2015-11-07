from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nanoblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'authentication.views.index'),
    url(r'^login/', 'authentication.views._login'),
    url(r'^register/', 'authentication.views.register'),
    url(r'^loginuser/', 'authentication.views._loginuser'),
    url(r'^dashboard/', 'authentication.views.dashboard'),
    url(r'^logout/', 'authentication.views._logout'),
    url(r'^updatelatlongt/', 'authentication.views.addLocation'),
    url(r'^safetylist/', 'authentication.views.safetylist'),
    url(r'^getlist/', 'authentication.views.getlist'),
    url(r'^makefriend/', 'authentication.views.makefriend'),
    url(r'^frequests/', 'authentication.views.frequests'),
    url(r'^acceptreq/', 'authentication.views.acceptreq'),
    url(r'^rejectreq/', 'authentication.views.rejectreq'),
    url(r'^aroundme/', 'authentication.views.aroundme'),
    url(r'^iamnotsafe/', 'authentication.views.notsafe'),
    url(r'^getnotification/', 'authentication.views.getnotifications'),
    url(r'^readnotification/', 'authentication.views.readnotification'),
    url(r'^recnotification/', 'authentication.views.recievenotification'),
    url(r'^notifications/', 'authentication.views.notifications'),
    url(r'^checksafe/', 'authentication.views.checksafe'),
    url(r'^getcode/', 'authentication.views.getcode'),
    
)



from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)