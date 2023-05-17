$(document).on('submit', '#cancel_ticket_form', function(e){
    e.preventDefault();

    let ele = $('#cancel_ticket_btn')
    ele.css('cursor', 'not-allowed')
    ele.css('background', '#a6a6a6')
    document.getElementById('cancel_ticket_loader').classList.remove('d-none')
    let data = new FormData($('#cancel_ticket_form').get(0));
    let req = $.ajax({
        type:'post',
        url:'/cancel-tickets/send-code/',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
    });
    req.done(function(response){

        if (response.error){
            history.pushState({}, null, window.location.href);
            window.location.replace(response.url);
        }
        else{
            document.title = response.title
            history.pushState({}, null, response.url);
            $('#cancel_ticket_container').html(response.template)
        }
    })

})

$(document).on('submit', '#cancel_ticket_code', function(e){
    e.preventDefault();
    let ele = $('#cancel_ticket_btn')
    ele.css('cursor', 'not-allowed')
    ele.css('background', '#a6a6a6')
    document.getElementById('cancel_ticket_loader').classList.remove('d-none')
    let data = new FormData($('#cancel_ticket_code').get(0));
    let req = $.ajax({
        type:'post',
        url:'/cancel-tickets/submit-code/',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
    });
    req.done(function(response){

        document.title = response.title

        $('#container').html(response.template)

    })

})

