from django.conf.urls import patterns, include, url

import JobsWeb.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'JobsProject.views.home', name='home'),
    # url(r'^JobsProject/', include('JobsProject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tools/', JobsWeb.views.tools),
    url(r'^logger', JobsWeb.views.logger),
    url(r'^actioncenter/', JobsWeb.views.actioncenter),
    url(r'^job/new/', JobsWeb.views.jobnew),
    url(r'^job/view/', JobsWeb.views.jobview),
    url(r'^job/edit/', JobsWeb.views.jobedit),
    url(r'^joblist/', JobsWeb.views.joblist),
    url(r'^alert/', JobsWeb.views.alert),
    url(r'.*', JobsWeb.views.home),
)
