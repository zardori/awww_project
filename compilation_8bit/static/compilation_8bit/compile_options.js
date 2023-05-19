
// Prefix of id's of options which are bases for dependencies with others
const option_base_prefix = "option_base_"

const dependant_prefix = "dependant_"

let curr_processor_selected = null


function setupCompilation() {
    setupCompileOptions()
    setupCompileButton()
}


function getDependant(base) {
    return $("#" + dependant_prefix + base.attr("id").slice(option_base_prefix.length))
}

function setupCompileOptions() {
    $("[id^='" + option_base_prefix + "']").each(function(){
        let current = $(this)
        let dependant_elem = getDependant(current)

        if (current.is(':checked')) {
            dependant_elem.css("display", "block")
            curr_processor_selected = current
        } else {
            dependant_elem.css("display", "none")
        }

        current.change( function() {
            if (curr_processor_selected != null) {
                getDependant(curr_processor_selected).css("display", "none")
            }
            getDependant(current).css("display", "block")
            curr_processor_selected = current
        })
    })
}


function setupCompileButton() {

    $("#compile_button").click(function() {

        $.ajax(
            {
                type: "POST",
                url: compile_url,
                headers: {'X-CSRFToken': csrftoken},
                data: $("#compilation_form").serialize(),
                success: function (data) {
                    $("#code_part pre").text(data.compile_result)
                },
                error: function (data) {
                    alert(data.responseJSON.error)
                }
            })
    })
}

