import random
from datetime import date, timedelta
from faker import Faker
from models import (db, Utilizator, Categorie, Producator, Furnizor, Produs, 
                    VariantaComercialaProdus, ReferatNecesitate, ProdusInReferat, Lot, ProdusInLot,
                    StareReferat, ProceduraAchizitie, TipProcedura, LotProcedura, Oferta, ArticolOferta,
                    Contract, TipContract, ArticolContractat, ComandaGeneral, DetaliiComandaProdus,
                    LivrareComanda, DocumentLivrare, TipDocument)

fake = Faker('ro_RO') # Folosim date specifice României unde e posibil

def seed_data():
    """Populează baza de date cu date de test."""
    
    # Verificăm dacă există deja date pentru a evita duplicarea
    if Categorie.query.first():
        print("Baza de date pare să fie deja populată. Se omite procesul de seeding.")
        return

    print("Începe popularea bazei de date cu date demo...")

    # 1. Utilizatori (pe lângă admin)
    utilizatori = []
    for i in range(3):
        user = Utilizator(
            Nume_Utilizator=fake.user_name(),
            Email=fake.email()
        )
        user.set_password('password123')
        utilizatori.append(user)
    db.session.add_all(utilizatori)
    db.session.commit()
    print(f"-> Creat {len(utilizatori)} utilizatori demo.")

    # 2. Entități independente: Categorii, Producători, Furnizori
    nume_categorii = ["Reactivi", "Sticlarie laborator", "Consumabile generale", "Echipamente mici", "Medii de cultura"]
    categorii = [Categorie(Nume_Categorie=nume) for nume in nume_categorii]
    db.session.add_all(categorii)

    producatori = [Producator(Nume_Producator=fake.company()) for _ in range(10)]
    db.session.add_all(producatori)

    furnizori = [Furnizor(Nume_Furnizor=fake.company(), CUI=fake.unique.ean(length=8)) for _ in range(8)]
    db.session.add_all(furnizori)
    db.session.commit()
    print(f"-> Creat {len(categorii)} categorii, {len(producatori)} producători, {len(furnizori)} furnizori.")

    # 3. Produse Generice (dependente de Categorii)
    produse = []
    for _ in range(50):
        produs = Produs(
            Nume_Generic=f"{fake.word().capitalize()} {fake.word()}",
            Specificatii_Tehnice=fake.text(max_nb_chars=150),
            Unitate_Masura=random.choice(['Buc', 'Cutie', 'Kit', 'Flacon']),
            ID_Categorie=random.choice(categorii).ID_Categorie
        )
        produse.append(produs)
    db.session.add_all(produse)
    db.session.commit()
    print(f"-> Creat {len(produse)} produse generice.")

    # 4. Variante Comerciale (dependente de Produse și Producători)
    variante = []
    for produs in produse:
        for _ in range(random.randint(1, 3)):
            varianta = VariantaComercialaProdus(
                ID_Produs_Generic=produs.ID_Produs,
                ID_Producator=random.choice(producatori).ID_Producator,
                Cod_Catalog=fake.unique.ean(length=13),
                Descriere_Ambalare=f"{random.choice(['Pachet', 'Cutie', 'Set'])} x {random.randint(1,100)} buc",
                Cantitate_Standard_Ambalare=1
            )
            variante.append(varianta)
    db.session.add_all(variante)
    db.session.commit()
    print(f"-> Creat {len(variante)} variante comerciale.")

    # 5. Referate de Necesitate și produsele lor
    referate_aprobate = []
    produse_aprobate_in_referate = []

    for i in range(10):
        stare_aleasa = random.choice(list(StareReferat))
        referat = ReferatNecesitate(
            Numar_Referat=f"REF-{i+1}-{date.today().year}",
            Data_Creare=date.today() - timedelta(days=random.randint(5, 100)),
            Stare=stare_aleasa,
            ID_Utilizator_Creare=random.choice(utilizatori).ID_Utilizator,
            Observatii=fake.sentence()
        )
        db.session.add(referat)
        db.session.flush() # Pentru a obține ID-ul referatului

        # Adăugăm 3-8 produse în referat
        produse_in_referat = []
        produse_selectate_pt_referat = random.sample(produse, random.randint(3, 8))
        for produs_generic in produse_selectate_pt_referat:
            pir = ProdusInReferat(
                ID_Referat=referat.ID_Referat,
                ID_Produs_Generic=produs_generic.ID_Produs,
                Cantitate_Solicitata=random.randint(1, 20)
            )
            produse_in_referat.append(pir)
        db.session.add_all(produse_in_referat)
        db.session.flush() # Pentru a obține ID-urile

        # Pentru referatele aprobate, le stocăm pentru a le folosi în proceduri
        if stare_aleasa == StareReferat.APROBAT:
            referate_aprobate.append(referat)
            produse_aprobate_in_referate.extend(produse_in_referat)
        
        # Pentru a testa pagina de detalii referat, creăm și alocăm produse în vechile Loturi
        if stare_aleasa != StareReferat.CIORNA:
            for j in range(random.randint(1, 2)):
                lot = Lot(
                    ID_Referat=referat.ID_Referat,
                    Nume_Lot=f"Lot {j+1} - {referat.Numar_Referat}",
                    Descriere_Lot=fake.bs()
                )
                db.session.add(lot)
                db.session.flush()
                # Alocăm o parte din produse în acest lot
                produse_de_alocat = random.sample(produse_in_referat, k=random.randint(1, len(produse_in_referat) // 2))
                for pir_de_alocat in produse_de_alocat:
                    # Verificăm dacă nu e deja alocat
                    if not ProdusInLot.query.filter_by(ID_Produs_Referat=pir_de_alocat.ID_Produs_Referat).first():
                        pil = ProdusInLot(ID_Lot=lot.ID_Lot, ID_Produs_Referat=pir_de_alocat.ID_Produs_Referat)
                        db.session.add(pil)

    db.session.commit()
    print(f"-> Creat 10 referate de necesitate, din care {len(referate_aprobate)} sunt aprobate.")

    # 6. Proceduri de Achiziție și Super-Loturi (LotProcedura)
    proceduri = []
    for i in range(3):
        procedura = ProceduraAchizitie(
            Nume_Procedura=f"PA-{i+1} - {fake.catch_phrase()}",
            Tip_Procedura=random.choice(list(TipProcedura)),
            ID_Utilizator_Creare=random.choice(utilizatori).ID_Utilizator
        )
        db.session.add(procedura)
        db.session.flush()

        # Creăm 1-2 Super-Loturi și le populăm cu produse din referatele aprobate
        for j in range(random.randint(1, 2)):
            if not produse_aprobate_in_referate: break # Nu mai avem produse de alocat
            
            super_lot = LotProcedura(
                ID_Procedura=procedura.ID_Procedura,
                Nume_Lot=f"Super-Lot {j+1}",
                Descriere_Lot=fake.bs()
            )
            # Alocăm un set de produse disponibile
            produse_de_alocat_in_super_lot = random.sample(produse_aprobate_in_referate, k=min(len(produse_aprobate_in_referate), random.randint(2, 4)))
            super_lot.articole_incluse.extend(produse_de_alocat_in_super_lot)
            # Scoatem produsele alocate din lista de disponibile
            produse_aprobate_in_referate = [p for p in produse_aprobate_in_referate if p not in produse_de_alocat_in_super_lot]
            db.session.add(super_lot)
        proceduri.append(procedura)
    db.session.commit()
    print(f"-> Creat {len(proceduri)} proceduri cu Super-Loturi.")

    # 7. Oferte și Articole de Ofertă
    oferte_castigatoare = {} # {lot_procedura_id: oferta_obj}
    for procedura in proceduri:
        for lot_proc in procedura.loturi_procedura:
            oferta_minima = None
            pret_minim = float('inf')
            # Generăm 2-3 oferte per lot
            for furnizor in random.sample(furnizori, k=random.randint(2, 3)):
                oferta = Oferta(
                    ID_Furnizor=furnizor.ID_Furnizor,
                    ID_Procedura=procedura.ID_Procedura,
                    Numar_Inregistrare=f"OFERTA-{fake.ean(length=8)}"
                )
                db.session.add(oferta)
                db.session.flush()
                
                valoare_totala_oferta_pe_lot = 0
                # Adăugăm articole în ofertă
                for articol_solicitat in lot_proc.articole_incluse:
                    varianta_aleasa = random.choice(articol_solicitat.produs_generic_req.variante_comerciale)
                    pret = round(random.uniform(10.0, 500.0), 2)
                    articol_oferta = ArticolOferta(
                        ID_Oferta=oferta.ID_Oferta,
                        ID_Varianta_Comerciala=varianta_aleasa.ID_Varianta_Comerciala,
                        ID_Produs_Referat=articol_solicitat.ID_Produs_Referat,
                        Pret_Unitar_Pachet=pret
                    )
                    db.session.add(articol_oferta)
                    valoare_totala_oferta_pe_lot += pret * articol_solicitat.Cantitate_Solicitata
                
                if valoare_totala_oferta_pe_lot < pret_minim:
                    pret_minim = valoare_totala_oferta_pe_lot
                    oferta_minima = oferta
            
            if oferta_minima:
                oferte_castigatoare[lot_proc.ID_Lot_Procedura] = oferta_minima
    db.session.commit()
    print(f"-> Creat oferte pentru proceduri și selectat {len(oferte_castigatoare)} oferte câștigătoare.")

    # 8. Contracte și Comenzi
    for lot_proc_id, oferta_castigatoare in oferte_castigatoare.items():
        lot_proc = LotProcedura.query.get(lot_proc_id)
        tip_contract = random.choice(list(TipContract))
        
        # Calculăm valoarea contractului
        valoare_contract = 0
        articole_oferta_castigatoare = ArticolOferta.query.filter_by(ID_Oferta=oferta_castigatoare.ID_Oferta).all()
        articole_oferta_map = {ao.ID_Produs_Referat: ao for ao in articole_oferta_castigatoare}

        articole_contractate = []
        for articol_solicitat in lot_proc.articole_incluse:
            art_oferta = articole_oferta_map.get(articol_solicitat.ID_Produs_Referat)
            if art_oferta:
                valoare_contract += art_oferta.Pret_Unitar_Pachet * articol_solicitat.Cantitate_Solicitata
                articole_contractate.append((art_oferta, articol_solicitat.Cantitate_Solicitata))

        contract = Contract(
            Tip_Contract=tip_contract,
            ID_Procedura=oferta_castigatoare.ID_Procedura,
            ID_Furnizor=oferta_castigatoare.ID_Furnizor,
            Pret_Total_Contract=valoare_contract,
            Numar_Contract=f"CONTRACT-{fake.ean(length=8)}",
            ID_Utilizator_Creare=random.choice(utilizatori).ID_Utilizator
        )
        contract.loturi_procedura_contractate.append(lot_proc)
        
        # Adăugăm articolele în contract
        for art_oferta, cantitate in articole_contractate:
            ac = ArticolContractat(
                ID_Produs_Referat=art_oferta.ID_Produs_Referat,
                ID_Varianta_Comerciala=art_oferta.ID_Varianta_Comerciala,
                Cantitate_Contractata_Pachete=cantitate,
                Pret_Unitar_Pachet_Contract=art_oferta.Pret_Unitar_Pachet
            )
            contract.articole_contractate.append(ac)
        
        db.session.add(contract)
        db.session.flush()

        # Creăm comenzi
        if tip_contract == TipContract.CONTRACT_FERM:
            comanda = ComandaGeneral(ID_Contract=contract.ID_Contract, Numar_Comanda=f"CMD-AUT-{contract.Numar_Contract}", Stare_Comanda="Generata Automat", ID_Utilizator_Creare=random.choice(utilizatori).ID_Utilizator)
            for ac in contract.articole_contractate:
                comanda.detalii_produse_comanda_rel.append(DetaliiComandaProdus(ID_Articol_Contractat=ac.ID_Articol_Contractat, Cantitate_Comandata_Pachete=ac.Cantitate_Contractata_Pachete))
            db.session.add(comanda)
            db.session.flush()

            # Adăugăm o livrare completă pentru comanda automată
            for detaliu_comanda in comanda.detalii_produse_comanda_rel:
                livrare = LivrareComanda(ID_Detalii_Comanda_Produs=detaliu_comanda.ID_Detalii_Comanda_Produs, Cantitate_Livrata_Pachete=detaliu_comanda.Cantitate_Comandata_Pachete, Numar_Lot_Producator=fake.ean(length=8), Data_Expirare=date.today() + timedelta(days=365), ID_Utilizator_Inregistrare=random.choice(utilizatori).ID_Utilizator)
                livrare.documente_asociate.append(DocumentLivrare(Tip_Document=TipDocument.FACTURA, Numar_Document=f"F-{fake.ean(length=8)}"))
                db.session.add(livrare)
            comanda.Stare_Comanda = "Livrata Complet"

    db.session.commit()
    print(f"-> Creat {Contract.query.count()} contracte, comenzi și livrări.")
    print("\nSeeding finalizat cu succes!")