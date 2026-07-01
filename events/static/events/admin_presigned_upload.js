document.addEventListener('DOMContentLoaded', function () {

    async function uploadFileToR2(file) {
        const params = new URLSearchParams({
            filename: file.name,
            content_type: file.type,
        });

        const response = await fetch(`/events/presigned-upload-url/?${params}`);
        const data = await response.json();

        await fetch(data.upload_url, {
            method: 'PUT',
            headers: { 'Content-Type': file.type },
            body: file,
        });

        return data.key;
    }

    function setupFileInput(fileInput) {
        const hiddenKeyInput = document.createElement('input');
        hiddenKeyInput.type = 'hidden';
        hiddenKeyInput.name = fileInput.name + '_r2_key';
        fileInput.parentNode.insertBefore(hiddenKeyInput, fileInput.nextSibling);

        fileInput.addEventListener('change', async function () {
            if (!fileInput.files || fileInput.files.length === 0) return;

            const file = fileInput.files[0];

            let statusEl = fileInput.parentNode.querySelector('.r2-upload-status');
            if (!statusEl) {
                statusEl = document.createElement('span');
                statusEl.className = 'r2-upload-status';
                fileInput.parentNode.insertBefore(statusEl, fileInput.nextSibling);
            }
            statusEl.textContent = ' Загрузка...';

            try {
                const key = await uploadFileToR2(file);
                hiddenKeyInput.value = key;
                statusEl.textContent = ' ✓ Загружено';
                fileInput.value = '';
            } catch (err) {
                statusEl.textContent = ' ✗ Ошибка загрузки';
                console.error(err);
            }
        });
    }

    function scanAndSetup() {
        document.querySelectorAll('input[type="file"][name$="-image"]').forEach(function (input) {
            if (!input.dataset.presignedSetup) {
                input.dataset.presignedSetup = 'true';
                setupFileInput(input);
            }
        });
    }

    scanAndSetup();

    document.body.addEventListener('click', function (e) {
        if (e.target.matches('.add-row a')) {
            setTimeout(scanAndSetup, 100);
        }
    });
});