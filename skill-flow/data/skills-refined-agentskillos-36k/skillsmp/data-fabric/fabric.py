import pandas as pd
import os

def process_miner_output(input_csv, output_csv, default_margin=1.30):
    """
    Convierte la salida del Minero (CDR) en la entrada del Tasador (ML).
    Aplica un margen por defecto al precio de costo.
    """
    print(f"Fabricando datos: {input_csv} -> {output_csv}")
    
    if not os.path.exists(input_csv):
        print(f"[ERROR] No existe {input_csv}")
        return False
        
    try:
        df = pd.read_csv(input_csv)
        
        # Mapping columns
        # CDR_MASTER_DB.csv: Categoria, Nombre, Precio_CDR_USD, Stock, URL
        # productos_listos_para_web.csv expected by appraiser: Nombre, Precio_Venta
        
        if 'Precio_CDR_USD' not in df.columns or 'Nombre' not in df.columns:
            print("[ERROR] Columnas faltantes en CSV de entrada")
            return False
            
        # Filter items with price > 0
        df = df[df['Precio_CDR_USD'] > 0].copy()
        
        # Calculate sale price
        df['Precio_Venta'] = df['Precio_CDR_USD'] * default_margin
        
        # Round to whole numbers
        df['Precio_Venta'] = df['Precio_Venta'].round(0).astype(int)
        
        # Select columns for appraiser
        # We might want to keep URL or Categoria for reference, appraiser accepts extra columns
        df_out = df[['Nombre', 'Precio_Venta', 'Categoria', 'Precio_CDR_USD']].copy()
        
        df_out.to_csv(output_csv, index=False, encoding='utf-8')
        print(f"[OK] Generados {len(df_out)} registros para tasacion")
        return True
        
    except Exception as e:
        print(f"[ERROR] Fallo en fabrica: {e}")
        return False

if __name__ == "__main__":
    pass
