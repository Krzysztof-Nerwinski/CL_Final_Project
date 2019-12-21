$(document).ready(()=> {
    let edit_btn = $('.btn-warning');

    edit_btn.on('click', function (e){
        if ($(this).parent().prev().prev('.col-2').text() === 'Timer aktywny') {
            e.preventDefault();
            alert('Nie możesz edytować aktywnego timera')
        }
    })


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
