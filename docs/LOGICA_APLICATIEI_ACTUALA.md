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
  - Import de produse generice dintr-un fișier JSON, cu un flux interactiv pentru crearea de categorii noi (solicită confirmarea utilizatorului).
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
  - **Editarea unui referat în starea "Ciornă"**: Permite ștergerea produselor din referat, ștergerea loturilor (dacă nu sunt în proceduri) și scoaterea produselor din loturi.
  - **Tranziția stării din "Ciornă" în "În Aprobare"**: Permite trimiterea unui referat pentru revizuire, blocându-l pentru editări ulterioare. Acțiunea este condiționată de validări (referatul trebuie să conțină produse și toate produsele trebuie să fie alocate în loturi).
  - **Flux de Aprobare/Respingere**: Un utilizator poate aproba un referat (stare -> `Aprobat`) sau îl poate respinge (stare -> `Ciornă`). Respingerea necesită un motiv, care este salvat și afișat creatorului pentru corecții.
  - Clonarea unui referat existent, inclusiv a produselor solicitate.
  - Căutare după număr, creator sau observații, cu paginare în lista de referate.
- **Interacțiuni:**
  - **Consumă** date din `produse` (lista de `Produs` și `Categorie`).
  - **Apelează** API-ul `get_produse_by_categorie` pentru a popula dinamic un dropdown.
  - **Furnizează** `Lot`-uri pentru modulul `proceduri`.
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
  - Asociere opțională cu un `Referat` sau o `ProceduraAchizitie`.
  - Filtrare contextuală a produselor: la crearea unei oferte pentru un referat/procedură, lista de produse este restrânsă la cele solicitate în contextul respectiv.
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

## 6. Modulul `proceduri` (`blueprints/proceduri.py`)

- **Scop:** Gestionează procedurile de achiziție, de la inițiere până la finalizare.
- **Entități Cheie:** `ProceduraAchizitie`, `TipProcedura`, `Lot`.
- **Funcționalități Principale:**
  - Listarea tuturor procedurilor de achiziție.
  - Inițierea unei noi proceduri, cu posibilitatea de a consolida loturi din mai multe referate.
  - Vizualizarea detaliilor unei proceduri, inclusiv loturile și ofertele asociate.
  - Generarea unui document text (.txt) cu specificațiile complete ale procedurii.
- **Interacțiuni:**
  - **Consumă** `Lot`-uri disponibile din modulul `referate`.
  - **Este integrat bidirecțional cu `Oferte`**:
    - Afișează o listă de oferte care au fost asociate cu el.
    - Oferă o scurtătură ("Adaugă Ofertă pentru Această Procedură") pentru a crea o nouă ofertă cu procedura curentă pre-selectată.

---

## 7. Modulul `contracte` (`blueprints/contracte.py`)

- **Scop:** Gestionează formalizarea legală a achizițiilor, de la generarea contractului până la vizualizarea detaliilor acestuia.
- **Entități Cheie:** `Contract`, `ArticolContractat`.
- **Funcționalități Principale:**
  - Distincție între `CONTRACT_FERM` (cu livrare integrală) și `ACORD_CADRU` (cu comenzi subsecvente).
  - Listarea tuturor contractelor.
  - Vizualizarea detaliilor unui contract, inclusiv loturile și articolele contractate.
  - Generarea unui nou contract pe baza unei oferte câștigătoare pentru un lot dintr-o procedură.
  - Căutare după număr, furnizor sau creator, cu paginare în lista de contracte.
  - Consolidarea mai multor loturi câștigate de același furnizor (în aceeași procedură) într-un singur contract.
- **Interacțiuni:**
  - **Este inițiat** din modulul `proceduri`, prin interfața de adjudecare a ofertelor pe lot.
  - **Consumă** date din `oferte` (furnizor, prețuri, articole) și `proceduri` (loturi, produse) pentru a pre-popula formularul de creare.
  - **Interacționează strâns cu modulul `comenzi`**:
    - Generează automat o comandă la crearea unui `CONTRACT_FERM`.
    - Servește ca bază pentru crearea manuală de comenzi subsecvente în cazul unui `ACORD_CADRU`.

---

## 8. Modulul `comenzi` (`blueprints/comenzi.py`)

- **Scop:** Gestionează comenzile plasate către furnizori, fie automat (pentru contracte ferme), fie manual (pentru acorduri-cadru).
- **Entități Cheie:** `ComandaGeneral`, `DetaliiComandaProdus`.
- **Funcționalități Principale:**
  - Listarea și vizualizarea detaliată a tuturor comenzilor.
  - Crearea de comenzi subsecvente în baza unui acord-cadru, cu validarea cantităților disponibile.
  - Vizualizarea comenzilor (atât cele automate, cât și cele manuale) în pagina de detalii a contractului părinte.
- **Interacțiuni:**
  - **Este inițiat** din modulul `contracte`.
  - **Va furniza** date pentru viitorul modul de `Stocuri` (recepția mărfii).

---

## 9. Modulul `api` (`blueprints/api.py`)

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
