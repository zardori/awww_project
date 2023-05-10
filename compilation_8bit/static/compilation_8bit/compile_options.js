
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
                    alert("success")
                    console.log(data.compile_result)
                },
                error: function (data) {
                    alert(data.responseJSON.error)
                }
            })



    })


}















function getCompileOptions(){

    // getCompilationStandard()



}

function getCompilationStandard() {

    let container = $("#tab_content_0")

    $.ajax(
    {
        type: "GET",
        url: get_compilation_standard_url,
        success: function (data) {


            renderOptions("tab_content_0", data.possible_standards,
                data.compiler_standard)

           /* let standard

            for (standard of data.possible_standards) {

                container.append("<input type='radio' id='compiler_standard_0' name='choice'>")
                if (standard === data.compiler_standard) {
                    container.children().last()[0].checked = true
                }

                container.append( "<label for='compiler_standard_0'></label>")
                container.children().last().text(standard)

                container.append("<br>")
            }
*/
        },
        error: function () {
            alert("Error happened")
        }
    })



}


function renderOptions(container_id, option_list, selected) {

    let container = $("#" + container_id)

    let radio_button
    let label

    for (let option of option_list) {

        container.append("<input type='radio'  name='choice'>")
        radio_button = container.children().last()

        radio_button.attr("id", option)

        if (selected === option) {
            radio_button[0].checked = true
        }

        container.append( "<label></label>")
        label = container.children().last()

        label.text(option)
        label.attr("for", option)

        container.append("<br>")

    }

}



