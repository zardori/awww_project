import logging
from django.shortcuts import render
from django.http import JsonResponse
from .models import File, Directory, User

logging.basicConfig(filename="logfile.txt", level=logging.DEBUG)


def index(request):
    context = {}

    return render(request, "compilation_8bit/index.html", context)


def del_file(request):
    file_id = int(request.GET["id"])

    logging.debug(f'{file_id}')

    File.objects.get(pk=file_id).soft_delete()

    return get_file_system(request)


def del_dir(request):
    dir_id = int(request.GET["id"])

    Directory.objects.get(id=dir_id).soft_delete()

    return get_file_system(request)



def get_file_system(request):

    logging.debug("got file system request")

    to_return = {}

    files = []
    directories = []

    for f in File.objects.all().filter(is_deleted__exact=False):

        parent = None
        if f.parent is not None:
            parent = f.parent.id

        files.append({"id": f.id, "name": f.name, "parent": parent})

    for d in Directory.objects.all().filter(is_deleted__exact=False):

        parent = None
        if d.parent is not None:
            parent = d.parent.id

        directories.append({"id": d.id, "name": d.name, "parent": parent})

    to_return['files'] = files
    to_return['directories'] = directories

    return JsonResponse(to_return)
