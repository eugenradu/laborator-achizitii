# Propunere de Arhitectură - Aplicație de Gestiune a Stocurilor

Acest document descrie structura de bază, funcționalitățile și planul de integrare pentru o nouă aplicație dedicată managementului stocurilor de reactivi și consumabile de laborator.

---

## 1. Filozofie și Principii

- **Separarea Responsabilităților (Separation of Concerns):** Aplicația de Achiziții se ocupă de fluxul "de la necesitate la comandă". Această nouă aplicație se va ocupa de fluxul "de la recepție la consum".
- **Dezvoltare Independentă:** Cele două aplicații pot fi dezvoltate, actualizate și scalate independent, reducând riscurile și complexitatea.
- **Integrare prin API:** Comunicația dintre cele două sisteme se va realiza printr-un API securizat și bine definit, asigurând o decuplare curată.

---

## 2. Structura Bazei de Date (Modele SQLAlchemy)

Vom folosi o structură de date optimizată pentru gestiunea stocurilor.

```python
import enum
from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# --- Modele Principale ---

class LocatieDepozitare(db.Model):
    """Definește locațiile fizice unde sunt stocate produsele (ex: Frigider -20C, Dulap Acizi)."""
    __tablename__ = 'Locatii_Depozitare'
    ID_Locatie = db.Column(db.Integer, primary_key=True)
    Nume_Locatie = db.Column(db.Text, unique=True, nullable=False)
    Tip_Locatie = db.Column(db.Text) # Ex: "Frigider", "Congelator", "Dulap"
    Descriere = db.Column(db.Text)

class LotStoc(db.Model):
    """Piesa centrală: reprezintă un lot specific de produs în stoc."""
    __tablename__ = 'Loturi_Stoc'
    ID_Lot_Stoc = db.Column(db.Integer, primary_key=True)
    
    # Cheia de legătură cu aplicația de achiziții. NU este un Foreign Key,
    # ci un simplu ID pentru a putea face referire la produsul din catalogul central.
    ID_Varianta_Comerciala = db.Column(db.Integer, nullable=False, index=True)
    
    Cantitate_Initiala = db.Column(db.Integer, nullable=False)
    Cantitate_Curenta = db.Column(db.Integer, nullable=False)
    Unitate_Masura_Ambalaj = db.Column(db.Text, nullable=False) # Ex: "pachet", "cutie", "flacon"
    
    Data_Intrare_Stoc = db.Column(db.Date, nullable=False, default=date.today)
    Data_Expirare = db.Column(db.Date, nullable=True, index=True)
    
    Numar_Lot_Producator = db.Column(db.Text, nullable=False)
    ID_Locatie_Depozitare = db.Column(db.Integer, db.ForeignKey('Locatii_Depozitare.ID_Locatie'), nullable=False)
    
    # Câmp pentru a stoca informații despre sursa intrării (ex: "Livrare #123 / Factura #456")
    Sursa_Intrare = db.Column(db.Text)
    
    locatie = db.relationship('LocatieDepozitare', backref='loturi_stoc')

class TipMiscareStoc(enum.Enum):
    CONSUM = "Consum"
    AJUSTARE_PLUS = "Ajustare Inventar (Plus)"
    AJUSTARE_MINUS = "Ajustare Inventar (Minus)"
    CASARE = "Casare (Expirat/Defect)"

class MiscareStoc(db.Model):
    """Înregistrează orice ieșire sau ajustare din stoc pentru un lot."""
    __tablename__ = 'Miscari_Stoc'
    ID_Miscare = db.Column(db.Integer, primary_key=True)
    ID_Lot_Stoc = db.Column(db.Integer, db.ForeignKey('Loturi_Stoc.ID_Lot_Stoc'), nullable=False)
    Tip_Miscare = db.Column(db.Enum(TipMiscareStoc), nullable=False)
    Cantitate = db.Column(db.Integer, nullable=False) # Cantitatea mișcată
    Data_Miscare = db.Column(db.Date, nullable=False, default=date.today)
    
    # ID-ul utilizatorului din sistemul de stocuri
    ID_Utilizator = db.Column(db.Integer, nullable=False) 
    Motiv_Observatii = db.Column(db.Text)
    
    lot_stoc = db.relationship('LotStoc', backref='miscari')

```

---

## 3. Structura Aplicației (Blueprints)

- **`main`**: Va conține ruta principală (`/`) care afișează un dashboard cu starea curentă a stocurilor.
- **`stocuri`**: Va gestiona operațiunile principale:
  - Vizualizarea listei de loturi în stoc (cu filtre și căutare).
  - Înregistrarea manuală a unui consum.
  - Înregistrarea unei ajustări de stoc (inventar).
- **`rapoarte`**: Va genera rapoarte utile:
  - Raport de stoc la o anumită dată.
  - Raport de consum pe o perioadă.
  - Raport de produse care urmează să expire.
- **`api`**: Va expune endpoint-urile necesare pentru integrare.

---

## 4. Funcționalități Cheie

1. **Dashboard Principal:**
    - Widget-uri vizuale: "Produse sub stoc minim", "Produse care expiră în următoarele 30 de zile", "Ultimele mișcări".
2. **Recepție Marfă:**
    - **Automată (via API):** Endpoint-ul `/api/receptie_marfa` va fi apelat de aplicația de achiziții.
    - **Manuală:** Un formular pentru a adăuga în stoc produse care nu provin dintr-o achiziție formală (ex: mostre, donații).
3. **Vizualizare Stoc:**
    - O pagină tabelară cu toate loturile din stoc.
    - Filtre puternice: după locație, dată de expirare, produs.
    - Căutare rapidă după lotul producătorului.
4. **Înregistrare Consum/Ajustare:**
    - Un formular simplu unde utilizatorul selectează lotul din stoc, specifică cantitatea consumată/ajustată și un motiv.
    - Aplicația va actualiza automat `Cantitate_Curenta` în `LotStoc` și va crea o înregistrare în `MiscareStoc`.
5. **Alerte și Notificări:**
    - (Opțional, V2) Un sistem care trimite email-uri sau afișează notificări pentru stocuri minime atinse sau produse aproape de expirare.

---

## 5. Plan de Integrare cu Aplicația de Achiziții

Acesta este punctul critic care leagă cele două sisteme.

### Modificări în Aplicația de Achiziții

1. În formularul de înregistrare a unei **livrări** (`LivrareComanda`), se vor adăuga două câmpuri noi, obligatorii:
    - `Numar_Lot_Producator` (Text)
    - `Data_Expirare` (Date)
2. După ce o livrare este marcată ca fiind completă și corectă, utilizatorul va avea un buton nou: **"Trimite în Gestiunea de Stocuri"**.
3. La apăsarea acestui buton, aplicația de achiziții va face un request `POST` către endpoint-ul aplicației de stocuri.

### Endpoint în Noua Aplicație de Stocuri

- **URL:** `POST /api/receptie_marfa`
- **Securitate:** Endpoint-ul va fi protejat cu un API Key (un token secret, partajat între cele două aplicații).
- **Request Body (JSON):**

  ```json
  {
    "id_varianta_comerciala": 123, // ID-ul din baza de date de achiziții
    "cantitate_receptionata": 10,
    "unitate_masura_ambalaj": "pachet", // Ex: "cutie", "flacon"
    "lot_producator": "A2024-XYZ-01",
    "data_expirare": "2026-12-31", // Format YYYY-MM-DD
    "sursa_intrare": "Livrare #78 / Factura #F12345" // Text informativ pentru trasabilitate
  }
  ```

- **Acțiune:** La primirea acestui request, aplicația de stocuri:
  1. Validează API Key-ul.
  2. Validează datele primite.
  3. Creează o nouă înregistrare în tabela `LotStoc`.
  4. Returnează un răspuns de succes (HTTP 201 Created) sau o eroare.

Această arhitectură oferă o bază solidă, flexibilă și scalabilă pentru viitor.
