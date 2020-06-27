$(document).ready(function() {
  
var race =  $('#race').DataTable( {
        "drawCallback": function(settings) {
            json_data = settings.json
            if ( json_data){
            $('#heat_id').text("Race: "+json_data.heat_id)
            $('#race_time').text("Race Time: "+json_data.heat_duration)
            $('#race_start').text("Race Start: "+json_data.heat_start)
            $('#race_end').text("Race End: "+json_data.heat_end)
            }
         },
        "ajax": {"url": $("#AjaxJsonUrl").val()},
        "paging": false,
        "info": false,
        "searching": false,
        "ordering": true,
        "order": [[ 7, 'asc' ]],
        "rowId": 1,
        "select": true,
        "emptyTable": "No race in progress",
        "columns": [
          {"title": "Position", "orderable": false},
          {"title": "Number", "orderable": false},
          {"title": "Laps", "orderable": false},
          {"title": "Lap Time", "orderable": false},
          {"title": "Raced Time", "orderable": false},
          {"title": "Diff", "orderable": false},
          {"title": "Gap", "orderable": false},
          {"title": "Best Lap Time", "orderable": true},
          {"title": "Best Lap", "orderable": false},],
    } );
    race.on( 'order.dt search.dt', function () {
    race.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
        cell.innerHTML = i+1;
    } );
} ).draw();
    setInterval (race.ajax.reload, 2000)
} );


