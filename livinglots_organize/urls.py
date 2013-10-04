from django.conf.urls.defaults import patterns, url

from livinglots import get_organizer_model

from .views import (AddParticipantSuccessView, DeleteOrganizerView,
                    EditLotParicipantView)


urlpatterns = patterns('',

    url(r'^(?P<object_pk>\d+)/(?P<hash>[^/]{30,})/success/$',
        AddParticipantSuccessView.as_view(
            model=get_organizer_model(),
        ),
        name='add_organizer_success'),

    url(r'^organize/(?P<hash>[^/]{30,})/edit/$',
        EditLotParicipantView.as_view(),
        name='edit_participant'),

    url(r'^organizers/delete/(?P<pk>\d+)/$', DeleteOrganizerView.as_view(),
        name='delete_organizer'),

)
