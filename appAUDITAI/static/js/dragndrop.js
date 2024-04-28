//THIS IS THE CODE TO DRAG AND DROP ATTACHMENT TO UPLOAD SECTION
const fileDropArea = document.querySelector(".file-drop-area");
const imagePreviewContainer = document.getElementById("image-preview-container");
const imagePreview = document.getElementById("image-preview");
const modal_imagePreviewContainer = document.getElementById("image-preview-container");
const modal_imagePreview = document.getElementById("image-preview2");

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

    // Display the image preview
    displayImagePreview(files[0]);
  }
});

// Add event listener for manual file selection
const fileInput = document.querySelector('input[type="file"]');
fileInput.addEventListener("change", (e) => {
  const selectedFile = e.target.files[0];

  if (selectedFile) {
    $('#image-preview-container').show()
    displayImagePreview(selectedFile);
  }
});

function triggerFileInputChange(input) {
  const event = new Event("change", { bubbles: true });
  input.dispatchEvent(event);
}

function displayImagePreview(file) {
  const reader = new FileReader();

  reader.onload = function (e) {
    imagePreview.src = e.target.result;
    modal_imagePreview.src = e.target.result;
  };

  reader.readAsDataURL(file);
  // You can also update other styles or properties here if needed
  $('#image-preview').show();
  imagePreviewContainer.classList.add("visible");
  modal_imagePreviewContainer.classList.add("visible");
}


 


