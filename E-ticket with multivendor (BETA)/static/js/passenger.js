$(document).on('submit', '#contact_information_form', function(e){

    e.preventDefault();


    document.getElementById('loader-p-t-p-f').classList.remove('d-none');
    document.getElementById('loader-bus-p-t-p-f').classList.add('loader-bus-p-t-p');
    let data = new FormData($('#contact_information_form').get(0));
    let req = $.ajax({
        type:'post',
        url: '/buy-seats/passenger-contact-info/',
        data: data,
        cache: false,
        processData: false,
        contentType: false,

    });
    req.done(function(data){
        console.log(data)
        document.getElementById('loader-p-t-p-f').classList.add('d-none');
        document.getElementById('loader-bus-p-t-p-f').classList.remove('loader-bus-p-t-p');
        if (data.error){
            window.location.replace('/unavailable/'+data.queue_id+'/');


        }
        else{
           window.location.replace(data.url)
        }

    });
});