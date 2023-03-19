
function prepareMenuButtons() {

    const file_selection_opener = document.getElementById("file_selection_opener");
    const file_selection_closer = document.getElementById("file_selection_closer");
    const menu_opener = document.getElementById("menu_opener");
    const menu_closer = document.getElementById("menu_closer");
    const menu = document.getElementById("menu");
    const file_selection = document.getElementById("file_selection");

    // file selection
    file_selection_opener.addEventListener("click", function () {

        file_selection.style.visibility = "visible";
        file_selection_opener.style.display = "none";
        file_selection_closer.style.display = "inline-block";
    });

    file_selection_closer.addEventListener("click", function() {
        file_selection.style.visibility = "hidden";
        file_selection_opener.style.display = "inline-block";
        file_selection_closer.style.display = "none";
    })


    // menu
    menu_opener.addEventListener("click", function() {
        menu.style.display = "block";
        menu_closer.style.display = "inline-block";
        menu_opener.style.display = "none";
    })

    menu_closer.addEventListener("click", function() {
        menu.style.display = "none";
        menu_opener.style.display = "inline-block";
        menu_closer.style.display = "none";
    })


    // resize
    window.addEventListener("resize", function() {

        if (window.innerWidth <= MAX_MOBILE_SIZE) {
            menu.style.display = "none";
            menu_opener.style.display = "inline-block";
            menu_closer.style.display = "none";
            file_selection.style.visibility = "hidden";
            file_selection_opener.style.display = "inline-block";
            file_selection_closer.style.display = "none";
        } else {
            menu.style.display = "block";
            menu_opener.style.display = "none";
            menu_closer.style.display = "none";
            file_selection.style.visibility = "visible";
            file_selection_opener.style.display = "none";
            file_selection_closer.style.display = "none";
        }

    })


}