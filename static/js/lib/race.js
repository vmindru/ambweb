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
//       "ajax": {"url": "/race/json/"+$("#HeatId").val()},
        "ajax": {"url": $("#AjaxJsonUrl").val()},
        "paging": false,
        "info": false,
        "searching": false,
        "ordering": false,
        "rowId": 1,
        "select": true,
        "emptyTable": "No race in progress",
        "messageBottom": "TEST",
        "columns": [
          {"title": "Position"},
          {"title": "Number"},
          {"title": "Name"},
          {"title": "Laps"},
          {"title": "Lap Time"},
          {"title": "Raced Time"},
          {"title": "Diff"},
          {"title": "Gap"},
          {"title": "Best Lap Time"},
          {"title": "Best Lap"},],
    } );
    setInterval (race.ajax.reload, 2000)
} );


