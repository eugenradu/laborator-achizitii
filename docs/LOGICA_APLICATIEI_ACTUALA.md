# Descrierea Logicii Aplicatei (Stare Curentă)

Acest document descrie funcționarea și interacțiunile modulelor cheie ale aplicației, așa cum sunt implementate în prezent. Servește ca un ghid de referință pentru dezvoltarea viitoare.

---

## 1. Modulul `auth` (`blueprints/auth.py`)

- **Scop:** Gestionează autentificarea, înregistrarea și sesiunile utilizatorilor.
- **Entități Cheie:** `Utilizator`.
- **Funcționalități Principale:**
  - Înregistrarea unui nou utilizator.
  - Autentificarea (login) și deautentificarea (logout).
- **Interacțiuni:**
  - Acționează ca un "gardian" pentru toate celelalte module prin decoratorul `@login_required`.
  - ID-ul utilizatorului curent (`current_user`) este folosit pentru a atribui proprietatea asupra documentelor create (referate, oferte, etc.).

---

## 2. Modulul `produse` (`blueprints/produse.py`)

- **Scop:** Gestionează catalogul central de produse, producători și categorii.
- **Entități Cheie:** `Produs`, `Categorie`, `Producator`, `VariantaComercialaProdus`.
- **Funcționalități Principale:**
  - CRUD complet pentru toate entitățile menționate.
  - Import de produse generice dintr-un fișier JSON.
- **Interacțiuni:**
  - Este **furnizorul principal de date** pentru modulele `Referate` și `Oferte`.
  - `Referate` consumă lista de `Produs` (produse generice).
  - `Oferte` consumă lista de `VariantaComercialaProdus` (produse specifice).

---

## 3. Modulul `referate` (`blueprints/referate.py`)

- **Scop:** Gestionează procesul intern de planificare a achizițiilor.
- **Entități Cheie:** `ReferatNecesitate`, `ProdusInReferat`, `Lot`.
- **Funcționalități Principale:**
  - CRUD pentru `ReferatNecesitate`.
  - Adăugarea de `Produs` (generic) într-un referat, specificând cantitatea.
  - Crearea de `Lot`-uri și alocarea produselor din referat în aceste loturi.
  - Editarea observațiilor pe un referat.
- **Interacțiuni:**
  - **Consumă** date din `produse` (lista de `Produs` și `Categorie`).
  - **Apelează** API-ul `get_produse_by_categorie` pentru a popula dinamic un dropdown.
  - **Furnizează** `Lot`-uri pentru viitorul modul de `Licitatii`.
  - **Este integrat bidirecțional cu `Oferte`**:
    - Afișează o listă de oferte care au fost asociate cu el.
    - Oferă o scurtătură ("Adaugă Ofertă pentru Acest Referat") pentru a crea o nouă ofertă cu referatul curent pre-selectat.

---

## 4. Modulul `oferte` (`blueprints/oferte.py`)

- **Scop:** Gestionează înregistrarea și managementul ofertelor de preț de la distribuitori.
- **Entități Cheie:** `Oferta`, `ArticolOferta`.
- **Funcționalități Principale:**
  - CRUD complet pentru `Oferta`.
  - Adăugare/ștergere dinamică de `ArticolOferta` în formulare.
  - Asociere opțională cu un `Referat` sau o `Licitatie`.
  - Filtrare dinamică în doi pași pentru selecția produselor.
  - Căutare după nume furnizor sau număr de înregistrare, cu paginare.
- **Interacțiuni:**
  - **Consumă** date din `produse` (lista de `Produs` și `Producator`) și din `furnizori` (lista de `Furnizor`).
  - **Apelează** API-ul `get_variante_by_produs` pentru filtrarea în doi pași.
  - **Apelează** API-ul `api_adauga_varianta_comerciala` pentru a crea dinamic variante noi.
  - **Apelează** API-ul `api_adauga_producator` pentru a crea dinamic producători noi.
  - **Apelează** API-ul `api_adauga_furnizor` pentru a crea dinamic furnizori noi.

---

## 5. Modulul `furnizori` (`blueprints/furnizori.py`)

- **Scop:** Gestionează catalogul central de furnizori/distribuitori.
- **Entități Cheie:** `Furnizor`.
- **Funcționalități Principale:**
  - CRUD complet pentru entitatea `Furnizor`.
- **Interacțiuni:**
  - Este **furnizor de date** pentru modulul `Oferte`.

---

## 6. Modulul `api` (`blueprints/api.py`)

- **Scop:** Centralizează toate endpoint-urile API care returnează date în format JSON.
- **Entități Cheie:** Citește (`Produs`, `VariantaComercialaProdus`, `Producator`). Creează (`VariantaComercialaProdus`, `Furnizor`, `Producator`).
- **Funcționalități Principale (Endpoint-uri):**
  - `/produse_by_categorie/<id>`: Returnează produsele dintr-o categorie.
  - `/variante_by_produs/<id>`: Returnează variantele comerciale ale unui produs generic.
  - `/variante_comerciale/adauga`: Creează o nouă variantă comercială în baza de date.
- `/furnizori/adauga`: Creează un nou furnizor în baza de date.
- `/producatori/adauga`: Creează un nou producător în baza de date.
- **Interacțiuni:**
  - Este **apelat** prin JavaScript (Fetch API) din template-urile modulelor `Referate` și `Oferte` pentru a oferi interactivitate formularelor.
