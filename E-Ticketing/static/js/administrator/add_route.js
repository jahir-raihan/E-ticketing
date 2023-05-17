var sub_station_count = 2;
var schedule_count = 2;
function add_sub_station(){
    $('#add_new_sub_station').before(
        `<div class="new-elem"><p class="new">**New Station</p></div>
         <div class="stations destination">
                <div class="station starting-point">
                    <div class="input">
                        <label style="font-size:14px; opacity: .8;" class="label" >Sub-Station Name(${sub_station_count})</label>
                        <div class="p-wrapper">


                            <input type="text" name="sub_station"  required  placeholder="Mohipal"  >

                        </div>
                    </div>
                </div>
                <div class="station starting-point">


                    <div class="input">
                        <label style="font-size:14px; opacity: .8;" class="label" >Distance Time From (Main Station)(${sub_station_count})</label>
                        <div class="p-wrapper">


                            <input type="number" name="distance_time" required placeholder="20"  >

                        </div>
                    </div>
                </div>
                <div class="station starting-point">


                    <div class="input">
                        <label style="font-size:14px; opacity: .8;" class="label">Contact Number(${sub_station_count})</label>
                        <div class="p-wrapper">


                            <input type="number" name="sub_station_contact" required  placeholder="018xx xxxxxx"  >

                        </div>
                    </div>
                </div>
            </div>`
    )
    sub_station_count += 1;
}


function add_schedule(){
    $('#add_new_schedule').before(
        `<div class="new-elem sc-itm-txt">
            <p class="new">**New Schedule</p>
         </div>
         <div class="stations destination">

            <div class="station starting-point">


                <div class="input">
                    <label style="font-size:14px; opacity: .8;" class="label">Bus Type (${schedule_count})</label>
                    <div class="p-wrapper">


                       <select name="bus_type" required id="">
                            <option value="">---------</option>
                            <option value="Business AC">Business AC</option>
                            <option value="Business Non AC">Business Non AC</option>
                            <option value="Economy AC">Economy AC</option>
                            <option value="Economy Non AC">Economy Non AC</option>
                        </select>

                    </div>
                </div>
            </div>
            <div class="station starting-point">


                <div class="input">
                    <label style="font-size:14px; opacity: .8;" class="label" >Bus No (${schedule_count})</label>
                    <div class="p-wrapper">


                        <input type="number" name="bus_no"  required >

                    </div>
                </div>
            </div>
            <div class="station starting-point">


                <div class="input">
                    <label style="font-size:14px; opacity: .8;" class="label">Departure Time (${schedule_count})</label>
                    <div class="p-wrapper">


                        <input type="time" name="departure_time"  required>

                    </div>
                </div>
            </div>
            <div class="station starting-point">

                    <div class="input">
                        <label style="font-size:14px; opacity: .8;" class="label">Seat Capacity (${schedule_count})</label>
                        <div class="p-wrapper">


                            <input type="number"  required name="seat_capacity" >

                        </div>
                    </div>
                </div>
            </div>
         `
    )
    schedule_count += 1
}


$(document).on('submit', '#create-route', function(e){

    e.preventDefault();
    document.getElementById('c-r-c-btn').classList.add('loader-bus-c-r-c')
    document.getElementById('loader-c-r-c').classList.remove('d-none')

    let data = new FormData($('#create-route').get(0));
    let req = $.ajax({
        type:'post',
        url: '/administrator/add-route/',
        data: data,
        cache: false,
        processData: false,
        contentType: false,

    });
    req.done(function(response){
        document.getElementById("create-route").reset();
        history.pushState({}, null, window.location.href)
        window.location.replace(response.url)
    })


})