
function getCompileOptions(){

    getCompilationStandard()



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



