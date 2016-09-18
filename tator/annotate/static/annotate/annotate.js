$(document).ready(function(){

    /* Apply "selected" class to the currently selected option for a form-group
     * (removing from any previously selected option)*/
    function highlightSelected() {
        if (this.checked) {
            $(this).closest(".form-group").find('input[type="radio"]').parent().removeClass("selected");
            $(this).parent().addClass("selected");
        }
    }

    $('input[type="radio"]').change(highlightSelected).each(highlightSelected);


    // Submit annotation button is disabled initially */
    $('#annotation-form button').prop('disabled', true);

    // Enable submit form button when form has been filled out
    $('input[type="radio"]').change(function() {
        if ($('input[type="radio"]:checked').length == 3) {
            $('#annotation-form button').prop('disabled', false);
        }
    });
});
