let already_selected;
let seat_containers;

// ajax & codes for viewing bus data with seats .


$(document).on('click', '.bus-info-table', function(e){
    e.preventDefault();
    var bus = $(this)[0];
    let id = $(this).attr('counter');
    let bus_id = $(this).attr('bus_id');
    let route = $(this).attr('route')

    if (already_selected){

        document.getElementById(seat_containers).remove();
        seat_containers = null;


    }
    if (already_selected === 'bus_no'+id){
        already_selected = null;

    }
    else{
        already_selected=null;


        document.getElementById('bus_loader'+id).classList.remove('d-none');
        document.getElementById('bus_info_table'+id).classList.add('loader-bus');

        let req = $.ajax({
                type:'post',
                url:'/bus-list/show-bus-data/',
                data: {
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    bus_id:bus_id,
                    route:route,
                },


        });
        req.done(function(response){
            console.log('data got')
            document.getElementById('bus_loader'+id).classList.add('d-none');
            document.getElementById('bus_info_table'+id).classList.remove('loader-bus');
            document.getElementById('bus_no'+id).classList.add('selected-bus');

            $('#bus_info_table'+id).after(response);



        })
        already_selected = 'bus_no'+id;
        seat_containers = 'seat-data-container'+bus_id;


    }



})