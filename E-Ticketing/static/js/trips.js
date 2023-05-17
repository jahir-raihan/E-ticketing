$(document).on('click', '.future-trips', function(e){
    e.preventDefault();

    var data = $(this);
    url = '/view-ticket/'+data.attr('t_id')+'/'+data.attr('obj_id')+'/'
    window.location.replace(url)

})