//COPY ROLE NAME AND ATTACH TO SUBMIT
$(document).ready(function() {
  // Event listener for changes in the role_name input field
  $('#role_name').on('input', function() {
      // Get the value of the role_name input field
      var roleNameValue = $(this).val();
      
      // Update the value of the assigned_roles hidden field with the value of role_name
      $('#assigned_roles').val(roleNameValue);
      $('#remove_roles').val(roleNameValue);
  });
});


//FIlTER THE PERMISSIONS IN BOTH NOT ASSIGNED AND ASSIGNED GROUP
$(document).ready(function(){
  $('#filter_group').on('input', function() {
      var searchText = $(this).val().toLowerCase();
      $('.permission-row').each(function() {
          var permissionName = $(this).find('label').text().toLowerCase();
          if (permissionName.indexOf(searchText) === -1) {
              $(this).hide();
          } else {
              $(this).show();
          }
      });
  });

  $('#select_all_permission').click(function() {
      var isChecked = $(this).prop('checked');
      $('.permission-row:visible').each(function() {
          $(this).find('input[name="permissions"]').prop('checked', isChecked);
      });
  });

  //MANAGE ASSIGNED PERMISSIONS
  $('#filter_assigned_group').on('input', function() {
    var searchText = $(this).val().toLowerCase();
    $('.permission-row-assigned').each(function() {
        var permissionName = $(this).find('label').text().toLowerCase();
        if (permissionName.indexOf(searchText) === -1) {
            $(this).hide();
        } else {
            $(this).show();
        }
    });
});

  $('#select_all_assigned_permission').click(function() {
    var isChecked = $(this).prop('checked');
    $('.permission-row-assigned:visible').each(function() {
        $(this).find('input[name="assigned_permissions"]').prop('checked', isChecked);
    });
});
});



//VALIDATE IF THE ADMIN FILTER IS COMPLETE
$('#policy_create_form').on('submit', function(event) {
  var selectedItems = $('#admin_role_list_2').val();
  if (selectedItems == null || selectedItems.length === 0) {
      event.preventDefault(); // Prevent form submission
      $('#admin_role_list_2').focus();
      $('#error_message').text('Please select at least one item.').show();
      // You can customize the error message as needed.
  } else {
      $('#error_message').hide();
  }
});

//VALIDATE THE NUMERIC REQUIREMENTS IN TERM DAYS
$(document).ready(function() {
  // Add event listener for keypress event
  $('#termed_days').keypress(function(event) {
      // Get the character code of the pressed key
      var keycode = event.keyCode || event.which;

      // Allow only numeric input (48-57 corresponds to 0-9 keys)
      if (keycode < 48 || keycode > 57) {
          // Prevent default action (typing non-numeric characters)
          event.preventDefault();
      }
  });
});

//SFTP SERVER USERNAME AND PASSWORD VALIDATION
$(document).ready(function() {
  // Add event listener to the username input field
  $('#sftp_username').on('input', function() {
      // Check if the username is not empty
      if ($(this).val().trim() !== '') {
          // Require the user to input password
          $('#sftp_password').prop('required', true);
          $('#sftp_retypepassword').prop('required', true);
      } else {
          // Clear and disable the password fields if username is empty
          $('#sftp_password').val('').prop('required', false);
          $('#sftp_retypepassword').val('').prop('required', false);
      }
  });

  // Add event listener to the password input field
  $('#sftp_password').on('input', function() {
      const password = $(this).val();
      const retypePassword = $('#sftp_retypepassword').val();

      // Check if password is not empty
      if (password.trim() !== '') {
          // Validate if password matches the retyped password
          if (password !== retypePassword) {
              // Show an error message or handle invalid password case
              // For example, you can add a CSS class to highlight the error
              $(this).addClass('is-invalid');
              $('#sftp_retypepassword').addClass('is-invalid');
          } else {
              // Clear error styles if passwords match
              $(this).removeClass('is-invalid');
              $('#sftp_retypepassword').removeClass('is-invalid');
          }
      } else {
          // Clear error styles if password is empty
          $(this).removeClass('is-invalid');
          $('#sftp_retypepassword').removeClass('is-invalid');
      }
  });

  // Add event listener to the retyped password input field
  $('#sftp_retypepassword').on('input', function() {
      const password = $('#sftp_password').val();
      const retypePassword = $(this).val();

      // Validate if password matches the retyped password
      if (password !== retypePassword) {
          // Show an error message or handle invalid password case
          // For example, you can add a CSS class to highlight the error
          $(this).addClass('is-invalid');
          $('#sftp_password').addClass('is-invalid');
      } else {
          // Clear error styles if passwords match
          $(this).removeClass('is-invalid');
          $('#sftp_password').removeClass('is-invalid');
      }
  });
});


// THIS CODE WILL DISABLE THE FOLLOWING FIELDS WHEN SSO IS SELECTED WHEN CREATING PASSWORD
$(document).ready(function() {

    function toggleInput() {
      if ($('#sso').is(':checked')) {
        $('#length').prop('disabled', true);
        $('#age').prop('disabled', true);
        $('#history').prop('disabled', true);
        $('#lockout').prop('disabled', true);
        $('#lockout_duration').prop('disabled', true);
        $('#req_specialchar').prop('disabled', true);
        $('#req_uppercase').prop('disabled', true);
        $('#req_lowercase').prop('disabled', true);
        $('#req_numeric').prop('disabled', true);
      } else {
        $('#length').prop('disabled', false);
        $('#age').prop('disabled', false);
        $('#history').prop('disabled', false);
        $('#lockout').prop('disabled', false);
        $('#lockout_duration').prop('disabled', false);
        $('#req_specialchar').prop('disabled', false);
        $('#req_uppercase').prop('disabled', false);
        $('#req_lowercase').prop('disabled', false);
        $('#req_numeric').prop('disabled', false);
      }
    }

    // Initial call to set input field state on page load
    toggleInput();

    // Event listener for radio button change
    $('input[name="authentication_method"]').change(function() {
      toggleInput();
    });
});

//Triger the Tooltip
$(function () {
  $('[data-toggle="tooltip"]').tooltip({
    trigger: "hover",
  });
});

//Side Bar
$(function () {
  $("#my-link").click(function (e) {
    e.preventDefault();
    // Toggle the visibility of the hidden div
    $("#hidden-div").toggle();
    var hiddenDivWidth = $("#hidden-div").outerWidth();
    // Move the container based on the size of the hidden div
    if ($("#hidden-div").is(":visible")) {
      $("#maincontainer").css("margin-left", "342px");
    } else {
      $("#maincontainer").css("margin-left", "60px");
    }
  });
});

$(function () {
  $("#closeprojnav").click(function (e) {
    e.preventDefault();
    // Toggle the visibility of the hidden div
    $("#hidden-div").toggle();
    var hiddenDivWidth = $("#hidden-div").outerWidth();
    // Move the container based on the size of the hidden div
    if ($("#hidden-div").is(":visible")) {
      $("#main-div").css("margin-left", "342px");
    } else {
      $("#main-div").css("margin-left", "60px");
    }
  });
});

function filterApps() {
  var input, filter, cards, card, appName, i, type;
  input = document.getElementById("searchAPP");
  filter = input.value.toUpperCase();
  cards = document.getElementsByClassName("app-card");

  for (i = 0; i < cards.length; i++) {
    card = cards[i];
    appName = card.getAttribute("data-appname").toUpperCase();
    type = card.getAttribute("data-apptype").toUpperCase();

    if (appName.indexOf(filter) > -1 || type.indexOf(filter) > -1) {
      card.style.display = "";
    } else {
      card.style.display = "none";
    }
  }
}

$("#employeeEdit").on("hidden.bs.modal", function () {
  $(this).find("input").val("");
});

$(document).ready(function () {
  const selectAllCheckbox = $("#select-all-checkbox");
  const checkboxes = $('input[id="user_checkbox"]');
  selectAllCheckbox.on("change", function () {
    checkboxes.prop("checked", selectAllCheckbox.prop("checked"));
  });
  checkboxes.on("change", function () {
    if (!$(this).prop("checked")) {
      selectAllCheckbox.prop("checked", false);
    }
  });
});

$(document).ready(function () {
  $("#passwordHelpLink").on("click", function (event) {
    event.preventDefault(); // Prevent the default link behavior
    $(".passwordHelpText").toggle();
  });
});

$(document).ready(function () {
  $('[data-bs-toggle="popover"]').popover({
    trigger: "click",
  });
});

//This is to open the Modal of the image preview in Process Owner PW Image Upload
$(document).ready(function () {
  $("#openModalLink").click(function () {
    $("#PWConfigModal").modal("show");
  });
});

//This is the close button of the password config preview
$(document).ready(function () {
  var srcValue = $("#image-preview").attr("src");

  // Check if the src value is equal to '/media/pwconfigs/default.png'
  if (srcValue === "/media/pwconfigs/default.png") {
    // Use jQuery to hide the image preview container
    $("#image-preview-container").hide();
  } else {
    $("#image-preview-container").show();
  }
  // Add click event listener to the close button
  $("#closeButton").click(function () {
    // Hide the image when the close button is clicked
    $("#PWScreenshotDelete").modal("show");
  });
});

$(document).ready(function () {
  // Add click event listener to the close button
  $("#confirmDeletePWConfig").click(function () {
    id = $("#selected-app").val();
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      type: "POST",
      url: "/dashboard/my-applications/delete/" + id + "/",
      headers: {
        "X-CSRFToken": csrf_token,
      },

      success: function (data) {
        $("#image-preview").hide();
        // Clear the file input
        const fileInput = document.querySelector('input[type="file"]');
        fileInput.value = "";

        // Optionally, reset the image preview
        imagePreview.src = "";
        modal_imagePreview.src = "";
        imagePreviewContainer.classList.remove("visible");
        modal_imagePreviewContainer.classList.remove("visible");

        $("#PWScreenshotDelete").modal("hide");
      },
      error: function (xhr, status, error) {
        $("#image-preview").hide();
        // Clear the file input
        const fileInput = document.querySelector('input[type="file"]');
        fileInput.value = "";

        // Optionally, reset the image preview
        imagePreview.src = "";
        modal_imagePreview.src = "";
        imagePreviewContainer.classList.remove("visible");
        modal_imagePreviewContainer.classList.remove("visible");

        $("#PWScreenshotDelete").modal("hide");
      },
    });
  });
});

//THIS IT RESTRICT USERS FROM TYPING NON-NUMERIC CHARACTERS
function validateInput(input) {
  // Remove non-numeric characters
  input.value = input.value.replace(/[^0-9]/g, "");
}

//THIS IS TO OPEN THE PASSWORD COMPLIANCE MODAL
$(document).ready(function () {
  var tableName = "#authentication_result_compliant";
  $(tableName).on("click", ".open-modal", function () {
    var userId = $(this).data("process-id");
    $("#PWCompliance").modal("show");
  });
});

$(document).ready(function () {
  var tableName = "#authentication_result_not_compliant";

  $(tableName).on("click", ".open-modal", function () {
    var id = $(this).data("process-id");
    var fullUrl =
      "/myclients/actions/audit/authentication/pwconfigviewer/" + id;
    $.ajax({
      url: fullUrl,
      type: "GET",
      dataType: "json",
      success: function (response) {
        var appDataArray = JSON.parse(response.app_name);
        var appData = appDataArray[0];
        $("#PWConfig_ApplicationName").text(appData.fields.APP_NAME);

        $("#PWConfigViewer .offcanvas-body div").empty();

        var tableHtml =
          '<table class="table" style="font-size:12px; width:100%;">';
        tableHtml +=
          '<thead><tr><th style="width: 33%;">Fields</th><th style="width: 33%;">Current Settings</th><th style="width: 33%;">Policy</th></tr></thead>';
        tableHtml += "<tbody>";

        $.each(response.matched_application_info, function (index, info) {
          // Check if arrays have the same length
          var minArrayLength = Math.min(
            info.non_matching_fields.length,
            info.configured_passwords.length,
            info.required_passwords.length
          );

          for (var i = 0; i < minArrayLength; i++) {
            tableHtml += "<tr>";
            tableHtml +=
              '<td style="width: 33%;">' +
              info.non_matching_fields[i] +
              "</td>";
            var configuredSettings =
              info.configured_passwords[i] === true
                ? "Enabled"
                : info.configured_passwords[i] === false
                ? "Not Enabled"
                : info.configured_passwords[i];
            tableHtml +=
              '<td style="width: 33%;">' + configuredSettings + "</td>";
            var requiredSettings =
              info.required_passwords[i] === true
                ? "Enabled"
                : info.required_passwords[i] === false
                ? "Not Enabled"
                : info.required_passwords[i];
            tableHtml +=
              '<td style="width: 33%;">' + requiredSettings + "</td>";
            tableHtml += "</tr>";
          }
        });

        tableHtml += "</tbody></table>";

        // Append the table to the offcanvas body
        $("#PWConfigViewer .offcanvas-body div").append(tableHtml);

        $("#PWConfigViewer").offcanvas("show");
      },
    });
  });
});

$(document).ready(function () {
  var newUserApprovalLink = $("#app_new_user_approval_link");
  var offcanvasElement = $("#app_user_new_approval");
  newUserApprovalLink.click(function (event) {
    event.preventDefault();
    offcanvasElement.offcanvas("toggle");
  });
});

$(document).ready(function () {
  $("#new_user_date_approved").datepicker({
    format: "mm/dd/yyyy",
    autoclose: true,
    orientation: "bottom", // Set orientation to bottom
  });
  // Adjust the position of the datepicker container when it is shown
  $("#new_user_date_approved").on("show", function () {
    $(".datepicker-dropdown").css({
      marginTop: "45px", // Adjust the value as needed
    });
  });
});

//THIS IS THE CODE TO POPULATE THE APPROVER1 TITLE
$(document).ready(function () {
  $("#approver1").change(function () {
    var selectedOption = $(
      '#approver1_list option[value="' + $(this).val() + '"]'
    );

    // Check if the option exists and extract data-user-id attribute
    if (selectedOption.length > 0) {
      var id = selectedOption.data("user-id");
      $("#approver1_title").val("");
      $.ajax({
        url: "/get_approver1_job_title/" + id + "/",
        type: "GET",
        dataType: "json",
        success: function (data) {
          $("#approver1_title").val(data.job_title);
        },
        error: function (error) {
          console.log("Error:", error);
        },
      });
    } else {
      console.log("No user selected");
    }
  });
});

//THIS IS THE CODE TO POPULATE THE APPROVER2 TITLE
$(document).ready(function () {
  $("#approver2").change(function () {
    var selectedOption = $(
      '#approver2_list option[value="' + $(this).val() + '"]'
    );

    // Check if the option exists and extract data-user-id attribute
    if (selectedOption.length > 0) {
      var id = selectedOption.data("user-id");
      $("#approver2_title2").val("");
      $.ajax({
        url: "/get_approver2_job_title/" + id + "/",
        type: "GET",
        dataType: "json",
        success: function (data) {
          $("#approver2_title2").val(data.job_title);
        },
        error: function (error) {
          console.log("Error:", error);
        },
      });
    } else {
      console.log("No user selected");
    }
  });
});

$(document).ready(function () {
  // Assuming you have an input field with type="file" to handle file uploads
  $("#id_file_name").on("change", function (e) {
    var fileInput = e.target;
    var file = fileInput.files[0];

    // Update the file name and size in the manual upload section
    $("#file_upload_user_approval").text(
      file.name + " (" + formatFileSize(file.size) + ")"
    );

    // Update the file type, file name, size, and corresponding icon in the preview section
    updateFilePreview(file.name, file.size);
  });

  function updateFilePreview(fileName, fileSize) {
    var filePreviewContainer = $("#file-preview");
    var closeButton = $("#closeButton");
    var openModalLink = $("#openModalLink");

    // Extract the file extension from the file name
    var fileExtension = fileName.split(".").pop().toLowerCase();

    // Update file type and icon based on the file extension
    var fileType, iconClass;
    if (fileExtension === "pdf") {
      fileType = "PDF";
      iconClass = "fas fa-file-pdf";
    } else if (fileExtension === "csv") {
      fileType = "CSV";
      iconClass = "fas fa-file-csv";
    } else if (fileExtension === "jpg" || fileExtension === "jpeg") {
      fileType = "Image";
      iconClass = "fas fa-file-image";
    } else {
      // Default to generic file type if the extension is not recognized
      fileType = "File";
      iconClass = "fas fa-file";
    }

    // Update the file type, icon, and size in the preview container
    filePreviewContainer.find("i").attr("class", iconClass);
    openModalLink.attr("title", "Click to preview " + fileType);
    closeButton.attr("aria-label", "Close " + fileType);

    // Add file size information at the bottom
    filePreviewContainer
      .find("#file-size")
      .text("File Size: " + formatFileSize(fileSize));
  }

  function formatFileSize(size) {
    var units = ["B", "KB", "MB", "GB", "TB"];
    var i = 0;
    while (size >= 1024 && i < units.length - 1) {
      size /= 1024;
      i++;
    }
    return size.toFixed(2) + " " + units[i];
  }
});

//PROCESS OWNER: NEW USER LIST: THIS IS TO ASSIGN THE ID TO HIDDEN FIELD

$(document).ready(function () {
  // Event listener for selection change
  $("#approver1").change(function () {
      // Get the selected option
      var selectedOption = $("#approver1_list option[value='" + $(this).val() + "']");
      
      // Get the data-user-id attribute value
      var userId1 = selectedOption.data("user-id");
      
      // Set the value to the hidden input
      $("#approver1_id").val(userId1);
  });

  $("#approver2").change(function () {
      // Get the selected option
      var selectedOption = $("#approver2_list option[value='" + $(this).val() + "']");
      
      // Get the data-user-id attribute value
      var userId2 = selectedOption.data("user-id");
      
      // Set the value to the hidden input
      $("#approver2_id").val(userId2);
  });

  $("#app_list_app_owners").change(function () {
    // Get the selected option
    var selectedOption = $("#app_owner_list option[value='" + $(this).val() + "']");
    
    // Get the data-user-id attribute value
    var userId3 = selectedOption.data("user-id");
    
    // Set the value to the hidden input
    $("#app_list_app_owner1").val(userId3);
});
});