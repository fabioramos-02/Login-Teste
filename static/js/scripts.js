document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    const responseElement = document.getElementById('response');
    const cancelButton = document.getElementById('cancelButton');

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        fileInput.files = e.dataTransfer.files;
    });

    uploadForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const files = fileInput.files;
        const formData = new FormData();
        for (const file of files) {
            formData.append('file', file);
        }

        try {
            const response = await fetch('/upload/', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            responseElement.textContent = result.info;
        } catch (error) {
            responseElement.textContent = 'Erro ao enviar o arquivo: ' + error.message;
        }
    });

    cancelButton.addEventListener('click', (e) => {
        e.preventDefault();
        fileInput.value = '';
        responseElement.textContent = '';
    });
});
