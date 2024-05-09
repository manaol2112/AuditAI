// Triggering change event using jQuery
//$('#applications_select').val('newValue').trigger('change');

$(document).ready(function() {

    $('#access_approver').next(".select2-container").hide();
    $('#approver_label').hide()
    $('#team_member_select').next(".select2-container").hide();
    $('#team_member_label').hide()
});

// Attaching an event listener for the change event
$('#applications_select').on('change', function() {
    var selectedAppId = $(this).val();
    $.ajax({
        url: '/access-request/get_roles/',  // URL to your Django view
        method: 'GET',
        data: {
            'app_id': selectedAppId
        },
        success: function(data) {
            // Populate roles_select dropdown with retrieved roles
            $('#roles_select').empty().append($('<option>', {
                value: '',
                text: '',
                disable: true,
            }));
            $.each(data.roles, function(index, role) {
                $('#roles_select').append($('<option>', {
                    value: role.ROLE_NAME,
                    text: role.ROLE_NAME
                }));
            });
        },
        error: function(xhr, status, error) {
            console.error('Error fetching roles:', error);
        }
    });
});

$('#request_type').on('change', function() {

    var selectedValue = $(this).val();
    if (selectedValue === "supervisor") {
        $('#team_member_select').next(".select2-container").show();
        $('#team_member_label').show();
        $('#access_approver').next(".select2-container").hide();
        $('#approver_label').hide();

    } else if (selectedValue === "own_access") {
        $('#team_member_select').next(".select2-container").hide();
        $('#team_member_label').hide();
        $('#access_approver').next(".select2-container").show();
        $('#approver_label').show();


    } else if (selectedValue === "team_member") {
        $('#team_member_select').next(".select2-container").show();
        $('#team_member_label').show();
        $('#access_approver').next(".select2-container").hide();
        $('#approver_label').hide();

    }
});

  
