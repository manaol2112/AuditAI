$(document).ready(function() {

    $("#mapping_div").hide()
    $("#map_all_success").hide()
    $("#map_not_success").hide()
    // Function to handle file selection
    function handleFileSelect(files) {
        // Filter files to accept only Excel (xlsx) and CSV files
        let allowedTypes = ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/csv'];

        for (let i = 0; i < files.length; i++) {
            let file = files[i];
            if (allowedTypes.includes(file.type)) {
                // Update hidden input value
                $("#manual_user_upload").val("Your selected value");

                // Read the file
                let reader = new FileReader();
                reader.onload = function(event) {
                    // Parse CSV content
                    let csv = event.target.result;
                    let lines = csv.split('\n');
                    if (lines.length > 0) {
                        // Extract column headers (assuming they are in the first row)
                        let headers = lines[0].split(',');
                        // Clear existing options in the select element
                        $("#user_id_mapped").empty();
                        $("#email_mapped").empty();
                        $("#first_name_mapped").empty();
                        $("#last_name_mapped").empty();
                        $("#roles_mapped").empty();
                        $("#status_mapped").empty();
                        $("#date_granted_mapped").empty();
                        $("#date_revoked_mapped").empty();
                        $("#last_login_mapped").empty();

                        $("#user_id_mapped").append(`<option>Choose fields to map</option>`);
                        $("#email_mapped").append(`<option>Choose fields to map</option>`);
                        $("#first_name_mapped").append(`<option>Choose fields to map</option>`);
                        $("#last_name_mapped").append(`<option>Choose fields to map</option>`);
                        $("#roles_mapped").append(`<option>Choose fields to map</option>`);
                        $("#status_mapped").append(`<option>Choose fields to map</option>`);
                        $("#date_granted_mapped").append(`<option>Choose fields to map</option>`);
                        $("#date_revoked_mapped").append(`<option>Choose fields to map</option>`);
                        $("#last_login_mapped").append(`<option>Choose fields to map</option>`);

                        // Assuming headers is an array containing the options you want to populate

                        headers.forEach(header => {
                            if (header.toLowerCase().includes("id")) {
                                $("#user_id_mapped").append(`<option value="${header}" selected>${header}</option>`);
                            } else {
                                $("#user_id_mapped").append(`<option value="${header}">${header}</option>`);
                            }

                            if (header.toLowerCase().includes("mail")) {
                                $("#email_mapped").append(`<option value="${header}" selected>${header}</option>`);
                            } else {
                                $("#email_mapped").append(`<option value="${header}">${header}</option>`);
                            }

                            if (header.toLowerCase().match(/first[\s_]?name/)) {
                                $("#first_name_mapped").append(`<option value="${header}" selected>${header}</option>`);
                            } else {
                                $("#first_name_mapped").append(`<option value="${header}">${header}</option>`);
                            }

                            if (header.toLowerCase().match(/last[\s_]?name/)) {
                                $("#last_name_mapped").append(`<option value="${header}" selected>${header}</option>`);
                            } else {
                                $("#last_name_mapped").append(`<option value="${header}">${header}</option>`);
                            }

                            if (header.toLowerCase().includes("role")) {
                                $("#roles_mapped").append(`<option value="${header}" selected>${header}</option>`);
                            } else {
                                $("#roles_mapped").append(`<option value="${header}">${header}</option>`);
                            }

                            if (header.toLowerCase().includes("status")) {
                                $("#status_mapped").append(`<option value="${header}" selected>${header}</option>`);
                            } else {
                                $("#status_mapped").append(`<option value="${header}">${header}</option>`);
                            }

                            if (header.toLowerCase().includes("date_granted")) {
                                $("#date_granted_mapped").append(`<option value="${header}" selected>${header}</option>`);
                            } else {
                                $("#date_granted_mapped").append(`<option value="${header}">${header}</option>`);
                            }

                            if (header.toLowerCase().includes("date_revoked")) {
                                $("#date_revoked_mapped").append(`<option value="${header}" selected>${header}</option>`);
                            } else {
                                $("#date_revoked_mapped").append(`<option value="${header}">${header}</option>`);
                            }

                            if (header.toLowerCase().includes("last_login")) {
                                $("#last_login_mapped").append(`<option value="${header}" selected>${header}</option>`);
                            } else {
                                $("#last_login_mapped").append(`<option value="${header}">${header}</option>`);
                            }
                        });


                        var anySelected = false;

                        // Check each specific select element
                        $("#user_id_mapped, #email_mapped, #first_name_mapped, #last_name_mapped, #roles_mapped, #status_mapped, #date_granted_mapped, #date_revoked_mapped, #last_login_mapped").each(function() {
                            // Check if the selected value is 'Choose field'
                            if ($(this).val() === 'Choose fields to map') {
                                anySelected = true;
                                return false; // Exit the loop early if any select has 'Choose field' selected
                            }
                        });
                        
                        // Now anySelected variable will be true if any of the specific select fields have 'Choose field' selected
                        if (anySelected) {
                            $("#map_all_success").hide();
                            $("#map_not_success").show();
                        } else {
                            $("#map_all_success").show();
                            $("#map_not_success").hide();
                        }
                        
                        $("#mapping_div").show();

                    }
                };
                reader.readAsText(file);
            } else {
                // Handle unsupported file type here (optional)
                console.log('Unsupported file type: ' + file.type);
            }
        }
    }

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop area when file is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        document.body.addEventListener(eventName, highlight, false);
    });

    // Remove highlight when file is dragged away
    ['dragleave', 'drop'].forEach(eventName => {
        document.body.addEventListener(eventName, unhighlight, false);
    });

    // Handle dropped files
    document.body.addEventListener('drop', function(e) {
        handleFileSelect(e.dataTransfer.files);
        preventDefaults(e);
    }, false);

    // Handle file selection through input element
    $('#fileInput').change(function(e) {
        handleFileSelect(e.target.files);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight() {
        $(".file-drop-area").addClass('highlight');
    }

    function unhighlight() {
        $(".file-drop-area").removeClass('highlight');
    }
});
