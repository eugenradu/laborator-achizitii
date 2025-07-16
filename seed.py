from datetime import date, timedelta
from faker import Faker
from models import (db, Utilizator, Categorie, Producator, Furnizor, Produs,
                    VariantaComercialaProdus, ReferatNecesitate, ProdusInReferat, Lot, ProdusInLot,
                    StareReferat, ProceduraAchizitie, TipProcedura, LotProcedura, Oferta, ArticolOferta,
                    Contract, TipContract, ArticolContractat, ComandaGeneral, DetaliiComandaProdus,
                    LivrareComanda, DocumentLivrare, TipDocument)

fake = Faker('ro_RO') # Folosim date specifice României unde e posibil
import random

def seed_data():
    """Populează baza de date cu date de test complete."""
    print("Începe popularea bazei de date...")

    # Curățarea tabelelor în ordinea corectă a dependențelor
    db.session.query(DocumentLivrare).delete()
    db.session.query(LivrareComanda).delete()
    db.session.query(DetaliiComandaProdus).delete()
    db.session.query(ComandaGeneral).delete()
    db.session.query(ArticolContractat).delete()
    db.session.query(Contract).delete()
    db.session.query(ArticolOferta).delete()
    db.session.query(Oferta).delete()
    db.session.query(LotProcedura.articole_incluse.property.secondary).delete()
    db.session.query(LotProcedura).delete()
    db.session.query(ProceduraAchizitie).delete()
    db.session.query(ProdusInLot).delete()
    db.session.query(Lot).delete()
    db.session.query(ProdusInReferat).delete()
    db.session.query(ReferatNecesitate).delete()
    db.session.query(VariantaComercialaProdus).delete()
    db.session.query(Produs).delete()
    db.session.query(Utilizator).delete()
    db.session.query(Categorie).delete()
    db.session.query(Producator).delete()
    db.session.query(Furnizor).delete()
    db.session.commit()
    print("-> Baza de date a fost curățată.")

    # 1. Utilizatori
    # Creează utilizatorul admin cu parola adminpass
    admin = Utilizator(Nume_Utilizator="admin", Email="admin@example.com")
    admin.set_password("adminpass")
    db.session.add(admin)

    # Creează alți 2 utilizatori cu date generate aleator
    for _ in range(2):
        u = Utilizator(Nume_Utilizator=fake.user_name(), Email=fake.email())  # Generează nume aleator
        u.set_password("1234")  # Setează parola implicită pentru ceilalți utilizatori
        db.session.add(u)
    db.session.commit()

    # Preluăm toți utilizatorii din baza de date pentru a-i folosi mai târziu
    utilizatori = Utilizator.query.all()
    print(f"-> Creat {len(utilizatori)} utilizatori.")

    # 2. Categorii, Producători, Furnizori
    categorii = [Categorie(Nume_Categorie=cat) for cat in ['Reactivi', 'Consumabile Laborator', 'Sticlarie', 'Echipamente']]
    producatori = [Producator(Nume_Producator=fake.company()) for _ in range(10)]
    furnizori = [Furnizor(Nume_Furnizor=f"{fake.company()} SRL") for _ in range(5)]
    db.session.add_all(categorii + producatori + furnizori)
    db.session.commit()
    print(f"-> Creat {len(categorii)} categorii, {len(producatori)} producători, {len(furnizori)} furnizori.")

    # 3. Produse Generice
    produse = [
        Produs(Nume_Generic=f"Kit {fake.word().capitalize()}", ID_Categorie=random.choice(categorii).ID_Categorie) for _ in range(15)
    ]
    db.session.add_all(produse)
    db.session.commit()
    print(f"-> Creat {len(produse)} produse generice.")

    # 4. Variante Comerciale
    variante = []
    for produs in produse:
        for _ in range(random.randint(1, 4)):
            varianta = VariantaComercialaProdus(
                ID_Produs_Generic=produs.ID_Produs,
                ID_Producator=random.choice(producatori).ID_Producator,
                Cod_Catalog=fake.ean(length=8),
                Descriere_Ambalare=f"Cutie x {random.choice([10, 25, 50, 100])} buc.",
                Cantitate_Standard_Ambalare=random.randint(1, 100)
            )
            variante.append(varianta)
    db.session.add_all(variante)
    db.session.commit()
    print(f"-> Creat {len(variante)} variante comerciale.")

    # 5. Referate de Necesitate
    referate_aprobate = []
    produse_aprobate_in_referate = []
    for i in range(10):
        stare_aleasa = random.choice(list(StareReferat))
        referat = ReferatNecesitate(
            Numar_Referat=f"REF-{i+1}-{date.today().year}",
            Data_Creare=date.today() - timedelta(days=random.randint(5, 100)),
            Stare=stare_aleasa,
            ID_Utilizator_Creare=random.choice(utilizatori).ID_Utilizator
        )
        db.session.add(referat)
        db.session.flush()
        produse_in_referat = []
        for produs_generic in random.sample(produse, random.randint(3, 8)):
            pir = ProdusInReferat(
                ID_Referat=referat.ID_Referat,
                ID_Produs_Generic=produs_generic.ID_Produs,
                Cantitate_Solicitata=random.randint(1, 20)
            )
            produse_in_referat.append(pir)
        db.session.add_all(produse_in_referat)
        db.session.flush()
        if stare_aleasa == StareReferat.APROBAT:
            referate_aprobate.append(referat)
            produse_aprobate_in_referate.extend(produse_in_referat)
    db.session.commit()
    print(f"-> Creat 10 referate de necesitate, din care {len(referate_aprobate)} sunt aprobate.")

    # 6. Proceduri de Achiziție și Super-Loturi
    proceduri = []
    produse_disponibile = list(produse_aprobate_in_referate)
    for i in range(3):
        procedura = ProceduraAchizitie(
            Nume_Procedura=f"PA-{i+1} - {fake.catch_phrase()}",
            Tip_Procedura=random.choice(list(TipProcedura)),
            ID_Utilizator_Creare=random.choice(utilizatori).ID_Utilizator
        )
        db.session.add(procedura)
        db.session.flush()
        for j in range(random.randint(1, 2)):
            if not produse_disponibile: break
            super_lot = LotProcedura(ID_Procedura=procedura.ID_Procedura, Nume_Lot=f"Super-Lot {j+1}")
            produse_de_alocat = random.sample(produse_disponibile, k=min(len(produse_disponibile), random.randint(2, 4)))
            super_lot.articole_incluse.extend(produse_de_alocat)
            produse_disponibile = [p for p in produse_disponibile if p not in produse_de_alocat]
            db.session.add(super_lot)
        proceduri.append(procedura)
    db.session.commit()
    print(f"-> Creat {len(proceduri)} proceduri cu Super-Loturi.")

    # 7. Oferte pentru Proceduri
    oferte_castigatoare_procedura = {}
    for procedura in proceduri:
        for lot_proc in procedura.loturi_procedura:
            oferta_minima = None
            pret_minim = float('inf')
            for furnizor in random.sample(furnizori, k=random.randint(2, 3)):
                oferta = Oferta(ID_Furnizor=furnizor.ID_Furnizor, ID_Procedura=procedura.ID_Procedura)
                db.session.add(oferta)
                db.session.flush()
                valoare_totala_oferta_pe_lot = 0
                for articol_solicitat in lot_proc.articole_incluse:
                    if not articol_solicitat.produs_generic_req.variante_comerciale: continue
                    varianta_aleasa = random.choice(articol_solicitat.produs_generic_req.variante_comerciale)
                    pret = round(random.uniform(10.0, 500.0), 2)
                    db.session.add(ArticolOferta(ID_Oferta=oferta.ID_Oferta, ID_Produs_Referat=articol_solicitat.ID_Produs_Referat, ID_Varianta_Comerciala=varianta_aleasa.ID_Varianta_Comerciala, Pret_Unitar_Pachet=pret))
                    valoare_totala_oferta_pe_lot += pret * articol_solicitat.Cantitate_Solicitata
                if valoare_totala_oferta_pe_lot < pret_minim:
                    pret_minim = valoare_totala_oferta_pe_lot
                    oferta_minima = oferta
            if oferta_minima:
                oferte_castigatoare_procedura[lot_proc.ID_Lot_Procedura] = oferta_minima
    print("-> Creat oferte pentru proceduri.")

    # 8. Ofertă direct pe Referat
    if referate_aprobate:
        referat_pt_oferta_directa = random.choice(referate_aprobate)
        oferta_directa = Oferta(ID_Furnizor=random.choice(furnizori).ID_Furnizor, ID_Referat=referat_pt_oferta_directa.ID_Referat)
        db.session.add(oferta_directa)
        db.session.flush()
        for articol_solicitat in referat_pt_oferta_directa.produse_in_referate:
            if not articol_solicitat.produs_generic_req.variante_comerciale: continue
            varianta_aleasa = random.choice(articol_solicitat.produs_generic_req.variante_comerciale)
            pret = round(random.uniform(10.0, 500.0), 2)
            db.session.add(ArticolOferta(ID_Oferta=oferta_directa.ID_Oferta, ID_Produs_Referat=articol_solicitat.ID_Produs_Referat, ID_Varianta_Comerciala=varianta_aleasa.ID_Varianta_Comerciala, Pret_Unitar_Pachet=pret))
    print("-> Creat ofertă direct pe referat.")

    db.session.commit()

    # 9. Contracte și Comenzi
    for lot_proc_id, oferta_castigatoare in oferte_castigatoare_procedura.items():
        lot_proc = LotProcedura.query.get(lot_proc_id)
        tip_contract = random.choice(list(TipContract))
        valoare_contract = sum(ao.Pret_Unitar_Pachet * ao.produs_referat_ofertat.Cantitate_Solicitata for ao in oferta_castigatoare.articole)
        contract = Contract(Tip_Contract=tip_contract, ID_Procedura=oferta_castigatoare.ID_Procedura, ID_Furnizor=oferta_castigatoare.ID_Furnizor, Pret_Total_Contract=valoare_contract, Numar_Contract=f"CONTRACT-{fake.ean(length=8)}", ID_Utilizator_Creare=random.choice(utilizatori).ID_Utilizator)
        contract.loturi_procedura_contractate.append(lot_proc)
        for art_oferta in oferta_castigatoare.articole:
            ac = ArticolContractat(ID_Produs_Referat=art_oferta.ID_Produs_Referat, ID_Varianta_Comerciala=art_oferta.ID_Varianta_Comerciala, Cantitate_Contractata_Pachete=art_oferta.produs_referat_ofertat.Cantitate_Solicitata, Pret_Unitar_Pachet_Contract=art_oferta.Pret_Unitar_Pachet)
            contract.articole_contractate.append(ac)
        db.session.add(contract)
        db.session.flush()

        if tip_contract == TipContract.CONTRACT_FERM:
            comanda = ComandaGeneral(ID_Contract=contract.ID_Contract, Numar_Comanda=f"CMD-AUT-{contract.ID_Contract}", Stare_Comanda="Generata Automat", ID_Utilizator_Creare=random.choice(utilizatori).ID_Utilizator)
            for ac in contract.articole_contractate:
                comanda.detalii_produse_comanda_rel.append(DetaliiComandaProdus(ID_Articol_Contractat=ac.ID_Articol_Contractat, Cantitate_Comandata_Pachete=ac.Cantitate_Contractata_Pachete))
            db.session.add(comanda)
            comanda.Stare_Comanda = "Livrata Complet"
        elif tip_contract == TipContract.ACORD_CADRU:
            comanda_partiala = ComandaGeneral(ID_Contract=contract.ID_Contract, Numar_Comanda=f"CMD-SUB-{contract.ID_Contract}", Stare_Comanda="Lansata", ID_Utilizator_Creare=random.choice(utilizatori).ID_Utilizator)
            for ac in contract.articole_contractate:
                cant_comandata = ac.Cantitate_Contractata_Pachete // 2
                if cant_comandata > 0:
                    comanda_partiala.detalii_produse_comanda_rel.append(DetaliiComandaProdus(ID_Articol_Contractat=ac.ID_Articol_Contractat, Cantitate_Comandata_Pachete=cant_comandata))
            db.session.add(comanda_partiala)
    db.session.commit()
    print("-> Creat contracte și comenzi.")

    # 10. Livrări
    comenzi_lansate = ComandaGeneral.query.all()
    for comanda in comenzi_lansate:
        prima_livrare_pentru_comanda = True
        for detaliu_comanda in comanda.detalii_produse_comanda_rel:
            cant_livrata = detaliu_comanda.Cantitate_Comandata_Pachete if comanda.Stare_Comanda == "Livrata Complet" else detaliu_comanda.Cantitate_Comandata_Pachete // 2
            if cant_livrata <= 0: continue
            livrare = LivrareComanda(ID_Detalii_Comanda_Produs=detaliu_comanda.ID_Detalii_Comanda_Produs, Cantitate_Livrata_Pachete=cant_livrata, Numar_Lot_Producator=fake.ean(length=8), Data_Expirare=date.today() + timedelta(days=365), ID_Utilizator_Inregistrare=random.choice(utilizatori).ID_Utilizator)
            if prima_livrare_pentru_comanda:
                livrare.documente_asociate.append(DocumentLivrare(Tip_Document=TipDocument.FACTURA, Numar_Document=f"F-{fake.ean(length=8)}"))
                livrare.documente_asociate.append(DocumentLivrare(Tip_Document=TipDocument.AVIZ_EXPEDITIE, Numar_Document=f"AVZ-{fake.ean(length=8)}"))
                prima_livrare_pentru_comanda = False
            db.session.add(livrare)
    db.session.commit()
    print("-> Creat livrări.")

    print("Seeding finalizat cu succes!")
