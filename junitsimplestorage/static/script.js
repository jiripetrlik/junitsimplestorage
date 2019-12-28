$(document).ready(function(){
    $( ".test_run_body" ).hide()

    $( ".test_run_header" ).click(function(event) {
        $(this).siblings(".test_run_body").toggle("fast");
    })
});
