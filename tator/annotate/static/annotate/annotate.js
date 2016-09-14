$(document).ready(function(){

    $('input[type="radio"]').change(function() {
        if(this.checked) {
            $(this).closest(".form-group").find('input[type="radio"]').parent().removeClass("selected");
            $(this).parent().addClass("selected");
        }
    });

});
