function showTextareaOrFile(effect) { 
    var type = $( "#junit_import_form input:radio[name=type]:checked" ).val()

    if (type == "text") {
        $( "#junit_import_form input[type=file]" ).hide(effect)
        $( "#junit_import_form textarea" ).show(effect)
    }

    if (type == "file") {
        $( "#junit_import_form textarea" ).hide(effect)
        $( "#junit_import_form input[type=file]" ).show(effect)
    }
}

function showConfirmationDialog(title, text, f) {
    $( "#dialog" ).attr("title", title)
    $( "#dialog > p" ).text(text)
    $( "#dialog" ).dialog({
        modal: true,
        buttons: {
            "Ok" : function() {
                $( this ).dialog( "close" );
                f();
            },
            "Cancel" : function() {
                $( this ).dialog( "close" );
            }
        }
    })
}

$(document).ready(function(){
    $( ".test_run_body" ).hide()

    $( ".test_run_header" ).click(function(event) {
        $(this).siblings(".test_run_body").toggle("fast");
    })

    $( ".test_run_delete_button" ).click(function(event) {
        var id = $(this).parents(".test_run").children("input[name=id]").attr("value")
        var testRunDiv = $(this).parents(".test_run")
        var rootUrl = $("#root_url").attr("value")
        
        showConfirmationDialog("Delete test run", "Do you really want to delete test run: " + id, function() {
            $.ajax({
                url: rootUrl + "api/delete/" + id,
                method: "DELETE"
            }).done(function() {
                testRunDiv.remove()
            })
        })
    })

    $( "#junit_import_form input[name=type]" ).change(function() {
        showTextareaOrFile("slow")
    })

    showTextareaOrFile()
});
