from django import forms

class HomeForm(forms.Form):
	query=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'placeholder':'Suggest some..'}))