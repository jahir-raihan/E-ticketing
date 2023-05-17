
$(window).on('popstate', function (e) {
    var state = e.originalEvent.state;

    if (state !== null) {
        history.back()
        location.reload();

    } else {

        window.location.replace('/')
    }
});
