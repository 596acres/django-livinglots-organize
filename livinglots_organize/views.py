"""
Generic views for editing participants.

"""

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import CreateView, TemplateView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import DeleteView

from livinglots import get_organizer_model
from livinglots_genericviews import AddGenericMixin


class EditParticipantMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        hash = self.get_participant_hash()
        context = super(EditParticipantMixin, self).get_context_data(**kwargs)
        context.update({
            'organizers': get_organizer_model().objects.filter(email_hash__istartswith=hash).order_by('added'),
        })
        return context

    def get_participant_hash(self):
        raise NotImplementedError('Implement get_participant_hash() to use '
                                  'EditParticipantMixin.')


class DeleteParticipantView(DeleteView):

    def get_context_data(self, **kwargs):
        context = super(DeleteParticipantView, self).get_context_data(**kwargs)
        context['target'] = self.object.content_object
        context['next_url'] = self.request.GET.get('next_url')
        return context

    def get_success_url(self):
        messages.info(self.request, self._get_success_message())
        return self.request.POST.get(
            'next_url',
            self.object.content_object.get_absolute_url()
        )

    def _get_success_message(self):
        verb = 'working on'
        if isinstance(self.object, get_organizer_model()):
            verb = 'subscribed to'
        return 'You are no longer %s %s.' % (verb, self.object.content_object)


class DeleteOrganizerView(DeleteParticipantView):
    model = get_organizer_model()
    pk_url_kwarg = 'organizer_pk'
    template_name = 'livinglots/organize/organizer_confirm_delete.html'


class EditLotParicipantView(EditParticipantMixin, TemplateView):
    template_name = 'livinglots/organize/edit_participant.html'

    def get_context_data(self, **kwargs):
        context = super(EditLotParicipantView, self).get_context_data(**kwargs)
        context.update({
            'email': self._get_email(context),
        })
        return context

    def get_participant_hash(self):
        return self.kwargs['hash']

    def _get_email(self, context):
        try:
            return context['organizers'][0].email
        except Exception:
            try:
                return context['watchers'][0].email
            except Exception:
                return None


class ParticipantMixin(object):

    def _get_participant_type(self):
        return self.model._meta.object_name.lower()


class AddParticipantView(AddGenericMixin, ParticipantMixin, CreateView):

    def get_success_url(self):
        kwargs = {
            'object_pk': self.object.pk,
            'hash': self.object.email_hash[:30],
            'pk': self.object.object_id,
        }
        urlname = 'organize:add_%s_success' % self._get_participant_type()
        return reverse(urlname, kwargs=kwargs)

    def get_template_names(self):
        return [
            'livinglots/organize/add_%s.html' % self._get_participant_type(),
        ]


class AddParticipantSuccessView(ParticipantMixin, TemplateView):
    model = get_organizer_model()

    def get_context_data(self, **kwargs):
        context = super(AddParticipantSuccessView, self).get_context_data(**kwargs)
        try:
            context['participant'] = self.model.objects.filter(
                email_hash__istartswith=kwargs['hash'],
                pk=self.kwargs['object_pk'],
            )[0]
        except Exception:
            raise Http404
        return context

    def get_template_names(self):
        return [
            'livinglots/organize/add_%s_success.html' % (
                self._get_participant_type(),
            ),
        ]
