$(document).ready(function(){
    $('#cell_phone').mask('(99)99999-9999');

    $('.save-employee-form').submit(function(e){
        e.preventDefault();
        $form = $('.save-employee-form');
        var form = document.getElementById('save-employee-form');
        var formData = new FormData(form);
        $.ajax({
            type: $form.attr('method'),
            url: $form.attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function(data){
                if (data.success){
                    location.href = '/list/';
                }
                else{
                    alert(data.message);
                }
            }
        });
    });

});