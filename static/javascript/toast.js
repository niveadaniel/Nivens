function show_toast(toast_type, message){
    if(toast_type){
        toast_type = 'bg-' + toast_type;
        $('.toast-header').addClass(toast_type);
    }
    $('.me-auto').addClass('white');
    $('.toast-body').html('<b>'+ message +'</b>');
    $('.toast').toast('show');
}