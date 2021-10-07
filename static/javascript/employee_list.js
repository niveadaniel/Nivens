var data = [];
generateTable();
function generateTable(){
    data = {'department': $('#department').val()};
    console.log(data);
    datatable_ticket = $('#data_table').DataTable({
            "destroy": true,
            "fixedHeader": false,
            "ordering": false,
            "processing": true,
            "serverSide": true,
            "ajax":{
                    url: "/api/list_employee/",
                    type: "GET",
                    data: data,
                    complete: function(response){
                        $(".scrollbar-table").floatingScroll();
                    }
            },
            "iDisplayLength": 50,
            "bJQueryUI": false,
            "language": {
                "lengthMenu": "Mostrando _MENU_ registros por página.",
                "zeroRecords": "Não foram encontrados registros",
                "info": "Exibindo _START_ até _END_ de um total de _TOTAL_ funcionários",
                "infoEmpty": "Não foram encontrados registros",
                "infoFiltered": "(filtrados de um total de _MAX_ funcionários)",
                "paginate": {
                    "first": "Primeiro",
                    "last": "Último",
                    "next": "Próximo",
                    "previous": "Anterior"
                },
                "search": "Buscar:"
            }

    });
}

$('#department').change(function(){
    generateTable();
});

$(document).on('click', 'a[notification-modal]', function(e) {
    e.preventDefault();
    swal({
        title: "Atenção",
        text: "Você realmente deseja deletar o funcionário?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
            swal("Funcionário excluido com sucesso!", {
              icon: "success",
            });
            location.href = $(this).attr('href');
        }
    });
});