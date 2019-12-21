$(document).ready(() => {
    let pause_button = $('#pause_button');
    let play_button = $('#play_button');
    let pause_div = $('#pause_counter');
    let edit_data = $('#edit_data');
    let form_div = $('#edit_timer');
    let start_time = $('#start_time');
    let duration_text = $('#timer_duration');
    let timer_id = $('#timer_id');
    let pause_duration = $('#timer_pause_duration')
    let pause_from = $('#timer_pause_from')
    moment.locale('pl');

    insertDurationTime(duration_text,start_time,pause_duration)

    if (pause_div.hasClass('hidden')) {
        let duration_refresh_interval = setInterval(() => {
            duration_text.text(calculateDurationTillNow(start_time, pause_duration));
        }, 1000);
    }

    play_button.on('click', () => {
        $.ajax({
        url: `/timer/unpause/${timer_id.text()}`,
        type: "GET",
        success: function (data) {
            if (data.error_info) {
                alert(data.error_info)
            } else {
                play_button.addClass('hidden');
                pause_div.addClass('hidden');
                pause_button.removeClass('hidden');
                pause_duration.text(data.pause_duration);
                let duration_refresh_interval = setInterval(() => {
                    duration_text.text(calculateDurationTillNow(start_time, pause_duration));
                }, 1000);
            }
        },
        error: function (data) {
            console.log('Bład serwera')
        }
        })
    });

    pause_button.on('click', () => {
        $.ajax({
        url: `/timer/pause/${timer_id.text()}`,
        type: "GET",
        success: function (data) {
            if (data.error_info) {
                alert(data.error_info)
            } else {
                play_button.removeClass('hidden');
                pause_div.removeClass('hidden');
                pause_button.addClass('hidden');
                pause_from.text(data.pause_from.getDate);
                clearInterval(duration_refresh_interval)
            }
        },
        error: function (data) {
            console.log('Bład serwera')
        }
        })

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


});

function insertDurationTime(duration_text,start_time,pause_duration) {
    duration_text.text(calculateDurationTillNow(start_time, pause_duration));
}

function calculateDurationTillNow(started_on, pause_duration = null) {
    let now = moment();
    if (pause_duration != null) {
        pause_duration = moment.duration(pause_duration.text())
        now = now.subtract(pause_duration)
    }
    let start_time_temp = moment(started_on.text(), 'YYYY-MM-DD hh:mm:ss');
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
    if (parseInt(time_value) < 10){
        time_value = '0' + time_value
    }
    return time_value
}
