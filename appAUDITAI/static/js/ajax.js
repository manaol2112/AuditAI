$("#employeelist tbody").on("click", "a", function (event) {
  event.preventDefault();
  var id = $(this).data("process-id");
  $.ajax({
    url: "/employeerecord/" + id,
    type: "GET",
    dataType: "json",
    success: function (response) {
      var form = $("#employee_form");
      form
      .find("#first_name")
      .text(response.employeeform_update.FIRST_NAME);
      form
      .find("#last_name")
      .text(response.employeeform_update.LAST_NAME);
      form
      .find("#email_address")
      .val(response.employeeform_update.EMAIL_ADDRESS);

      //Set the background color of the badge
      var statusLabel = form.find("#status")
      var badgeColor = form.find("#badgecolor")
      if (response.employeeform_update.STATUS === 'ACTIVE'){
        statusLabel.text('ACTIVE')
        badgeColor.removeClass("badge bg-danger rounded-pill text-bg-danger")
        badgeColor.addClass("badge bg-success rounded-pill text-bg-success")
      } else {
        statusLabel.text(response.employeeform_update.STATUS)
        badgeColor.removeClass("badge bg-success rounded-pill text-bg-success")
        badgeColor.addClass("badge bg-danger rounded-pill text-bg-danger")
      }

      form
      .find("#user_id")
      .text("(" + response.employeeform_update.USER_ID + ")") ;

      form
      .find("#job_title")
      .val(response.employeeform_update.JOB_TITLE) ;

      form
      .find("#department")
      .val(response.employeeform_update.DEPARTMENT) ;

      form
      .find("#manager")
      .val(response.employeeform_update.MANAGER) ;

      form
      .find("#employee_type")
      .val(response.employeeform_update.EMP_TYPE) ;

      if (response.employeeform_update.HIRE_DATE === '1900-01-01') {
        $("#date_hired").val();
      } else {
        var hireDate = response.employeeform_update.HIRE_DATE;
        var parts1 = hireDate.split('-');
        if (parts1.length === 3) {
            var hireformattedDate = parts1[1] + '/' + parts1[2] + '/' + parts1[0];
            $("#date_hired").val(hireformattedDate);
        } ;
      }
     
      if(response.employeeform_update.TERMINATION_DATE === '1900-01-01') {
        $("#termed_hired").val()
      } else {
        var termedDate = response.employeeform_update.TERMINATION_DATE; 
        var parts2 = termedDate.split('-');
        if (parts2.length === 3) {
            var termedformattedDate = parts2[1] + '/' + parts2[2] + '/' + parts2[0];
            $("#date_termed").val(termedformattedDate);
        } ;
      }
      $("#employeeEdit").modal("show");
    },
    error: function (jqXHR, textStatus, errorThrown) {
      var errorMessage = "An error occurred while fetching employee data.";
      try {
        var responseJson = JSON.parse(jqXHR.responseText);
        if (responseJson && responseJson.error) {
          errorMessage = responseJson.error;
        }
      } catch (e) {
      }
      alert(errorMessage);
    }
  });
});


$("#mapped_users tbody").on("click", "a", function (event) {
  event.preventDefault();

  var id = $(this).data("process-id");
  $.ajax({
    url: "/application-details/" + id,
    type: "GET",
    dataType: "json",
    
    success: function (response) {
      var form = $("#mapped_user_form");
      form
      .find("#first_name")
      .text(response.hr_mapping.FIRST_NAME);
      form
      .find("#last_name")
      .text(response.hr_mapping.LAST_NAME);
      form
      .find("#email_address")
      .val(response.hr_mapping.EMAIL_ADDRESS);

      //Set the background color of the badge
      var statusLabel = form.find("#status")
      var badgeColor = form.find("#badgecolor")
      if (response.hr_mapping.STATUS === 'ACTIVE'){
        statusLabel.text('ACTIVE')
        badgeColor.removeClass("badge bg-danger rounded-pill text-bg-danger")
        badgeColor.addClass("badge bg-success rounded-pill text-bg-success")
      } else {
        statusLabel.text(response.hr_mapping.STATUS)
        badgeColor.removeClass("badge bg-success rounded-pill text-bg-success")
        badgeColor.addClass("badge bg-danger rounded-pill text-bg-danger")
      }

      form
      .find("#user_id")
      .text("(" + response.hr_mapping.USER_ID + ")") ;

      form
      .find("#job_title")
      .val(response.hr_mapping.JOB_TITLE) ;

      form
      .find("#department")
      .val(response.hr_mapping.DEPARTMENT) ;

      form
      .find("#manager")
      .val(response.hr_mapping.MANAGER) ;

      form
      .find("#employee_type")
      .val(response.hr_mapping.EMP_TYPE) ;

      if (response.hr_mapping.HIRE_DATE === '1900-01-01') {
        $("#date_hired").val();
      } else {
        var hireDate = response.hr_mapping.HIRE_DATE;
        var parts1 = hireDate.split('-');
        if (parts1.length === 3) {
            var hireformattedDate = parts1[1] + '/' + parts1[2] + '/' + parts1[0];
            $("#date_hired").val(hireformattedDate);
        } ;
      }
     
      if(response.hr_mapping.TERMINATION_DATE === '1900-01-01') {
        $("#termed_hired").val()
      } else {
        var termedDate = response.hr_mapping.TERMINATION_DATE; 
        var parts2 = termedDate.split('-');
        if (parts2.length === 3) {
            var termedformattedDate = parts2[1] + '/' + parts2[2] + '/' + parts2[0];
            $("#date_termed").val(termedformattedDate);
        } ;
      }
      
      $("#mapped_user_modal").modal("show");
    },
    error: function (jqXHR, textStatus, errorThrown) {
      var errorMessage = "An error occurred while fetching employee data.";
      try {
          var responseJson = JSON.parse(jqXHR.responseText);
          if (responseJson && responseJson.error) {
              errorMessage = responseJson.error;
          }
      } catch (e) {
      }
      alert(errorMessage);
  }
});
});

$("#mapped_users tbody").on("click", "a", function (event) {
  event.preventDefault();
  var email_add = $(this).data("process-id");
  $.ajax({
    url: "/application-details/" + email_add,
    type: "GET",
    dataType: "json",
    success: function (response) {
      console.log(response); // Check the structure of the response in the browser console
      var form = $("#mapped_user_form");
      form.find("#first_name").text(response.mapped_user.FIRST_NAME); // Update according to the actual structure of mapped_user
      $("#mapped_user_modal").modal("show");
    },
    error: function (jqXHR, textStatus, errorThrown) {
      var errorMessage = "An error occurred while fetching employee data.";
      try {
        var responseJson = JSON.parse(jqXHR.responseText);
        if (responseJson && responseJson.error) {
          errorMessage = responseJson.error;
        }
      } catch (e) {
        // Handle parsing error
      }
      alert(errorMessage);
    }
  });
});

//THIS CODE WILL UPDATE THE SELECTED USER TYPE AS TO INTEGRATION, SYSTEM ACCOUNT, REGULAR USER
$(document).ready(function() {
  var id;  
  $('input[name="user_checkbox"]').on('click', function() {
    id = $(this).val();
  });

  $('#selected_user_type li a.dropdown-item').on('click', function() {
    $('#selected_user_type li a.dropdown-item').removeClass('active');
    $(this).addClass('active');
  });

  $('#confirm_usertype').on('click', function(event) {
    event.preventDefault();
    var checkedRecords = [];
    $('input[name="user_checkbox"]:checked').each(function() {
      id = $(this).val();
      checkedRecords.push(id);
    });

    var selectedType = $('#selected_user_type li a.dropdown-item.active').attr('name');
    var csrf_token = $('input[name=csrfmiddlewaretoken]').val()

    // Send an Ajax request to update the user types
    $.ajax({
      url: '/update-user-type/' + id,
      type: 'POST',
      headers: {
        'X-CSRFToken': csrf_token,
      },
      contentType: 'application/json; charset=UTF-8',
      data:JSON.stringify({
      'checkedRecords': checkedRecords,
      'selected_type': selectedType,
      //'csrfmiddlewaretoken': csrf_token,
      }),
      success: function(response) {
        // Handle the success response if needed
        console.log(checkedRecords),
        console.log(selectedType)
        console.log(response);
        location.reload(true);
      },
      error: function(error) {
        // Handle the error response if needed
        console.error(error);
        $("#update_user_type_modal").modal("hide");
      }
    });
  });
});

//This is to extract data from password configuration screenshot
$(document).ready(function() {
  $('#extractPWdata').click(function() {

      // Assuming you have some data to send
      id = $('#selected-app').val();
      var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
      var fileInput = $('input[name="file_name"]')[0].files[0];
      var formData = new FormData();
      formData.append('file_name', fileInput);
      formData.append('is_ajax_request', 'true');
      console.log('FormData:', formData); 
      // Make the POST request using jQuery
      $.ajax({
          type: 'POST',
          url: id,
          data: formData,
          headers: {
            'X-CSRFToken': csrf_token,
          },
          processData: false,
          contentType: false,
          success: function(data) {
              console.log('Data sent successfully');
          var lines = data.split('\n');  // Split the response by lines

          var max_history_pw = lines[0].split(': ')[1].trim();
          $('#pass_history').val(max_history_pw);
          var extract_min_pw_age = lines[1].split(': ')[1].trim();
          $('#pass_age').val(extract_min_pw_age);
          var extract_pw_length = lines[4].split(': ')[1].trim();
          $('#pass_length').val(extract_pw_length);
          },
          error: function(xhr, status, error) {
              console.error('Error sending data. Status code: ' + xhr.status);
          }
      });
  });
});

$("#risktable tbody").on("click", "a", function (event) {
  event.preventDefault();
  var id = $(this).data("process-id");
  $.ajax({
    url: "/riskform/" + id,
    type: "GET",
    datatype: "json",
    success: function (response) {
      var form = $("#risk_update");
      form.find("#id_default").val(id);
      form
        .find("#id_auditprojectname")
        .val(response.riskform_update.auditprojectname);
      form.find("#id_processname").val(response.riskform_update.processname);
      form.find("#id_riskid").val(response.riskform_update.riskid);
      form
        .find("#id_riskdescription")
        .val(response.riskform_update.riskdescription);
      form.find("#id_riskrating").val(response.riskform_update.riskrating);
      form
        .find("#id_riskratingrationale")
        .val(response.riskform_update.riskratingrationale);
      // Show modal
      $("#riskeditModal").modal("show");
    },
  });
});


//This is the code to open control in a new tab
$("#controldetailstable tbody").on("click", "a", function (event) {
  event.preventDefault();
  var controlid = $(this).closest("tr").find("td:first").text();

  // Check if tab with same tabName already exists
  var tabAlreadyExists = false;
  $(".nav-tabs li a").each(function () {
    if ($(this).text() === controlid) {
      tabAlreadyExists = true;
      $(this).tab("show"); // Activate existing tab
      return false; // Break out of loop
    } 
  });

  // If tab already exists, add a new tab
  if (tabAlreadyExists) {
    var tabs = JSON.parse(localStorage.getItem("tabs")) || {};
    var tabCounter = Object.keys(tabs).length + 1;
    var tabName = controlid;
    var tabId = "tab" + tabCounter;
    var selectedID = $(this).data("process-id");

    // Save the new tab to local storage
    tabs[tabId] = {
      name: tabName,
      field1: tabId,
      field2: selectedID,
      // Add additional fields as necessary
    };
    localStorage.setItem("tabs", JSON.stringify(tabs));

    // Activate the new tab
    $("#" + tabId).tab("show");

    // Save the selected tab and active process ID to local storage
    localStorage.setItem("selectedTabId", tabName);
    localStorage.setItem("control_id", selectedID);

    window.location.href = $(this).attr("href");
    return;
  }

  //Clone the hidden div
  var tabs = JSON.parse(localStorage.getItem("tabs")) || {};
  var tabCounter = Object.keys(tabs).length + 1; // Initialize the counter to the number of tabs in local storage plus 1
  var tabName = controlid; // Use the control ID to generate a unique tab name
  var tabId = "tab" + tabCounter; // Use the counter to generate a unique tab ID
  var selectedID = $(this).data("process-id");

  // Handle the click event of the close button
  $(".close-tab").click(function () {
    var tab = $(this).closest(".nav-item");
    var contentId = $(this).parent().attr("data-bs-target");
    var content = $(contentId);
    tab.remove();
    content.remove();
    // Remove the tab from local storage
    var tabs = JSON.parse(localStorage.getItem("tabs")) || {};
    delete tabs[contentId.substring(1)];
    localStorage.setItem("tabs", JSON.stringify(tabs));
    // Activate the home tab
  });

  // Save the tab to local storage
  var tabs = JSON.parse(localStorage.getItem("tabs")) || {};
  tabs[tabId] = {
    name: tabName,
    field1: tabId,
    field2: selectedID,
    // Add additional fields as necessary
  };
  localStorage.setItem("tabs", JSON.stringify(tabs));

  // Activate the new tab
  $("#" + tabId).tab("show");

  // Save the selected tab and active process ID to local storage
  localStorage.setItem("selectedTabId", tabName);
  localStorage.setItem("control_id", selectedID);

  window.location.href = $(this).attr("href");
});

