from django import forms


def validate_not_empty(value):
    if value == '':
        raise forms.ValidationError(
            'Вы не заполнили поле!',
            params={'value': value},
        )
