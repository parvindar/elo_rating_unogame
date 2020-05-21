from django import forms

class scoreForm(forms.Form):
    Daddy = forms.DecimalField(label='Daddy')
    Mummy = forms.DecimalField(label='Mummy')
    Parvindar = forms.DecimalField(label='Parvindar')
    Ricky = forms.DecimalField(label='Ricky')