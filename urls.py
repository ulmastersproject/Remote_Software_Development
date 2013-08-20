"""
Project Title: Remote Software Development
Author: Santhosh Kumar Balasa Ramnath
Supervisor: Dr. John Nelson
University: University of Limerick
Year: 2012 - 2013
"""

from django.conf.urls.defaults import patterns, include, url
from Remote_Software_Development.Development.views import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Remote_Software.views.home', name='home'),
    # url(r'^Remote_Software/', include('Remote_Software.foo.urls')),

    url(r'^$', Remote_Software_Development),
    url(r'^Remote_Software_Development/$', Remote_Software_Development),
    url(r'^Submitted_Code/$', Submitted_code),
    url(r'^Submitted_Code/Add_to_dropbox/$', Add_to_dropbox),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
