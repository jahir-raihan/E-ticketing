
$(document).ready(function(){
    $("#d-p-inp").datepicker({dateFormat:"yy-mm-dd",minDate:new Date(), maxDate:new Date() +1});
})
$(document).ready(function(){
    $("#d-p-inp2").datepicker({dateFormat:"yy-mm-dd",minDate:new Date(), maxDate:new Date() +1});
})

// ajax for search for bus

$(document).on('submit', '#search_for_bus_form', function(e){
    e.preventDefault();
    let to = $('#from').val();
    let from = $('#to').val();
    if (from === to){
        $('.s-f-b-p-wrapper').after('<small class="warning-invalid">Start and End location can\'t be same</small>')
    }
    else{
        document.getElementById('s-f-b-loader').classList.remove('d-none');

        let ele = $('#search-for-bus')
        ele.css('cursor', 'not-allowed')
        ele.css('background', '#a6a6a6')
        let data = new FormData($('#search_for_bus_form').get(0));
        let req = $.ajax({
            type:'POST',
            url:'/',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
        });
        req.done(function(response){
            if (response.error){
                var loc = window.location.origin + response.url
                document.title = response.site_title

                history.pushState({}, null, loc);

                $('#container').html(response.template)
            }
            else{

                var loc = window.location.origin + response.url
                document.title = response.site_title

                history.pushState({}, null, loc);

                $('#container').html(response.template)
            }
        })
    }
})

// end search for bus