from django import forms
from payu.utils import generate_hash

class PayUForm(forms.Form):
    # payu specific fields
    key = forms.CharField(widget = forms.HiddenInput(), )
    hash = forms.CharField(widget = forms.HiddenInput(), required=False)

    # cart order related fields
    txnid = forms.CharField(widget = forms.HiddenInput(), )
    productinfo = forms.CharField(widget = forms.HiddenInput(), )
    amount = forms.IntegerField(widget = forms.HiddenInput(), )

    # buyer details
    firstname = forms.CharField(widget = forms.HiddenInput(), )
    lastname = forms.CharField(widget = forms.HiddenInput(), required=False)
    email = forms.EmailField(widget = forms.HiddenInput(), )
    phone = forms.RegexField(widget = forms.HiddenInput(), regex=r'\d{10}', min_length=10, max_length=10)
    address1 = forms.CharField(widget = forms.HiddenInput(), required=False)
    address2 = forms.CharField(widget = forms.HiddenInput(), required=False)
    city = forms.CharField(widget = forms.HiddenInput(), required=False)
    state = forms.CharField(widget = forms.HiddenInput(), required=False)
    country = forms.CharField(widget = forms.HiddenInput(), required=False)
    zipcode = forms.RegexField(widget = forms.HiddenInput(), regex=r'\d{6}', min_length=6, max_length=6, required=False)
    
    # merchant's side related fields
    furl = forms.URLField(widget = forms.HiddenInput(), )
    surl = forms.URLField(widget = forms.HiddenInput(), )
    curl = forms.URLField(widget = forms.HiddenInput(), required=False)
    codurl = forms.URLField(widget = forms.HiddenInput(), required=False)
    touturl = forms.URLField(widget = forms.HiddenInput(), required=False)
    udf1 = forms.CharField(widget = forms.HiddenInput(), required=False)
    udf2 = forms.CharField(widget = forms.HiddenInput(), required=False)
    udf3 = forms.CharField(widget = forms.HiddenInput(), required=False)
    udf4 = forms.CharField(widget = forms.HiddenInput(), required=False)
    udf5 = forms.CharField(widget = forms.HiddenInput(), required=False)
    pg = forms.CharField(widget = forms.HiddenInput(), required=False)
    drop_category = forms.CharField(widget = forms.HiddenInput(), required=False)
    custom_note = forms.CharField(widget = forms.HiddenInput(), required=False)
    note_category = forms.CharField(widget = forms.HiddenInput(), required=False)
    service_provider = forms.CharField(widget = forms.HiddenInput(), required=True)
    
    def clean(self):
        cleaned_data = super(PayUForm, self).clean()
        cleaned_data['hash'] = generate_hash(cleaned_data)
        print(cleaned_data)
        return cleaned_data

class HashForm(forms.Form):
        hash = forms.CharField(widget = forms.HiddenInput(), required = False) 