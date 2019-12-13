$(document).ready(()=> {
    let stop_button = $('.timer-stop');
    let pause_button = stop_button.parent().next().children();
    let play_button =  pause_button.parent().next().children();
    let pause_div = $('#pause_counter');
    let edit_data = $('#edit_data');
    let form_div = $('#edit_timer');
    let start_time = $('#start_time');
    let duration = $('#timer_duration');

    console.log(duration)
    console.log(start_time)

    pause_button.on('click', ()=>{
        play_button.removeClass('hidden');
        pause_div.removeClass('hidden');
        pause_button.addClass('hidden');
    });

    play_button.on('click', ()=>{
        play_button.addClass('hidden');
        pause_div.addClass('hidden');
        pause_button.removeClass('hidden');
    });

    edit_data.on("click", ()=>{
        if (form_div.hasClass('hidden')){
            form_div.removeClass('hidden');
            form_div.prev('div').addClass('hidden');
            edit_data.text('Anuluj')
        } else {
            form_div.addClass('hidden');
            form_div.prev('div').removeClass('hidden');
            edit_data.text('zmień dane')

        }
    });

    let x = setInterval(function() {
        // Find the distance between now and the count down date
        let now = new Date().getTime();
        let start_time_temp = new Date(start_time.text()).getTime()
        console.log(start_time_temp)
        duration_value = now - start_time.text();


        // Time calculations for days, hours, minutes and seconds
        let days = Math.floor(duration_value / (1000 * 60 * 60 * 24));
        let hours = Math.floor((duration_value % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minutes = Math.floor((duration_value % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((duration_value % (1000 * 60)) / 1000);

        duration.text(`${days} dni, ${hours} godzin, ${minutes} minut, ${seconds} sekund`);

}, 1000);




});
