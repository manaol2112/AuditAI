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

            // Create elements to display file name and Font Awesome icon
            var fileItem = $('<div>').addClass('selected-file-item');
            var iconElement = $('<i>').addClass(iconClass).css({'margin-right': '3px', 'font-size': '12px !important'});
            var fileNameElement = $('<span>').text(fileName).css({'margin-right': '3px', 'font-size': '12px !important'});

            fileItem.append(iconElement, fileNameElement);
            $('#selectedFilesContainer').append(fileItem);
        });
    });
});
