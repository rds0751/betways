from django import forms
from django.forms import ModelForm
from binary.models import BinaryTree

STATES = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)

class BinaryJoinForm(forms.ModelForm):
    class Meta:
        model = BinaryTree
        fields = ['user', 'direct_user_id', 'amount', 'position']