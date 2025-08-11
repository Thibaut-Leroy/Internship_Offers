from openpyxl import load_workbook

def excel_settings(filename):
    wb = load_workbook(filename)
    ws = wb.active

    for column_cells in ws.columns:
        max_length = 0
        column = column_cells[0].column_letter
        for cell in column_cells:
            try:
                if len(str(cell.value))>max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        ws.column_dimensions[column].width = max_length + 2
    
    wb.save(filename)
    print("Excel formatting done")

if __name__ == "__main__":
    excel_settings()

