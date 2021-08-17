var data = [];
generateTable();
function generateTable(){
    data = {'month': $('#month').val(),
            'year': $('#year').val(),
            'employee': $('#employee_id').val()};
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

$('#report').on('click', function(e) {
    e.preventDefault();
    console.log($('#month').val())
    var api_url = '/report/api/?id=' + $('#employee_id').val() + '&month='  + $('#month').val() + '&year=' + $('#year').val();
    window.open(api_url);
    return false;
});