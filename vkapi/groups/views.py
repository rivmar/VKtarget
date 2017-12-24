import os
from time import sleep
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .modules import VKads

@login_required
def groups(request):
    client = VKads()
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
        client = VKads()
        client.import_target_contacts(id, ','.join(chunk))
        #avoid vk flood control.
        sleep(3)

@login_required
def group(request, pk=None):
    client = VKads()
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

@login_required
def files(request, pk):
    _files = os.listdir(settings.MEDIA_ROOT)
    group_files = list(filter(lambda x: pk in x, _files))
    return render(request, 'groups/files.html', {'files':group_files})
