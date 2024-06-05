document.addEventListener('DOMContentLoaded', function () {
    var trigger = document.querySelector('[data-bs-toggle="offcanvas"]');
    var offcanvasElement = document.querySelector('.offcanvas');
    var bootstrapOffcanvas = new bootstrap.Offcanvas(offcanvasElement);
  
    trigger.addEventListener('click', function () {
      bootstrapOffcanvas.toggle();
    });
  });

$(document).ready(function() {
    $('#procedure_name').on('change', function() {
        var selectedProcedure = $(this).val(); 
        alert(selectedProcedure)
        $.ajax({
            url: '/get_procedure_content/',
            type: 'GET',
            data: {
                procedure_id: selectedProcedure
            },
            success: function(response) {
                // Update the test_procedures div with the received content
                $('#test_procedure_design').html(response.design_procedures);
                $('#test_procedure_interim').html(response.interim_procedures);
                $('#test_procedure_rollforward').html(response.rollforward_procedures);
            }
        });
    });
});


