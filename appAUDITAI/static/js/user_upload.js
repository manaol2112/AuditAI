$(document).ready(function() {
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
    document.body.addEventListener('drop', handleDrop, false);

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

    function handleDrop(e) {
        let dt = e.dataTransfer;
        let files = dt.files;

        // Filter files to accept only Excel (xlsx) and CSV files
        let allowedTypes = ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/csv'];

        for (let i = 0; i < files.length; i++) {
            let file = files[i];
            if (allowedTypes.includes(file.type)) {
                // Add dropped file to file input
                $("#fileInput")[0].files = files;

                // Update hidden input value
                $("#manual_user_upload").val("Your selected value");

                // Add any other handling code here if needed
            } else {
                // Handle unsupported file type here (optional)
                console.log('Unsupported file type: ' + file.type);
            }
        }

        // Prevent default drop behavior (open as link for some elements)
        preventDefaults(e);
    }
});