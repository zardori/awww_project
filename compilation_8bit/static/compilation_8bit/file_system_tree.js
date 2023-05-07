// Make request to the server for file and directories in the filesystem and show them.

const container_id = "file_selection"
const tree_step_len = 30
const dir_id_prefix = "dir"
const file_id_prefix = "file"


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


// Add div node representing file.
function addFileSystemItem(container, name, id, shift, is_dir) {

    container.append("<div></div>")
    let inserted = container.children().last()
    inserted.css("position", "relative")
    inserted.css("left", shift + "px")
    inserted.css("display", "flex")
    inserted.css("flex-direction", "row")

    inserted.append("<div></div>")
    let name_div = inserted.children().last()
    name_div.css("width", "fit-content")
    name_div.text(name)

    inserted.append("<button></button>")
    let del_button = inserted.children().last()
    del_button.text("del")

    del_button.click(function() {
        delFileSystemItem(inserted)
    })


    //inserted.text(name)

    if (is_dir) {
        inserted.css("color", "yellow")
        inserted.attr("id", dir_id_prefix + id)

    } else /* is file */ {
        inserted.css("color", "red")
        inserted.attr("id", file_id_prefix + id)

    }

}



function printDir(file_system, curr_dir, shift) {

    let container = $("#" + container_id)

    addFileSystemItem(container, curr_dir.name, curr_dir.id, shift, true)

    let dir
    let file

    for (dir of file_system.directories) {
        if (dir.parent === curr_dir.id) {
            printDir(file_system, dir, shift + tree_step_len)
        }
    }

    for (file of file_system.files) {
        if (file.parent === curr_dir.id) {

            addFileSystemItem(container, file.name, file.id, shift + tree_step_len, false)

        }
    }

}



function showFileSystem(file_system) {

    console.log(file_system)

    $("#" + container_id).empty()

    let dir

    for (dir of file_system.directories) {

        if (dir.parent === null) {
            printDir(file_system, dir, 0)
            break
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
                alert("Request successful")
                showFileSystem(data)

            },
            error: function () {
                alert("Error happened")
            }
        })

}