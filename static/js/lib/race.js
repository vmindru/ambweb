$(document).ready(function() {
var db =  $('#live').DataTable( {
        "ajax": '/race/json/',
        "paging":   false,
        "info": false,
        "searching": false,
        "ordering": false,
        "stateSave": true,
        "rowId": 1,
        "select": true,
        "dom": 'Bfrtip',
        "language": {
           "emptyTable": "No race in progress"
    }
    } );
setInterval (db.ajax.reload, 2000);

/*$('#live')
    .on( 'mousedown', 'td', function () {
        var rowIdx = db.cell(this).index().row;
        $( db.row( rowIdx ).nodes() ).toggleClass( 'highlight' );
    } );
*/


} );


