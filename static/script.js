document.addEventListener("DOMContentLoaded", function () {
    const contentField = document.getElementById("content");
    const charCount = document.getElementById("charCount");
    const noteForm = document.getElementById("noteForm");

    // Display the content character count
    if (contentField && charCount) {
        function updateCharCount() {
            const count = contentField.value.length;
            charCount.textContent = count + " characters";
        }

        contentField.addEventListener("input", updateCharCount);
        updateCharCount();
    }

    // Validate the new note form
    if (noteForm) {
        noteForm.addEventListener("submit", function (event) {
            const title = document.getElementById("title").value.trim();
            const content = contentField.value.trim();

            if (!title || !content) {
                event.preventDefault();
                alert("Please enter both a title and note content.");
            }
        });
    }

    // Ask for confirmation before deleting a note
    document.querySelectorAll(".delete-form").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const confirmed = confirm(
                "Are you sure you want to delete this note?"
            );

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
});

