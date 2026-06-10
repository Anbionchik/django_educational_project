from django import forms
from list_item.models import ListItemModel
from django.core.exceptions import NON_FIELD_ERRORS


class ListItemForm(forms.ModelForm):
    """
    Форма надстроек расписания обмена
    """
    name = forms.CharField(required=True, widget=forms.TextInput())
    expiration_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ListItemModel
        fields = ('name', 'expiration_date', 'listmodel_id')
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Такая задача уже существует.",
            }
        }
