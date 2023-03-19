let curr_selected_tab = -1;

const SELECTED_TAB_COLOR = getComputedStyle(document.documentElement)
    .getPropertyValue('--selected_tab_color');

const UNSELECTED_TAB_COLOR = getComputedStyle(document.documentElement)
    .getPropertyValue('--unselected_tab_color');

// maximum value of screen width in px for which mobile display of application is used
const MAX_MOBILE_SIZE = 600;


function selectTab(tab_num) {
    if (curr_selected_tab !== tab_num) {

        let tab_button = document.getElementById("tab_button_" + tab_num);
        let tab_content = document.getElementById("tab_content_" + tab_num);

        tab_button.style.backgroundColor = SELECTED_TAB_COLOR;
        tab_content.style.display = "block";

        if (curr_selected_tab >= 0) {

            let old_tab_button = document.getElementById("tab_button_" + curr_selected_tab);
            let old_tab_content = document.getElementById("tab_content_" + curr_selected_tab);

            old_tab_button.style.backgroundColor = UNSELECTED_TAB_COLOR;
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


    // Prepare tabs open button and tabs close button for mobile version

    const TABS_OPENER = document.getElementById("tabs_opener");

    const TABS_CLOSER = document.getElementById("tabs_closer");

    const TABS_WRAPPER = document.getElementById("tabs_wrapper");

    TABS_OPENER.addEventListener("click", function() {
        TABS_WRAPPER.style.visibility = "visible";
        TABS_CLOSER.style.visibility = "visible";
        TABS_OPENER.style.visibility = "hidden";
    })

    TABS_CLOSER.addEventListener("click", function() {
        TABS_WRAPPER.style.visibility = "hidden";
        TABS_OPENER.style.visibility = "visible";
        TABS_CLOSER.style.visibility = "hidden";
    })


    window.addEventListener("resize", function() {

        if (window.innerWidth <= MAX_MOBILE_SIZE) {
            TABS_WRAPPER.style.visibility = "hidden";
            TABS_OPENER.style.visibility = "visible";
            TABS_CLOSER.style.visibility = "hidden";
        } else {
            TABS_WRAPPER.style.visibility = "visible";
            TABS_OPENER.style.visibility = "hidden";
            TABS_CLOSER.style.visibility = "hidden";
        }

    })


}