$(document).ready(() => {
    let stop_button = $('.timer-stop');
    let pause_button = stop_button.parent().next().children();
    let play_button = pause_button.parent().next().children();
    let pause_div = $('#pause_counter');
    let edit_data = $('#edit_data');
    let form_div = $('#edit_timer');
    let start_time = $('#start_time');
    let duration_text = $('#timer_duration');
    moment.locale('pl');
    duration_text.text(calculateDurationTillNow(start_time))



    pause_button.on('click', () => {
        play_button.removeClass('hidden');
        pause_div.removeClass('hidden');
        pause_button.addClass('hidden');
    });


    edit_data.on("click", () => {
        if (form_div.hasClass('hidden')) {
            form_div.removeClass('hidden');
            form_div.prev('div').addClass('hidden');
            edit_data.text('Anuluj')
        } else {
            form_div.addClass('hidden');
            form_div.prev('div').removeClass('hidden');
            edit_data.text('zmień dane')

        }
    });

    let duration_refresh_interval = setInterval(function () {
        let temp_duration_text = calculateDurationTillNow(start_time);
        duration_text.text(temp_duration_text)
    }, 1000);


});

function calculateDurationTillNow(start_time) {
    let now = moment();
    let start_time_temp = moment(start_time.text(), 'YYYY-MM-DD hh:mm:ss');
    let diff = now.diff(start_time_temp);
    let diffDuration = moment.duration(diff);
    let days = diffDuration.days();
    let hours = diffDuration.hours();
    let minutes = diffDuration.minutes();
    let seconds = diffDuration.seconds();
    hours = makeTimeDoubleDigit(hours);
    minutes = makeTimeDoubleDigit(minutes);
    seconds = makeTimeDoubleDigit(seconds);
    return `${days} dni, ${hours}:${minutes}:${seconds}`
}

function makeTimeDoubleDigit(time_value) {
    if (parseInt(time_value) <= 10){
        time_value = '0' + time_value
    }
    return time_value
}