
//THIS IS THE CODE TO DRAG AND DROP ATTACHMENT TO UPLOAD SECTION
const fileDropArea = document.querySelector(".file-drop-area");

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
    const fileInput = document.querySelector('input[type="file"]');
    fileInput.files = files;
    triggerFileInputChange(fileInput);
  }
});

function triggerFileInputChange(input) {
  const event = new Event("change", { bubbles: true });
  input.dispatchEvent(event);
}

function triggerFileInputClick() {
    document.getElementById('fileInput').click();
}

$(document).ready(function() {

    $('#fileInput').on('change', function(event) {
        var files = event.target.files;
        $('#selectedFilesContainer').empty(); // Clear previous content

        $.each(files, function(index, file) {
            var fileName = file.name;
            var fileType = fileName.split('.').pop(); // Get file extension

            // Map file extensions to Font Awesome icons
            var iconClass;
            switch(fileType.toLowerCase()) {
                case 'pdf':
                    iconClass = 'far fa-file-pdf';
                    break;
                case 'doc':
                case 'docx':
                    iconClass = 'far fa-file-word';
                    break;
                case 'xls':
                case 'xlsx':
                    iconClass = 'far fa-file-excel';
                    break;
                case 'ppt':
                case 'pptx':
                    iconClass = 'far fa-file-powerpoint';
                    break;
                case 'jpg':
                case 'jpeg':
                case 'png':
                case 'gif':
                    iconClass = 'far fa-file-image';
                    break;
                case 'zip':
                case 'rar':
                case 'txt':
                    iconClass = 'far fa-file-archive';
                    break;
                default:
                    iconClass = 'far fa-file';
                    break;
            }

            // Create elements to display file name, Font Awesome icon, and delete icon
            var fileItem = $('<div>').addClass('selected-file-item');
            var iconElement = $('<i>').addClass(iconClass).css({'margin-right': '3px', 'font-size': '13px !important'});
            var fileNameElement = $('<span>').text(fileName).css({'margin-right': '3px', 'font-size': '13px !important'});
            var deleteIcon = $('<i>').addClass('far fa-trash-alt delete-icon').css({'cursor': 'pointer', 'color': 'orange', 'font-size': '13px !important', });
            var downloadIcon = $('<i>').addClass('fas fa-download download-icon').css({'cursor': 'pointer', 'color': 'lightblue', 'font-size': '13px !important','margin-right': '5px'});

            // Add click event to delete icon to remove the file item
            deleteIcon.on('click', function(event) {
                event.stopPropagation(); // Prevent click event propagation to the parent file item
                fileItem.remove();
            });

            // Add click event to download icon to trigger download
            downloadIcon.on('click', function(event) {
                event.stopPropagation(); // Prevent click event propagation to the parent file item
                var downloadLink = URL.createObjectURL(file);
                var a = document.createElement('a');
                a.href = downloadLink;
                a.download = fileName;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            });

            fileItem.append(iconElement, fileNameElement,downloadIcon, deleteIcon );
            $('#selectedFilesContainer').append(fileItem);
        });
    });
});
