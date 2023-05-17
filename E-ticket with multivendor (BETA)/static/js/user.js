$(document).on('submit', '#login-form', function(e){
    e.preventDefault();
    document.getElementById('login-loader').classList.remove('d-none');
    document.getElementById('container').classList.add('events-none');
    var btn = document.getElementById('log-reg-btn')
    btn.classList.add('btn-bg')


    let data = new FormData($('#login-form').get(0));
    let req = $.ajax({
        type:'post',
        url:'/auth/login/',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
    });
    req.done(function(response){
        if (response.login===false){
            $('.p-wrapper').after('<small class="warning-invalid">Incorrect Information . Try again!</small>')
            document.getElementById('login-loader').classList.add('d-none');
            document.getElementById('container').classList.remove('events-none');

            e.preventDefault();
        }
        else{
            btn.classList.remove('btn-bg');

            window.location.replace(window.location.origin);
        }

    })

})

$(document).on('submit', '#register-form', function(e){
    e.preventDefault();
    document.getElementById('register-loader').classList.remove('d-none');
    var pass1= $('#pass1').val();
    var pass2 = $('#pass2').val();
    console.log('hello')
    if (pass1===pass2){
        var btn = document.getElementById('log-reg-btn')
        btn.classList.add('btn-bg')
        document.getElementById('container').classList.add('events-none');
        let data = new FormData($('#register-form').get(0));
        let req = $.ajax({
            type:'post',
            url:'/auth/register/',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
        });
        req.done(function(response){
            if (response.login===false){


                if (response.email===true){
                    $('#email').after('<small class="warning-invalid">Account with this email already exists.</small>')
                }
                if(response.phone===true){
                    $('#phone').after('<small class="warning-invalid">Account with this phone number already exists.</small>')
                }
                btn.classList.remove('btn-bg')
                document.getElementById('register-loader').classList.add('d-none');
                document.getElementById('container').classList.remove('events-none');


            }
            else{
                btn.classList.remove('btn-bg')
                document.getElementById('register-loader').classList.add('d-none');
                document.getElementById('container').classList.remove('events-none');
                window.location.replace(window.location.origin)
            }


        })
    }
    else{
        $('.pass').after('<small class="warning-invalid">Password didn\'t matched!</small>')
        document.getElementById('register-loader').classList.add('d-none');
        e.preventDefault();
    }

})
