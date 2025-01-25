// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('myForm');
    const message = document.getElementById('message');

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();
            message.textContent = `Name: ${result.name}, Email: ${result.email}`;
        } catch (error) {
            message.textContent = 'Error submitting form';
        }
    });
});
