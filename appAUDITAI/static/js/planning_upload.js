document.addEventListener("DOMContentLoaded", function() {
    const fileDropArea = document.querySelector(".planning_file-drop-area");
    const fileInput = document.getElementById('planning_fileInput');

    // Add event listeners for drag and drop
    fileDropArea.addEventListener("dragover", (e) => {
        e.preventDefault();
        fileDropArea.classList.add("dragover");
    });

    fileDropArea.addEventListener("dragleave", () => {
        fileDropArea.classList.remove("dragover");
    });

    fileDropArea.addEventListener("drop", (e) => {
        e.preventDefault();
        fileDropArea.classList.remove("dragover");

        const files = e.dataTransfer.files;

        if (files.length > 0) {
            fileInput.files = files;
            triggerFileInputChange(fileInput);
        }
    });

    function triggerFileInputChange(input) {
        const event = new Event("change", { bubbles: true });
        input.dispatchEvent(event);
    }

    window.planning_triggerFileInputClick = function() {
        fileInput.click();
    }

    // Handle file input change event
    fileInput.addEventListener('change', function () {
        handleFiles(this.files);
    });

});
