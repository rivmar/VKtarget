from django import forms

class GetTokenForm(forms.Form):
    client_id = forms.CharField(max_length=20, label='ID приложения')
    secret = forms.CharField(max_length=20, label='Защищенный ключ')
    account_id = forms.CharField(max_length=20, label='ID рекламного кабинета')
    url = forms.URLField(max_length=200, label='URL приложения без завершающего "/". Этот же домен должен быть'+
                         ' указан в настройках приложения в vk')