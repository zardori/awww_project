// script to handle logout button on the main page

function setupLogoutButton() {
    $("#logout").click(function() {
        console.log("logout button clicked")
        $.ajax(
            {
                type: "POST",
                url: logout_url,
                headers: {'X-CSRFToken': csrftoken},
                success: function (data) {
                    // this url probably should be read from settings
                    window.location.href = "/accounts/login"
                },
                error: function (data) {
                }
            })
    })
}