// This javaScript file is only for navigation

// Navigation Normal User Interface



$(document).on('click', '.m-nav-section', function(e){
    let section_no_lst = ['counter-info', 'cancel-tickets', 'nav-home', 'trips', 'options-settings']
    e.preventDefault();
    let section_id = $(this).attr('s_no');
    let curr_ele = section_no_lst.splice(section_id-1, 1)[0]
    var element = document.getElementById(curr_ele)
    element.classList.add('active-nav')
    for(var sec of section_no_lst){
        document.getElementById(sec).classList.remove('active-nav')

    }
    document.getElementById('bus_loader_navigation').classList.remove('d-none')
    var container = document.getElementById('container')
    container.classList.add('disable-screen')
    var body = document.getElementById('main-body')
    body.classList.add('disable-scroll')
    try{
         var footer = document.getElementById('footer')
         footer.classList.add('disable-screen')
    }
    catch{}


    var req = $.ajax({
        type:'post',
        url:'/'+curr_ele+'/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        }
    });
    req.done(function(response){
        container.classList.remove('disable-screen');
        body.classList.remove('disable-scroll');
        try{

             footer.classList.remove('disable-screen')
        }
        catch{}

        document.getElementById('bus_loader_navigation').classList.add('d-none')
        console.log('response', response)
        document.title = response.title

        history.pushState({}, null, response.url);

        $('#container').html(response.template)
    })



})

// End Navigation Normal User Interface