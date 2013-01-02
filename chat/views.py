# Create your views here.
from django.views.generic import FormView
from django import forms, http

import pusher


class MessageForm(forms.Form):
    RED, BLUE, YELLOW = map(str, range(3))
    CHATROOMS = (
        (RED, 'Red'),
        (BLUE, 'Blue'),
        (YELLOW, 'Yellow')
    )
    name = forms.CharField(widget=forms.HiddenInput)
    message = forms.CharField()
    chatroom = forms.ChoiceField(choices=CHATROOMS)


class MessageCreateView(FormView):
    form_class = MessageForm

    template_name = 'index.html'

    def form_valid(self, form):
        message = form.cleaned_data.get('message')
        chatroom = form.cleaned_data.get('chatroom')
        name = form.cleaned_data.get('name')
        p = pusher.pusher_from_url()
        if p[chatroom].trigger('new-message', {'id': '1', 'name': name, 'message': message}):
            return http.HttpResponse('Ok')
        return self.form_invalid(form=form)

    def form_invalid(self, form):
        return http.HttpResponse('Error')

    def get_initial(self):
        return {
            'name': 'Anonym'
        }
