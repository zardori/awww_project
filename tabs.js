let curr_selected_tab = -1;

const selected_tab_color = getComputedStyle(document.documentElement)
    .getPropertyValue('--selected_tab_color');

const unselected_tab_color = getComputedStyle(document.documentElement)
    .getPropertyValue('--unselected_tab_color');

function selectTab(tab_num) {
    console.log(tab_num);
    if (curr_selected_tab !== tab_num) {

        let tab_button = document.getElementById("tab_button_" + tab_num);
        let tab_content = document.getElementById("tab_content_" + tab_num);

        tab_button.style.backgroundColor = selected_tab_color;
        tab_content.style.display = "block";

        if (curr_selected_tab >= 0) {

            let old_tab_button = document.getElementById("tab_button_" + curr_selected_tab);
            let old_tab_content = document.getElementById("tab_content_" + curr_selected_tab);

            old_tab_button.style.backgroundColor = unselected_tab_color;
            old_tab_content.style.display = "none";
        }

        curr_selected_tab = tab_num;

    }

}

window.onload = function() {

    let tab_idx = 0;
    for (let tab_button of document.getElementById("tabs_bar").children) {
        let helper = tab_idx;
        tab_button.addEventListener("click", function(){
            selectTab(helper);
        });
        tab_idx++;
    }


    selectTab(0);
}