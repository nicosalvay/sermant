from django import forms

class SearchProductoForm(forms.Form):
    querycom = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'size': 32,
            'class': 'form-control',
            'placeholder': 'Buscar producto'
        })
    )

    def __init__(self, *args, **kwargs):
        super(SearchProductoForm, self).__init__(*args, **kwargs)
