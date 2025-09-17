from fuzzywuzzy import fuzz
from src.models.lijek import Lijek
import pandas as pd
from src.models.lijek import Lijek

from src.models.djelatna_tvar import DjelatnaTvar

class LijekService:
    @staticmethod
    async def import_lijekovi_from_excel(file_path: str, db):
        try:
            df = pd.read_excel(file_path, skiprows=9)
            required_columns = {"Naziv", "Status nestašice"}
            if not required_columns.issubset(df.columns):
                raise ValueError(f"Excel file must contain the following columns: {required_columns}")
            column_map = {
                "Naziv": "naziv",         
                "Status nestašice": "nestasica" 
            }
            print(df)
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
                mapped["accepted"] = True 
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

    @staticmethod
    async def get_requested_meds(db):
        response = []
        lijekovi = db.query(Lijek).filter_by(accepted=False).all()
        if not lijekovi:
            return None
        for lijek in lijekovi:
            djelatna_tvar = db.query(DjelatnaTvar).filter_by(id=lijek.idDjelatnaTvar).first()
            response.append({
                "id": lijek.id,
                "naziv": lijek.naziv,
                "nestasica": lijek.nestasica,
                "DjelatnaTvar": djelatna_tvar.naziv if djelatna_tvar else None
            })
        return response

    @staticmethod
    async def create_med(med_dict, db):
        med_dict = dict(med_dict)

       
        closest_lijek = LijekService.get_closest_med(db, med_dict["naziv"], 0.9)
        if closest_lijek:
            return None
        closest_tvar = LijekService.get_closest_tvar(db, med_dict.get("DjelatnaTvar", ""), 0.9)
        if closest_tvar:
            med_dict["idDjelatnaTvar"] = closest_tvar.id
        else:
            tvar = db.query(DjelatnaTvar).filter_by(naziv=med_dict.get("DjelatnaTvar", "")).first()
            if tvar:
                med_dict["idDjelatnaTvar"] = tvar.id
        med_dict.pop("DjelatnaTvar", None)
        lijek = Lijek(**med_dict)
        db.add(lijek)
        db.commit()
        db.refresh(lijek)
        return lijek

    @staticmethod
    async def approve_med(id, db):
        lijek = db.query(Lijek).filter_by(id=id).first()
        if not lijek:
            return None
        lijek.accepted = True
        db.commit()
        db.refresh(lijek)
        return lijek

    
    @staticmethod
    async def delete_med(id, db):
        lijek = db.query(Lijek).filter_by(id=id).first()
        if not lijek:
            return None
        db.delete(lijek)
        db.commit()
        return lijek

    @staticmethod
    async def get_med(id, db):
        return db.query(Lijek).filter_by(id=id).first()

    @staticmethod
    async def get_all_meds(db, current_user=None):
        return db.query(Lijek).all()
    
    @staticmethod
    def get_closest_med(db, query, min_ratio=0.0):
        ilike_candidates = db.query(Lijek).filter(Lijek.naziv.ilike(f"%{query}%")).all()
        best_med = None
        best_score = -1.0
        for med in ilike_candidates:
            score = fuzz.ratio(query, med.naziv) / 100.0
            if score >= min_ratio and score > best_score:
                best_score = score
                best_med = med

        return best_med
    @staticmethod
    def get_closest_tvar(db, query, min_ratio=0.0):
        ilike_candidates = db.query(DjelatnaTvar).filter(DjelatnaTvar.naziv.ilike(f"%{query}%")).all()
        best_tvar = None
        best_score = -1.0
        for tvar in ilike_candidates:
            score = fuzz.ratio(query, tvar.naziv) / 100.0
            if score >= min_ratio and score > best_score:
                best_score = score
                best_tvar = tvar

        return best_tvar
