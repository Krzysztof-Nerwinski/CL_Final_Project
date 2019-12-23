moment.locale('pl');

$(document).ready(() => {
    let pause_button = $('#pause_button');
    let play_button = $('#play_button');
    let pause_div = $('#pause_counter');
    let stop_button = $('#stop_button');
    let edit_data = $('#edit_data');
    let form_div = $('#edit_timer');
    let start_time = $('#start_time');
    let duration_text = $('#timer_duration');
    let timer_id = $('#timer_id');
    let pause_duration = $('#timer_pause_duration');
    let pause_from = $('#timer_pause_from');

    if (pause_div.hasClass('hidden')) {
        insertDurationTime(duration_text, start_time, pause_duration, null);
    } else {
        insertDurationTime(duration_text,start_time, pause_duration, pause_from);
    }

    let duration_refresh_interval = timerStartStop(pause_div, duration_text, start_time, pause_duration);

    stop_button.on("click", function (e) {
        e.preventDefault();
        confirmationDialog($(this))
    });

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
                    duration_refresh_interval = timerStartStop(pause_div, duration_text, start_time, pause_duration)
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
                    let data_pause_from = moment(data.pause_from).format( 'YYYY-MM-DD HH:mm:ss');
                    pause_from.text(data_pause_from);
                    timerStartStop(pause_div, duration_text, start_time, pause_duration, duration_refresh_interval)
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

function insertDurationTime(duration_text, start_time, pause_duration, pause_from) {
    if (pause_duration === null) {
        duration_text.text(calculateDurationTillNow( start_time,null, pause_from))
    } else {
        duration_text.text(calculateDurationTillNow(start_time, pause_duration, null));
    }
}

function calculateDurationTillNow(started_on, pause_duration, pause_from = null) {
    started_on = moment(started_on.text(), 'YYYY-MM-DD HH:mm:ss');
    let diff = undefined;
    let now = moment();
    pause_duration = moment.duration(pause_duration.text());
    if (pause_from === null) {
        now = now.subtract(pause_duration);
        diff = now.diff(started_on);
    } else {
        pause_from = moment(pause_from.text());
        pause_from = pause_from.subtract(pause_duration)
        diff = pause_from.diff(started_on)
    }
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
    if (parseInt(time_value) < 10) {
        time_value = '0' + time_value
    }
    return time_value
}


function confirmationDialog(button) {
    let confirmation = confirm("Czy na pewno chcesz zatrzymać timer?");
    if (confirmation === true) {
        window.location = button.children('a').attr('href')
    }
}

function timerStartStop(pause_div, duration_text, start_time, pause_duration, duration_refresh_interval = null) {
    if (duration_refresh_interval === null) {
        let duration_refresh_interval = setInterval(() => {
            duration_text.text(calculateDurationTillNow(start_time, pause_duration));
        }, 1000);
        return duration_refresh_interval
    } else {
        clearInterval(duration_refresh_interval)
    }
}