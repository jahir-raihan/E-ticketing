//  This file is just a representation of the embed code inside bus_seat_template.
// This is only for  readability.

var selected = [];
var element = [];
var total = 0;
var price = 1400;

$(document).ready(function(){
    $(".not-occupied").click(function(){
        console.log('function triggered ')
        let ele = $(this);
        let seat_name = ele[0].outerText;
        if (!check_already_selected(seat_name) && selected.length <= 9){
            ele.css('background', 'rgb(12, 169, 248)');
            ele.css('color', 'white');
            ele.css('border', '1px solid white')

            
            selected.push(seat_name)
            element.push(ele)
            total += price;
            let temp = document.createElement('tr')
            temp.setAttribute('id', `${seat_name}`)
            
            temp.innerHTML = `<td><p class="s-name">${seat_name}</p></td> <td><p class="price">1400</p></td><td> <p class="cancel" onclick="remove_seat('${seat_name}')">&#10006;</p></td>`
            document.getElementById('total-amount').innerHTML = `<p>${total} TK</p>`;
            $('#t-a-t').before(temp)
        }
    });
});

function remove_seat(seat_id){
    var idx = selected.indexOf(seat_id)
    var ele = element[idx]

    ele.css('background', 'unset');
    ele.css('color', 'black');
    ele.css('border', '1px solid black')
    element.splice(idx, 1)
    document.getElementById(seat_id).remove();
    selected.splice(idx, 1)
    total -= price;
    document.getElementById('total-amount').innerHTML = `<p>${total} TK</p>`;
}

function check_already_selected(seat_name){
    
    if (selected.includes(seat_name)){
        return true
    }
    return false
}

// buying seats

$(document).on('submit', '#select-boarding-point-form', function(e){

    e.preventDefault();
    document.getElementById('loader-p-t-p').classList.remove('d-none');
    document.getElementById('loader-bus-p-t-p').classList.add('loader-bus-p-t-p');

    let req = $.ajax({
        type:'post',
        url: '/buy-seats/',
        data: {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            boarding_point: $('#boarding_point').val(),
            bus_id: $('#bus_id_for_seats').val(),
            seats: selected,
            total: total,
        }


    });
    req.done(function(data){
        console.log('data received');
    });


})