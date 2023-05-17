$(document).ready(function(){

     $('#permission').on('change', function(){
        console.log('triggred')
        try{
            var selectedEle = $(this).children("option:selected").val();
            if (selectedEle === 'staff'){
                console.log('do it')
                document.getElementById('s-staff-station').classList.remove('d-none');

                $("#id_station_name").attr('required', 'true');
                console.log('come here')


            }
            else{

                document.getElementById('s-staff-station').classList.add('d-none');
                var ele = document.getElementById('#id_station_name').required = false;
            }
        }
        catch{}


     })
})

$(document).on('submit', '#register-staff', function(e){

    e.preventDefault();
    document.getElementById('loader-reg-staff').classList.remove('d-none');
    var pass1= $('#pass1').val();
    var pass2 = $('#pass2').val();
    console.log('hello')
    if (pass1===pass2){
        var btn = document.getElementById('reg-staff-btn')
        btn.classList.add('btn-bg')
        document.getElementById('container').classList.add('events-none');
        let data = new FormData($('#register-staff').get(0));
        let req = $.ajax({
            type:'post',
            url:'/administrator/add-staff/',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
        });
        req.done(function(response){
            if (response.register===false){


                if (response.email===true){
                    $('#email').after('<small class="warning-invalid">Account with this email already exists.</small>')
                }
                if(response.phone===true){
                    $('#phone').after('<small class="warning-invalid">Account with this phone number already exists.</small>')
                }
                btn.classList.remove('btn-bg')
                document.getElementById('loader-reg-staff').classList.add('d-none');
                document.getElementById('container').classList.remove('events-none');


            }
            else{
                btn.classList.remove('btn-bg')
                document.getElementById('loader-reg-staff').classList.add('d-none');
                document.getElementById('container').classList.remove('events-none');
                document.getElementById("register-staff").reset();
                 history.pushState({}, null, window.location.href)
                window.location.replace(response.url)
            }


        })
    }
    else{
        $('.pass').after('<small class="warning-invalid">Password didn\'t matched!</small>')
        document.getElementById('loader-reg-staff').classList.add('d-none');
        e.preventDefault();
    }

})
