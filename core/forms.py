from django import forms

class SearchForm(forms.Form):
    origin = forms.CharField(required=True)
    destination = forms.CharField(required=True)
    travel_date = forms.CharField()


class ManageTicketForm(forms.Form):
    reference = forms.CharField(required=True)
    countrycode = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
