$(document).ready(()=> {
    let start_time_field = $('#id_start_time');
    let end_time_field = $('#id_end_time');

    console.log(start_time_field)
    console.log(start_time_field.type);
    start_time_field.type = 'datetime-local';




    // pause_button.on('click', ()=>{
    //     play_button.removeClass('hidden');
    //     pause_div.removeClass('hidden');
    //     pause_button.addClass('hidden');
    // });
    //
    // play_button.on('click', ()=>{
    //     play_button.addClass('hidden');
    //     pause_div.addClass('hidden');
    //     pause_button.removeClass('hidden');
    // });
    //
    // stop_button.on("click", (e)=>{
    //     if (counter ===0){
    //         e.preventDefault()
    //         counter++
    //     }else{
    //         this.trigger("click")
    //     }
    // });
    //
    // edit_data.on("click", ()=>{
    //     if (form_div.hasClass('hidden')){
    //         form_div.removeClass('hidden');
    //         form_div.prev('div').addClass('hidden');
    //         edit_data.text('Anuluj')
    //     } else {
    //         form_div.addClass('hidden');
    //         form_div.prev('div').removeClass('hidden');
    //         edit_data.text('zmień dane')
    //
    //     }
    // });




});
