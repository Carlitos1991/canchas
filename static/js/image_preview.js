document.addEventListener('DOMContentLoaded', function(){
    const input = document.getElementById('nuevaCanchaFotos');
    const preview = document.getElementById('previewContainer');
    const info = document.getElementById('previewInfo');

    if (!input) return;

    function clearPreview(){
        while(preview.firstChild) preview.removeChild(preview.firstChild);
        info.textContent = '';
    }

    input.addEventListener('change', function(e){
        clearPreview();
        const files = Array.from(input.files || []);
        if (files.length === 0) {
            info.textContent = 'No hay archivos seleccionados.';
            return;
        }
        info.textContent = files.length + ' archivo(s) seleccionado(s).';

        files.slice(0,6).forEach(file => {
            if (!file.type.startsWith('image/')) return;
            const reader = new FileReader();
            reader.onload = function(evt){
                const img = document.createElement('img');
                img.src = evt.target.result;
                img.classList.add('preview-thumb'); // Usamos clase CSS
                preview.appendChild(img);
            };
            reader.readAsDataURL(file);
        });

        if (files.length > 6) {
            const more = document.createElement('div');
            more.textContent = '+' + (files.length - 6) + ' más';
            more.classList.add('preview-more'); // Usamos clase CSS
            preview.appendChild(more);
        }
    });
});