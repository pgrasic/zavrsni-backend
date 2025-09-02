from src.models.lijek import Lijek
from src.models.user import Korisnik
import pandas as pd
from src.models.lijek import Lijek

from src.models.djelatna_tvar import DjelatnaTvar

class LijekService:
    @staticmethod
    async def import_lijekovi_from_excel(file_path: str, db):
        try:
            df = pd.read_excel(file_path)
            required_columns = {"Naziv", "Status nestašice"}
            if not required_columns.issubset(df.columns):
                raise ValueError(f"Excel file must contain the following columns: {required_columns}")
            column_map = {
                "Naziv": "naziv",         
                "Status nestašice": "nestasica" 
            }
            imported = []
            for record in df.dropna().to_dict(orient="records"):
                mapped = {}
                for excel_field, model_field in column_map.items():
                    value = record[excel_field]
                    if model_field == "nestasica":
                        mapped[model_field] = True if value == "u tijeku" else False
                    else:
                        mapped[model_field] = value
                djelatna_tvar_row = db.query(DjelatnaTvar.id).filter_by(naziv=record.get("Djelatna tvar")).first()
                if djelatna_tvar_row:
                    mapped["idDjelatnaTvar"] = djelatna_tvar_row.id
                existing = db.query(Lijek).filter_by(naziv=mapped["naziv"]).first()
                if not existing:
                    lijek = Lijek(**mapped)
                    print("IMPORTING LIJEK: " + str(lijek.idDjelatnaTvar))
                    db.add(lijek)
                    db.commit()
                    db.refresh(lijek)
                    imported.append(lijek)
            return imported
        
        except Exception as e:
            raise ValueError(f"Error processing Excel file: {e}")

    @staticmethod
    async def import_djelatne_tvari_from_excel(file_path: str, db):
        try:
            df = pd.read_excel(file_path)
            if "Djelatna tvar" not in df.columns:
                raise ValueError("Excel file must contain the column: 'Djelatna tvar'")
            djelatne_tvari = set()
            for cell in df["Djelatna tvar"].dropna():
                for naziv in str(cell).split(";"):
                    naziv_clean = naziv.strip()
                    if naziv_clean:
                        djelatne_tvari.add(naziv_clean)

            imported = []
            for naziv in djelatne_tvari:
                print("------------------------------")
                print(naziv)
                if not isinstance(naziv, str) or not naziv.strip():
                    print("Invalid Djelatna tvar name:", naziv)
                    continue
                if isinstance(naziv, str) or not naziv.strip():
                    
                    existing = db.query(DjelatnaTvar).filter_by(naziv=naziv).first()
                    if not existing:
                        dt = DjelatnaTvar(naziv=naziv)
                        db.add(dt)
                        db.commit()
                        db.refresh(dt)
                        imported.append(dt)
            return imported
        except Exception as e:
            raise ValueError(f"Error processing Excel file: {e}")
            