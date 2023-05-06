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

function prepareTabs() {

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

    const tabs_opener = document.getElementById("tabs_opener");

    const tabs_closer = document.getElementById("tabs_closer");

    const tabs_wrapper = document.getElementById("tabs_wrapper");

    tabs_opener.addEventListener("click", function() {
        tabs_wrapper.style.visibility = "visible";
        tabs_closer.style.visibility = "visible";
        tabs_opener.style.visibility = "hidden";
    })

    tabs_closer.addEventListener("click", function() {
        tabs_wrapper.style.visibility = "hidden";
        tabs_opener.style.visibility = "visible";
        tabs_closer.style.visibility = "hidden";
    })


    window.addEventListener("resize", function() {

        if (window.innerWidth <= MAX_MOBILE_SIZE) {
            tabs_wrapper.style.visibility = "hidden";
            tabs_opener.style.visibility = "visible";
            tabs_closer.style.visibility = "hidden";
        } else {
            tabs_wrapper.style.visibility = "visible";
            tabs_opener.style.visibility = "hidden";
            tabs_closer.style.visibility = "hidden";
        }

    })


}