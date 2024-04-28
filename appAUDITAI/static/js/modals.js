//OPEN MODAL TO CONFIRM THE USER TYPE UPDATE

$(document).ready(function() {
  $('#selected_user_type').on('click', '.dropdown-item', function() {
    // Check if any checkboxes are selected
    if ($('#app_user_unmapped_table tbody input[name="user_checkbox"]:checked').length > 0) {
      var selectedText = $(this).text();
      $('#confirm_update_type_display').html('This will classify selected users as <strong>' + selectedText + '</strong>. Click confirm button to proceed.');
      $("#update_user_type_modal").modal("show");
    } else {
      // Show a message or perform some action if no checkboxes are selected
      $('#confirm_update_type_display_error').html('Please select at least one user before proceeding.');
      $("#update_user_type_modal_error").modal("show");
    }
  });
});
