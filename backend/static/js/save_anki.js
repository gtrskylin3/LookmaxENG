document.addEventListener('DOMContentLoaded', () => {
    const exportBtn = document.getElementById('exportBtn');
    
    if (exportBtn) {
        exportBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            
            // Проверяем: запущено ли приложение внутри окна pywebview?
            if (window.pywebview && window.pywebview.api) {
                exportBtn.disabled = true;
                exportBtn.innerText = 'Сохранение...';

                // Вызываем функцию Python, которую мы написали на Шаге 1
                //const result = await window.pywebview.api.export_anki_to_disk();
                let result;
                if (typeof window.pywebview.api.exportAnkiToDisk === 'function') {
                    result = await window.pywebview.api.exportAnkiToDisk();
                } else if (typeof window.pywebview.api.export_anki_to_disk === 'function') {
                    result = await window.pywebview.api.export_anki_to_disk();
                } else {
                    console.error("[JS] Метод экспорта не найден в объекте api!", window.pywebview.api);
                    alert("Ошибка: Метод экспорта не найден в приложении.");
                    return;     
                }
                exportBtn.disabled = false;
                exportBtn.innerText = 'Export dict to Anki (.apkg file)';

                if (result === "Success") {
                    alert("Файл успешно сохранен!");
                } else if (result !== "Cancelled") {
                    alert("Произошла ошибка: " + result);
                }
            } else {
                // Если открыли просто через обычный браузер — используем стандартный метод
                exportBtn.disabled = true;
                exportBtn.innerText = 'Downloading...';
                
                try {
                    const response = await fetch('/export-anki', { method: 'POST' });
                    if (!response.ok) throw new Error('Ошибка сети');
                    
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = "anki_cards.apkg";
                    document.body.appendChild(a);
                    a.click();
                    
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                } catch (err) {
                    alert('Не удалось скачать файл: ' + err.message);
                } finally {
                    exportBtn.disabled = false;
                    exportBtn.innerText = 'Export dict to Anki (.apkg file)';
                }
            }
        });
    }
});