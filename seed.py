import random
from datetime import date, timedelta
from faker import Faker
from models import (db, Utilizator, Categorie, Producator, Furnizor, Produs, 
                    VariantaComercialaProdus, ReferatNecesitate, ProdusInReferat, Lot)

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
    for i in range(10):
        referat = ReferatNecesitate(
            Numar_Referat=f"REF-{i+1}-{date.today().year}",
            Data_Creare=date.today() - timedelta(days=random.randint(5, 100)),
            Stare=random.choice(['Ciorna', 'In Aprobare', 'Aprobat']),
            ID_Utilizator_Creare=random.choice(utilizatori).ID_Utilizator,
            Observatii=fake.sentence()
        )
        db.session.add(referat)
        db.session.flush() # Pentru a obține ID-ul referatului

        # Adăugăm produse în referat
        produse_in_referat = []
        for _ in range(random.randint(2, 8)):
            pir = ProdusInReferat(
                ID_Referat=referat.ID_Referat,
                ID_Produs_Generic=random.choice(produse).ID_Produs,
                Cantitate_Solicitata=random.randint(1, 20)
            )
            produse_in_referat.append(pir)
        db.session.add_all(produse_in_referat)
        db.session.flush() # Pentru a obține ID-urile

        # Creăm 1-2 loturi și alocăm produse
        if referat.Stare == 'Aprobat':
            for j in range(random.randint(1, 2)):
                lot = Lot(
                    ID_Referat=referat.ID_Referat,
                    Nume_Lot=f"Lot {j+1} - {referat.Numar_Referat}",
                    Descriere_Lot=fake.bs()
                )
                db.session.add(lot)

    db.session.commit()
    print("-> Creat 10 referate de necesitate cu produse și loturi.")
    print("\nSeeding finalizat cu succes!")