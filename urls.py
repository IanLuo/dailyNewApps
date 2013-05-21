from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$',views.home),
     url(r'^ios/+$', views.get_new_apps),
     url(r'^ios/appdetail/(?P<app_id>\d*)$',views.get_app_detail),
     url(r'^ios/applist/(?P<list_type>\w*)/(?P<genre>\w*)$',views.get_app_list),
    # url(r'^jaguar/', include('jaguar.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
