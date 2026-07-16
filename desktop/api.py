import os 
import webview
import requests

class Api:
    def export_anki_to_disk(self):
        active_win = webview.active_window()
        if not active_win:
            return "Ошибка: Окно приложения не найдено"
        
        save_path = active_win.create_file_dialog(
            webview.FileDialog.SAVE,
            directory='',
            save_filename='anki_cards.apkg'
        )

        if not save_path:
            return "Cancelled"
        try:
            response = requests.post("http://127.0.0.1:8000/export-anki")
            if response.status_code == 200:
                with open(save_path[0], 'wb') as f:
                    f.write(response.content)
                return "Success"
            else:
                return f"Server Error {response.status_code}"
        except Exception as e:
            return f"Save Error: {str(e)}"
        

api = Api()