function getNumberOfLabels() {
    var names = $( "div.label_item input" ).map(function() {
        return $(this).attr("name")
    })
    names = names.get()

    var max = 0
    for (var i=0; i < names.length; i++) {
        name = names[i]
        if (name.includes("label_key_")) {
            var number = name.replace("label_key_", "")
            number = parseInt(number)

            if (number > max) {
                max = number
            }
        }
    }

    return max
}

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

function createDatePicker(selector) {
    var value = $(selector).val()
    $(selector).datepicker()
    $(selector).datepicker("option", "dateFormat", "yy-mm-dd")
    $(selector).val(value)
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

    $( "div.labels_buttons input[type=button][name=add]" ).click(function() {
        var numberOfLabels = getNumberOfLabels()
        var html = `
            <div class="label_item">
                <input type="text" name="label_key_number" placeholder="key"/>
                =
                <input type="text" name="label_value_number" placeholder="value"/>
            </div>
        `
        html = html.replace(/number/g, numberOfLabels + 1)

        $( "div.labels" ).append(html)
    })

    $( "div.labels_buttons input[type=button][name=remove]" ).click(function() {
        var numberOfLabels = getNumberOfLabels()

        if (numberOfLabels > 0) {
            var selector = "input[name=label_key_" + numberOfLabels + "]"
            $( selector ).parents("div.label_item").remove()
        }
    })

    showTextareaOrFile()

    var datePickerFormat = "yy-mm-dd"
    
    createDatePicker("#minImportTime")
    createDatePicker("#maxImportTime")
    createDatePicker("#minTimeDate")
    createDatePicker("#maxTimeDate")
});
