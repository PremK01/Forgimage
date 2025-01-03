// main.ts

// Function to handle form submission with image resizing
document.addEventListener("DOMContentLoaded", () => {
    const formResize = document.querySelector('form[action="/resize-image"]') as HTMLFormElement;
    formResize?.addEventListener('submit', (e) => {
        e.preventDefault();

        // Perform frontend validation and possible image preview before submitting
        const fileInput = document.querySelector('input[name="file"]') as HTMLInputElement;
        const widthInput = document.querySelector('input[name="width"]') as HTMLInputElement;
        const heightInput = document.querySelector('input[name="height"]') as HTMLInputElement;

        if (fileInput.files && fileInput.files.length > 0 && widthInput.value && heightInput.value) {
            alert('Form ready to submit');
            formResize.submit();
        } else {
            alert('Please fill all fields');
        }
    });
});
