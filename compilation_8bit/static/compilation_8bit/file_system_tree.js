// Make request to the server for file and directories in the filesystem and show them.

const container_id = "file_selection"
const tree_step_len = 30
const dir_id_prefix = "dir"
const file_id_prefix = "file"
const file_container_id = "program_code"

let curr_selected_file_id = null

function delFileSystemItem(item) {

    let url
    let item_id
    let html_node_id = item.attr("id")

    if (html_node_id.includes(dir_id_prefix)) {
        url = del_dir_url
        item_id = parseInt(html_node_id.slice(dir_id_prefix.length))

    } else { /* must be a file */
        url = del_file_url
        item_id = parseInt(html_node_id.slice(file_id_prefix.length))
    }


    $.ajax(
        {
            type: "GET",
            url: url,
            data: {id: item_id},
            success: function (data) {
                console.log("Object deleted successfully.")
                showFileSystem(data)
            },
            error: function () {
                alert("Error happened")
            }
        })
}

function addFile(file, parent_id) {

    let reader = new FileReader()

    reader.addEventListener("load", function () {

        $.ajax(
            {
                type: "POST",
                url: add_file_url,
                headers: {'X-CSRFToken': csrftoken},
                data: {
                    file_name: file.name,
                    content: reader.result,
                    parent_id: parent_id
                },
                success: function (data) {
                    showFileSystem(data)
                },
                error: function (data) {
                    alert("error")
                }
            })
    })

    reader.readAsText(file)

}

function setupFileSystemActions() {
    $("#add_dir_button").click(function() {
        addDirectory(null)
    })
}


function addDirectory(parent_id) {

    $("body").append("<div class = 'popup_window'></div>")

    let popup_window = $(".popup_window")

    popup_window.append("<div> </div>")

    let popup_main_div = $(".popup_window div")
    popup_main_div.append("<form> <label for = 'dir_name'>directory name:</label><input id = 'dir_name' name = 'dir_name' type = 'text'></form>")

    popup_window.append("<button class = 'popup_close_button'>close</button>")

    $(".popup_close_button").click(function() {
        $(".popup_window").remove()
    })

    popup_main_div.append("<button>submit</button>")

    popup_main_div.children().last().click(function() {

        let to_send = {
            dir_name: popup_main_div.find("input").val(),
        }

        if (parent_id != null) {
            to_send.parent_id = parent_id
        }


        $(".popup_window").remove()

        $.ajax(
            {
                type: "POST",
                headers: {'X-CSRFToken': csrftoken},
                url: add_dir_url,
                data: to_send,
                success: function(data) {
                    showFileSystem(data)
                },
                error: function(data) {
                    alert("could not add directory")
                }
            }
        )

    })
}





// Add div node representing file or directory to the parent div.
function addFileSystemNode(container, name, id, shift, is_dir) {

    container.append("<div></div>")
    let inserted = container.children().last()
    inserted.css("position", "relative")
    inserted.css("left", shift + "px")
    inserted.css("display", "flex")
    inserted.css("flex-direction", "row")
    inserted.css("width", "fit-content")

    inserted.append("<div></div>")
    let name_div = inserted.children().last()
    name_div.css("width", "fit-content")
    name_div.text(name)

    inserted.append("<button>del</button>")
    let del_button = inserted.children().last()

    del_button.click(function() {
        delFileSystemItem(inserted)
    })


    if (is_dir) {
        inserted.css("color", "yellow")
        inserted.attr("id", dir_id_prefix + id)

        inserted.append("<input type='file' id='file' name='file' />")
        let file_upload = inserted.children().last()
        file_upload.css("display", "none")


        file_upload.change(function(){
            let files = file_upload[0].files
            if (files.length > 0) {
                addFile(files[0], id)
            }
        })

        inserted.append("<button>add file</button>")
        let add_file_button = inserted.children().last()
        add_file_button.click(function() {
            file_upload.trigger("click")
        })

        inserted.append("<button> add dir</button>")
        let add_dir_button = inserted.children().last()
        add_dir_button.click(function () {
            addDirectory(id)
        })


    } else /* is file */ {
        inserted.css("color", "red")
        inserted.attr("id", file_id_prefix + id)

        if (curr_selected_file_id === id) {
            inserted.css("background-color", "black")
        }


        inserted.click(
            function () {
                $.ajax(
                    {
                        type: "GET",
                        data: {selected_file_id: id},
                        url: select_file_url,
                        success: function (data) {

                            // uncolor previous element
                            if (curr_selected_file_id != null) {
                                $("#" + file_id_prefix + curr_selected_file_id).css(
                                    "background-color", "transparent"
                                )
                            }
                            curr_selected_file_id = id

                            // color new element
                            inserted.css("background-color", "black")

                            // display text
                            $("#" + file_container_id + " pre").text(data.file_content)

                        },
                        error: function () {
                            alert("Error happened")
                        }
                    })


            }
        )


    }

}



function printDir(file_system, curr_dir, shift) {

    let container = $("#" + container_id)

    addFileSystemNode(container, curr_dir.name, curr_dir.id, shift, true)

    let dir
    let file

    for (dir of file_system.directories) {
        if (dir.parent === curr_dir.id) {
            printDir(file_system, dir, shift + tree_step_len)
        }
    }

    for (file of file_system.files) {
        if (file.parent === curr_dir.id) {

            addFileSystemNode(container, file.name, file.id, shift + tree_step_len, false)

        }
    }

}



function showFileSystem(file_system) {

    if (Object.hasOwn(file_system, "selected_file_id")) {
        curr_selected_file_id = file_system.selected_file_id
    }


    console.log(file_system)

    $("#" + container_id).empty()

    let dir

    for (dir of file_system.directories) {
        if (dir.parent === null) {
            printDir(file_system, dir, 0)
        }
    }

}




function getFileSystem() {


    console.log("url: " + get_file_system_url)

    $.ajax(
        {
            type: "GET",
            url: get_file_system_url,
            success: function (data) {
                showFileSystem(data)

            },
            error: function () {
                alert("Error happened")
            }
        })

}