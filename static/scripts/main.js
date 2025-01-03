document.addEventListener("DOMContentLoaded", function () {
    // Handle form submissions or interactions here if needed
    
    // Sample alert for resize action (can be expanded based on actual functionality)
    const resizeForm = document.querySelector('form[action="/resize"]');
    if (resizeForm) {
        resizeForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const width = document.getElementById('width').value;
            const height = document.getElementById('height').value;

            if (!width || !height) {
                alert("Please enter both width and height values.");
                return;
            }

            alert(`Image will be resized to ${width}x${height}px.`);
        });
    }
});
