function show_p_options(){
    let ele = document.getElementById('profile-toggle');
    ele.classList.toggle('d-none')
    let ele1 = document.getElementById('dashboard-toggle');
    ele1.classList.add('d-none')
    let dash = document.getElementById('dashboard-link')
    dash.classList.remove('bg-black')

}
function show_dash_options(){
    let ele = document.getElementById('dashboard-toggle');
    ele.classList.toggle('d-none')
    let ele1 = document.getElementById('profile-toggle');
    ele1.classList.add('d-none')
    
    let dash = document.getElementById('dashboard-link')
    dash.classList.toggle('bg-black')

    
}