function search(){
    let key = $('#search_user_staff').val();
    if (key === ''){

    }
    else{
        let btn = document.getElementById('search-user-staff')
        btn.classList.add('loader-btn')
        let loader = document.getElementById('loader-s-u-staff')
        loader.classList.remove('d-none')

        let req = $.ajax({
            type:'POST',
            url: '/administrator/search-user-staff/',
            data: {
                 csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                 keyword: key
            }
        });
        req.done(function(response){
            $('#user-container').html(response)
            console.log(response)
            btn.classList.remove('loader-btn')
            loader.classList.add('d-none')
        })



    }
}
function search_recent(){
    let key = $('#search_recent_keyword').val();
    if (key === ''){

    }
    else{
        let btn = document.getElementById('search_recent_btn')
        btn.classList.add('loader-btn')
        let loader = document.getElementById('loader-s-rec')
        loader.classList.remove('d-none')

        let req = $.ajax({
            type:'POST',
            url: '/administrator/search-recent-bookings-data/',
            data: {
                 csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                 keyword: key
            }
        });
        req.done(function(response){
            $('#booking-data').html(response)
            console.log(response)
            btn.classList.remove('loader-btn')
            loader.classList.add('d-none')
        })



    }
}

$(document).ready(function(){

     $('#trips-data-admin-filter').on('change', function(){

        try{
            var selectedEle = $(this).children("option:selected").val();

            let req = $.ajax({
                type:'post',
                url: '/administrator/filter-earning-data/',
                data:{
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    filter_by: selectedEle,

                }
            });
            req.done(function(response){
                $('#r-t-container').html(response.template)
                document.getElementById('filter-title').innerHTML = 'Data by ' + selectedEle
            })

        }
        catch{}


     })
})