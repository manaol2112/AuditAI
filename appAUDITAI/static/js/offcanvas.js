// Update the ID of the file input and file drop area
const app_user_fileDropArea = document.querySelector("#app_user_upload_form .file-drop-area");

// Add event listeners for drag and drop
app_user_fileDropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  app_user_fileDropArea.classList.add("dragover");
});

app_user_fileDropArea.addEventListener("dragleave", () => {
  app_user_fileDropArea.classList.remove("dragover");
});

app_user_fileDropArea.addEventListener("drop", (e) => {
  e.preventDefault();

  app_user_fileDropArea.classList.remove("dragover");

  const files = e.dataTransfer.files;

  if (files.length > 0) {
    const app_user_fileInput = document.querySelector('#app_user_upload_form input[type="file"]');
    
    // Clear existing files
    app_user_fileInput.files = null;

    // Add the dropped file
    app_user_fileInput.files = files;

    // Trigger the change event on the file input
    triggerFileInputChange(app_user_fileInput);
  }
});

// Add event listener for manual file selection
const app_user_fileInput = document.querySelector('#app_user_upload_form input[type="file"]');
app_user_fileInput.addEventListener("change", (e) => {
  const selectedFile = e.target.files[0];

  // You can handle the selected file as needed
});

function triggerFileInputChange(input) {
  const event = new Event("change", { bubbles: true });
  input.dispatchEvent(event);
}

app_user_fileInput.addEventListener("change", (e) => {
    const selectedFile = e.target.files[0];
  
    // Check if a file is selected
    if (selectedFile) {
      // Get the file extension
      const fileExtension = selectedFile.name.split('.').pop().toLowerCase();
  
      // Check if the file extension is allowed (CSV or TXT)
      if (fileExtension === 'csv' || fileExtension === 'txt') {
        // You can handle the selected file as needed
        console.log('File is allowed:', selectedFile);
      } else {
        // Display an error message or take appropriate action for invalid file type
        alert('Invalid file type. Please upload a CSV or TXT file.');
        // Clear the file input to prevent submitting invalid files
        app_user_fileInput.value = '';
      }
    }
  });


  // Update the ID of the file input and file drop area
const new_user_fileDropArea = document.querySelector("#new_user_approval_upload_form .file-drop-area");

// Add event listeners for drag and drop
new_user_fileDropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  new_user_fileDropArea.classList.add("dragover");
});

new_user_fileDropArea.addEventListener("dragleave", () => {
  new_user_fileDropArea.classList.remove("dragover");
});

new_user_fileDropArea.addEventListener("drop", (e) => {
  e.preventDefault();

  new_user_fileDropArea.classList.remove("dragover");

  const files = e.dataTransfer.files;

  if (files.length > 0) {
    const new_user_fileInput = document.querySelector('#app_user_upload_form input[type="file"]');
    
    // Clear existing files
    new_user_fileInput.files = null;

    // Add the dropped file
    new_user_fileInput.files = files;

    // Trigger the change event on the file input
    triggerFileInputChange(new_user_fileInput);
  }
});

// Add event listener for manual file selection
const new_user_fileInput = document.querySelector('#app_user_upload_form input[type="file"]');
new_user_fileInput.addEventListener("change", (e) => {
  const selectedFile = e.target.files[0];

  // You can handle the selected file as needed
});

function triggerFileInputChange(input) {
  const event = new Event("change", { bubbles: true });
  input.dispatchEvent(event);
}

new_user_fileInput.addEventListener("change", (e) => {
    const selectedFile = e.target.files[0];
  
    // Check if a file is selected
    if (selectedFile) {
      // Get the file extension
      const fileExtension = selectedFile.name.split('.').pop().toLowerCase();
  
      // Check if the file extension is allowed (CSV or TXT)
      if (fileExtension === 'csv' || fileExtension === 'txt') {
        // You can handle the selected file as needed
        console.log('File is allowed:', selectedFile);
      } else {
        // Display an error message or take appropriate action for invalid file type
        alert('Invalid file type. Please upload a CSV or TXT file.');
        // Clear the file input to prevent submitting invalid files
        new_user_fileInput.value = '';
      }
    }
  });
