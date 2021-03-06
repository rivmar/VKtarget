import os
from time import sleep
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import FileSystemStorage
from .modules import VKads
from .models import Credential
from .forms import GetTokenForm
import requests

def token_is_valid(user):
    client = VKads(user)
    try:
        groups = client.get_target_groups()
    except KeyError:
        return False
    return True

@user_passes_test(token_is_valid, login_url='/auth/')
def groups(request):
    client = VKads(request.user)
    groups = client.get_target_groups()
    return render(request, 'groups/groups.html', {'groups':groups})

def save_and_upload_users(id, f):
    fs = FileSystemStorage()
    file = fs.save(f'{id}.txt', f)
    with open(f'{settings.MEDIA_ROOT}\\{file}', 'r') as file:
        data = file.read().split(',')
    while data:
        chunk = data[:1000]
        data = data[1000:]
        client = VKads(request.user)
        client.import_target_contacts(id, ','.join(chunk))
        #avoid vk flood control.
        sleep(3)

@user_passes_test(token_is_valid, login_url='/auth/')
def group(request, pk=None):
    client = VKads(request.user)
    context = {
        'title':'Создать группу',
        "create": True
    }
    if pk:
        #if edit existing group, update context - add group name, change title etc.
        id = int(pk)
        context = {
            'title': 'Изменить список группы',
            "create": False
        }
        groups = client.get_target_groups()
        context['name'] = next(g['name'] for g in groups if g['id'] == id)

    if request.method == 'POST':
        name = request.POST.get('name', None)
        if name:
            # Application does not update group name, only userlist
            # So name in the form means that it's a new group and we have to get it's id
            id = client.create_target_group(name)

        file = request.FILES.get('file', None)
        if file:
            save_and_upload_users(id, file)

        return redirect(reverse('groups:groups'))

    return render(request, 'groups/add.html', context)

@user_passes_test(token_is_valid, login_url='/auth/')
def files(request, pk):
    _files = os.listdir(settings.MEDIA_ROOT)
    group_files = list(filter(lambda x: pk in x, _files))
    return render(request, 'groups/files.html', {'files':group_files})

@login_required
def get_token(request):
    code = request.GET['code']
    user = request.user
    url = settings.VK_TOKEN_URL
    data = {
        'client_id': user.credentials.client_id,
        'client_secret': user.credentials.secret,
        'redirect_uri': user.credentials.url+'/token/',
        'scope': 'offline',
        'code': code
    }
    r = requests.get(url, params=data)
    token = r.json()['access_token']
    user.credentials.token = token
    user.credentials.save()

    return redirect('/')

@login_required
def auth(request):
    form = GetTokenForm()
    if request.method == 'POST':
        client_id = request.POST['client_id']
        secret = request.POST['secret']
        account_id = request.POST['account_id']
        url = request.POST['url']
        user = request.user

        user_cred = Credential.objects.get_or_create(user = user)[0]
        user_cred.client_id=client_id
        user_cred.secret=secret
        user_cred.account_id=account_id
        user_cred.url=url
        user_cred.save()

        auth_url = settings.VK_AUTH_URL.format(client_id, url)
        return redirect(auth_url)

    return render(request, 'groups/auth.html', {'form': form})
