$(document).ready(function () {
    // Initialize Select2 for both dropdowns
    $('#team_member_select').select2();
    $('#access_approver').select2();

    // Hide both Select2 dropdowns
    $('#team_member_select').next(".select2-container").hide();
    $('#access_approver').next(".select2-container").hide();

    // Listen for change in request type
    $('#request_type').change(function () {
        var selectedValue = $(this).val();

        // Hide all Select2 dropdowns
        $('.select2-container').hide();

        // Show relevant dropdown based on selection
        if (selectedValue == 'supervisor' || selectedValue == 'team_member') {
            $('#team_member_select').next(".select2-container").show();
        }
        if (selectedValue == 'own_access') {
            $('#access_approver').next(".select2-container").show();
        }
    });
});

$(document).ready(function(){

    $('#applications_select').on("select2:select", function(e) { 
        console.log($(this).val());
        alert('hahaha')
    });

    $('#applications_select').change(function(){
        var selectedApp = $(this).val();
        $.ajax({
            type: 'GET',
            url: '/get_roles/',
            data: {
                'app_name': selectedApp
            },
            success: function(data){
                $('#roles_select').empty();
                $('#roles_select').append('<option value="" selected disabled></option>');
                $.each(data, function(key, value){
                    $('#roles_select').append('<option value="'+ value +'">'+ value +'</option>');
                });
            }
        });
    });
});
