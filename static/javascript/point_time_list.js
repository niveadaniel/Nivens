var data = [];
generateTable();
function generateTable(){
    data = {'month': $('#month').val(),
            'year': $('#year').val(),
            'employee': $('#employee_id').val()};
    console.log(data);
    datatable_ticket = $('#data_table').DataTable({
            "destroy": true,
            "fixedHeader": false,
            "ordering": false,
            "processing": true,
            "serverSide": true,
            "ajax":{
                    url: "/api/list_point_time/",
                    type: "GET",
                    data: data,
                    complete: function(response){
                        $(".scrollbar-table").floatingScroll();
                    }
            },
            "paging": false,
            "ordering": false,
            "info": false,
            "searching": false,

    });
}

$('#month').change(function(){
    generateTable();
});