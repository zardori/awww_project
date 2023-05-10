import logging
import subprocess

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import File, Directory, User
from .compile_options import compile_options
from django.conf import settings

logging.basicConfig(filename="logfile.txt", level=logging.DEBUG)

# session keys
selected_file_id_key = "selected_file_id"
selected_options_key = "selected_options"


# If the standard is defined in session take it to the context.
# If not set the default standard for session and context.
def get_compiler_standard(session, context):
    # logging.debug(f"current session: {session.items()}")

    default_standard = "C11"

    if selected_options_key not in session:
        session[selected_options_key] = []

    standard_already_selected = False

    for option in compile_options.standard:
        if option.name in session[selected_options_key]:
            option.checked = True
            standard_already_selected = True
        else:
            option.checked = False

    if not standard_already_selected:
        compile_options.name_to_opt(default_standard).checked = True
        session[selected_options_key].append(default_standard)

    # logging.debug(f"{[ str(opt) for opt in compile_options.standard]}")

    context["standard"] = compile_options.standard

    # logging.debug(f"{[ str(opt) for opt in context['standard']]}")


def index(request):
    context = {}

    logging.debug(f"{request.session.items()}")

    if selected_file_id_key in request.session:
        selected_file = File.objects.get(pk=int(request.session[selected_file_id_key]))
        context["selected_file"] = selected_file

    get_compiler_standard(request.session, context)

    logging.debug(f"{[str(opt) for opt in context['standard']]}")

    return render(request, "compilation_8bit/index.html", context)


def del_file(request):
    file_id = int(request.GET["id"])

    File.objects.get(pk=file_id).soft_delete()

    return get_file_system(request)


def del_dir(request):
    dir_id = int(request.GET["id"])

    Directory.objects.get(id=dir_id).soft_delete()

    return get_file_system(request)


def add_file(request):
    logging.debug(f"data received: {request.POST.dict()}")

    if request.method == "POST":
        parent = Directory.objects.get(id=request.POST["parent_id"])

        new_file = File(parent=parent, name=request.POST["file_name"],
                        content=request.POST["content"], owner=parent.owner)

        new_file.save()

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

    if selected_file_id_key in request.session:
        to_return[selected_file_id_key] = request.session[selected_file_id_key]

    return JsonResponse(to_return)


def select_file(request):
    session = request.session

    selected_id = int(request.GET[selected_file_id_key])

    session[selected_file_id_key] = selected_id

    logging.debug(f"id: {selected_id}")

    content = File.objects.get(pk=selected_id).content

    return JsonResponse({"file_content": content})


possible_standards = ["C89", "C99", "C11"]
possible_optimizations = ["opt1", "opt2", "opt3"]
possible_processors = ["MCS51", "Z80", "STM8"]

processor_dependant = {"MCS51": ["MCS51_opt_1", "MCS51_opt_2"],
                       "Z80": ["Z80_opt_1", "Z80_opt_2"],
                       "STM8": ["STM8_opt_1", "STM8_opt_2"]
                       }


def get_compilation_standard(request):
    # If the standard is not set yet, set the default one
    if "compiler_standard" not in request.session:
        request.session["compiler_standard"] = "C11"

    to_return = {"possible_standards": possible_standards,
                 "compiler_standard": request.session["compiler_standard"]}

    return JsonResponse(to_return)


def set_compilation_standard(request):
    request.session["compiler_standard"] = request.GET["compiler_standard"]

    return HttpResponse("success")


processor_name_to_option = {
    "MCS51": "-mmcs51",
    "Z80": "-mz80",
    "STM8": "-mstm8"
}


def compile(request):
    if selected_file_id_key not in request.session:
        response = JsonResponse({"error": "no file selcted"})
        response.status_code = 400
        return response

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
            if (split[1] == "dependant" and split[2] == curr_processor) \
                    or split[1] != "dependant":
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
