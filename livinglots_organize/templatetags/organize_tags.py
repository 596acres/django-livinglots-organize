"""
Template tags for the organize app, loosely based on django.contrib.comments.

"""
from django import template

from livinglots import get_organizer_model
from livinglots_generictags.tags import (GetGenericRelationList,
                                         RenderGenericRelationList,
                                         GetGenericRelationCount)

register = template.Library()


class RenderOrganizerList(RenderGenericRelationList):
    model = get_organizer_model()

register.tag(RenderOrganizerList)


class GetOrganizerList(GetGenericRelationList):
    model = get_organizer_model()

register.tag(GetOrganizerList)


class GetOrganizerCount(GetGenericRelationCount):
    model = get_organizer_model()

register.tag(GetOrganizerCount)
