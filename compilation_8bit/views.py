import logging
import subprocess

from django.urls import reverse


from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import File, Directory, User, FilesystemItem
from .compile_options import compile_options
from django.conf import settings
from django.contrib.auth.decorators import login_required

logging.basicConfig(filename="logfile.txt", level=logging.DEBUG)

# session keys
selected_file_id_key = "selected_file_id"
selected_options_key = "selected_options"


# decorator for returning 403 error if the user is not logged
def logged_or_403(func):
    def inner(request):
        if not request.user.is_authenticated:
            response = JsonResponse({"error": "no user logged"})
            response.status_code = 403
            return response
        return func(request)

    return inner


def get_object_from_id(model, object_id):
    try:
        object_id = int(object_id)
        return model.objects.get(pk=object_id)
    except (model.DoesNotExist, ValueError, TypeError):
        return None


def error_json(text, code):
    response = JsonResponse({"error": text})
    response.status_code = code
    return response


@login_required
def index(request):

    return render(request, "compilation_8bit/index.html", {})


# Helper function for deleting files and directories
def del_file_system_object(request, model):
    object_to_del = get_object_from_id(model, request.GET.get("id"))

    if object_to_del is not None and object_to_del.owner == request.user:
        object_to_del.soft_delete()
    else:
        response = JsonResponse(
            {"error": f"cannot delete object of id = {str(request.GET.get('id'))}"}
        )
        response.status_code = 400
        return response

    return get_file_system(request)


@logged_or_403
def del_file(request):
    return del_file_system_object(request, File)


@logged_or_403
def del_dir(request):
    return del_file_system_object(request, Directory)


@logged_or_403
def add_file(request):
    #logging.debug(f"data received: {request.POST.dict()}")

    parent = get_object_from_id(Directory, request.POST.get("parent_id"))
    name = request.POST.get("file_name")
    owner = request.user
    content = request.POST.get("content")

    if name is None or len(name) > FilesystemItem.MAX_FILE_SYSTEM_ITEM_NAME_LEN\
            or content is None or parent is None:
        return error_json("Cannot add file.", 400)

    if parent.owner != owner:
        return error_json("Cannot add file.", 400)

    new_file = File(parent=parent, name=name,
                    content=content, owner=owner)
    new_file.save()

    return get_file_system(request)


@logged_or_403
def add_dir(request):
    #logging.debug(f"got add directory request: {request.POST.dict()}")

    parent = get_object_from_id(Directory, request.POST.get("parent_id"))
    name = request.POST.get("dir_name")
    owner = request.user

    if name is None or len(name) > FilesystemItem.MAX_FILE_SYSTEM_ITEM_NAME_LEN:
        return error_json("Cannot add directory.", 400)

    if parent is None:
        new_dir = Directory(name=name, owner=owner)
    else:
        if request.user != parent.owner:
            return error_json("Cannot add directory.", 400)
        else:
            new_dir = Directory(parent=parent, name=name, owner=owner)

    new_dir.save()

    return get_file_system(request)



@logged_or_403
def get_file_system(request):
    logging.debug("got file system request")

    to_return = {}

    files = []
    directories = []

    for f in File.objects.all().filter(is_deleted__exact=False) \
            .filter(owner=request.user):
        parent = None
        if f.parent is not None:
            parent = f.parent.id

        files.append({"id": f.id, "name": f.name, "parent": parent})

    for d in Directory.objects.all().filter(is_deleted__exact=False) \
            .filter(owner=request.user):
        parent = None
        if d.parent is not None:
            parent = d.parent.id

        directories.append({"id": d.id, "name": d.name, "parent": parent})

    to_return['files'] = files
    to_return['directories'] = directories

    if selected_file_id_key in request.session:
        to_return[selected_file_id_key] = request.session[selected_file_id_key]

    logging.debug(to_return)

    return JsonResponse(to_return)


@logged_or_403
def select_file(request):
    file_to_select = get_object_from_id(File, request.GET.get(selected_file_id_key))

    if file_to_select is not None and file_to_select.owner == request.user:
        request.session[selected_file_id_key] = request.GET[selected_file_id_key]
    else:
        return error_json("Cannot select file", 400)

    return JsonResponse({"file_content": file_to_select.content})


processor_name_to_option = {
    "MCS51": "-mmcs51",
    "Z80": "-mz80",
    "STM8": "-mstm8"
}


@logged_or_403
def compile_file(request):
    selected_file_id = request.session.get(selected_file_id_key)
    if selected_file_id is None:
        return error_json("no file selected", 400)

    selected_file = get_object_from_id(File, selected_file_id)
    if selected_file is None:
        return error_json("bad file selected", 400)

    if selected_file.owner != request.user:
        return error_json("cannot access selected file", 403)

    logging.debug(f"got compilation request: {request.POST.dict()}")

    curr_processor = ""

    options_dict = request.POST

    if "option_processor" in options_dict:
        curr_processor = options_dict["option_processor"]

    split = []

    parsed_options = []

    for option in options_dict:
        if option == "option_processor":
            continue

        split = option.split("_")

        if split[0] == "option":

            if (len(split) >= 2 and split[1] != "dependant") \
                    or (len(split) >= 3 and split[1] == "dependant" and split[2] == curr_processor):
                parsed_options.append(options_dict[option])


    if curr_processor != "":
        parsed_options.append(processor_name_to_option[curr_processor])

    logging.debug(f"parsed options {parsed_options}")

    logging.debug(f"path: {settings.BASE_DIR.joinpath('compilation_8bit/compilation')}")
    logging.debug(f"path: {settings.BASE_DIR}")

    compile_source_file_path = settings.BASE_DIR.joinpath('compilation_8bit/compilation/compile_tmp.c')
    compile_result_file_path = settings.BASE_DIR.joinpath('compilation_8bit/compilation/compile_tmp.asm')

    with open(compile_source_file_path, "w") \
            as to_compile:
        # Write content of the selected file to temporary file
        to_compile.write(File.objects.get(pk=request.session[selected_file_id_key]).content)

    command = ["sdcc", "-S"]
    command.extend(parsed_options)
    command.append(str(compile_source_file_path))
    command.extend(["-o", str(compile_result_file_path)])

    logging.debug(f"command: {command}")

    compile_process = subprocess.run(command, stdout=subprocess.PIPE)

    result = ""

    with open(compile_result_file_path, "r") as compiled:
        result = compiled.read()

    return JsonResponse({"compile_result": result})
