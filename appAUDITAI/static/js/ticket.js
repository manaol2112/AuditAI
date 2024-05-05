$(document).ready(function() {
    $('#request_type').change(function() {
        var selectedValue = $(this).val();
        var teamMemberLabel = $('#team_member_label');
        var teamMemberDropdown = $('#team_member');
        var approverLabel = $('#approver_label');
        var approverDropdown = $('#access_approver');

        // Reset display for all elements
        teamMemberLabel.hide();
        teamMemberDropdown.hide();
        approverLabel.hide();
        approverDropdown.hide();

        // Show relevant elements based on selection
        if (selectedValue == 'supervisor' || selectedValue == 'team_member') {
            teamMemberLabel.show();
            teamMemberDropdown.show();
        }
        if (selectedValue == 'own_access') {
            approverLabel.show();
            approverDropdown.show();
        }
    });
});


