from django import forms


class OrderForm(forms.Form):

    txnid = forms.CharField(widget = forms.HiddenInput())
    productinfo = forms.CharField(widget = forms.HiddenInput())

    # buyer details
    firstname = forms.CharField(required=False,widget = forms.HiddenInput())
    lastname = forms.CharField(required=False, widget = forms.HiddenInput())
    email = forms.EmailField(required=False,widget = forms.HiddenInput())
    address1 = forms.CharField(required=False,widget = forms.HiddenInput())
    address2 = forms.CharField(required=False, widget = forms.HiddenInput())
    city = forms.CharField(required=False,widget = forms.HiddenInput())
    state = forms.CharField(required=False,widget = forms.HiddenInput())
    country = forms.CharField(required=False,widget = forms.HiddenInput())
    zipcode = forms.RegexField(regex=r'\d{6}', min_length=6, max_length=6, required=False,widget = forms.HiddenInput())

    txnid.widget.attrs.update({'class': 'form-control form-control-lg'})
    productinfo.widget.attrs.update({'class': 'form-control form-control-lg'})
    firstname.widget.attrs.update({'class': 'form-control form-control-lg'})
    lastname.widget.attrs.update({'class': 'form-control form-control-lg'})
    email.widget.attrs.update({'class': 'form-control form-control-lg'})
    address1.widget.attrs.update({'class': 'form-control form-control-lg'})
    address2.widget.attrs.update({'class': 'form-control form-control-lg'})
    city.widget.attrs.update({'class': 'form-control form-control-lg'})
    state.widget.attrs.update({'class': 'form-control form-control-lg'})
    country.widget.attrs.update({'class': 'form-control form-control-lg'})
    zipcode.widget.attrs.update({'class': 'form-control form-control-lg'})


