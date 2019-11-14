$(document).ready(function() {
var race =  $('#race').DataTable( {
        "ajax": '/race/json/',
        "paging":   false,
        "info": false,
        "searching": false,
        "ordering": false,
        "rowId": 1,
        "select": true,
        "dom": 'Bfrtip',
        "emptyTable": "No race in progress",
        "columns": [
          {"title": "Position"},
          {"title": "Number"},
          {"title": "Laps"},
          {"title": "Lap Time"},
          {"title": "Raced Time"},
          {"title": "Diff"},
          {"title": "Gap"},
          {"title": "Best Lap Time"},
          {"title": "Best Lap"},]

    } );

var qualy =  $('#qualy').DataTable( {
        "ajax": '/race/json/',
        "paging":   false,
        "info": false,
        "searching": false,
        "ordering": false,
        "rowId": 1,
        "select": true,
        "dom": 'Bfrtip',
        "emptyTable": "No race in progress",
        "columns": [
          {"title": "Position"},
          {"title": "Number"},
          {"title": "Laps"},
          {"title": "Lap Time"},
          {"title": "Raced Time"},
          {"title": "Diff"},
          {"title": "Gap"},
          {"title": "Best Lap Time"},
          {"title": "Best Lap"},]
    } );

if ( $( "#qualy" ).length ) {
    setInterval (qualy.ajax.reload, 2000);
}

if ( $( "#race" ).length ) {
    setInterval (race.ajax.reload, 2000);
    console.log(race)
}
} );


