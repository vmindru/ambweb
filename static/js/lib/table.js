$(document).ready(function() {

var db =  $('#live').DataTable( {
        "ajax": '/race/json/',
        "paging":   false,
        "info": false,
        "searching": false,
        "ordering": false,
        "rowId": 1,
        "select": true,
        "dom": 'Bfrtip',
        "emptyTable": "No race in progress",
/*        "columns": [
            {"title": "Position"},
            {"title": "Number"},
            {"title": "Laps"},
            {"title": "Lap Time"},
            {"title": "Raced Time"},
            {"title": "Diff"},
            {"title": "Gap"},
            {"title": "Best Lap Time"},
            {"title": "Best Lap"},]
*/
    } );
setInterval (db.ajax.reload, 2000);
} );


