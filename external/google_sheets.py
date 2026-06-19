
from .auth.auth import get_google_sheets_client

def update_google_sheet(data):
    try: 
        sheet_id = "1C-z7bDquJuNgL6CdVZgrUm7Hw-Z5C0H6PBr_YOrrKBQ"
        client = get_google_sheets_client()

        workbook = client.open_by_key(sheet_id)
        
        # Acessa a primeira aba da planilha
        sheet = workbook.get_worksheet(0)

        #Exemplo data = ["16/06/2026", "João Silva", "R$ 150,00", "Pago"]
        sheet.append_row(data) 

    except Exception as e:
        print(f"Erro ao atualizar a planilha no Google Sheets: {e}")

