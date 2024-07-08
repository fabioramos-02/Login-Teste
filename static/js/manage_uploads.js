document.addEventListener('DOMContentLoaded', function() {
    async function deleteFile(filename) {
        const responseElement = document.getElementById('response');
        try {
            const response = await fetch(`/delete-file/${filename}`, {
                method: 'DELETE',
            });
            const result = await response.json();
            responseElement.textContent = result.message;
            responseElement.style.color = 'green';
            document.getElementById('fileList').innerHTML = '';
            location.reload();
        } catch (error) {
            responseElement.textContent = 'Erro ao deletar o arquivo: ' + error.message;
            responseElement.style.color = 'red';
        }
    }

    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function() {
            const filename = this.getAttribute('data-filename');
            deleteFile(filename);
        });
    });

    document.getElementById('backToUploadButton').addEventListener('click', () => {
        window.location.href = '/';
    });
});
