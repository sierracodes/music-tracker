"""
forms.py

Module for holding custom forms for the tracker application.

"""

from django import forms

from .models import Listen

class ListenForm(forms.ModelForm):

    class Meta:
        model = Listen
        fields = ['album', 'listen_date']


class ListenFormForAlbum(ListenForm):

    def __init__(self, *args, **kwargs):
        super(ListenFormForAlbum, self).__init__(*args, **kwargs)

        self.fields['album'].widget = forms.widgets.HiddenInput()
