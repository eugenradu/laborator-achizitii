# Foaie de Parcurs (TODO)

Acest document inventariază sarcinile planificate pentru dezvoltarea aplicației, organizate pe priorități.

---

### Următorul Obiectiv Major

- [ ] **Implementare Modul Gestiune Stocuri:**
  - [ ] Crearea blueprint-ului `stocuri.py`.
  - [ ] Implementarea logicii de recepție a mărfii (creare `LotStoc` din `LivrareComanda`).
  - [ ] Implementarea logicii de consum de stoc.

---

### Îmbunătățiri și Refactorizări Planificate

- [ ] **Îmbunătățiri Generale de Utilizabilitate și Performanță:**
  - *Toate listele principale (Referate, Proceduri, Contracte) au acum funcționalități de căutare și paginare.*
- [ ] **Refactorizare Entități:**
  - [ ] Crearea entității `Departament` și legarea ei de `ReferatNecesitate` pentru trasabilitate bugetară.
  - [ ] Crearea entităților `UnitateMasura` și `Moneda` pentru a standardiza datele.
- [ ] **Îmbunătățiri Tehnice:**
  - [ ] Îmbunătățirea validărilor în formulare (atât pe frontend, cât și pe backend).
  - [ ] Standardizarea mesajelor flash și a stilurilor CSS pentru butoane/alerte.
  - [ ] Verificarea și adăugarea de indecși în baza de date pentru a optimiza interogările frecvente.

---

### Funcționalități Finalizate (Recent)

- [x] **Îmbunătățire Import Produse din JSON** (cu confirmare pentru categorii noi)
- [x] **Funcționalitate de Clonare a Referatelor**
- [x] **Editare Referate în Stare "Ciornă"** (ștergere produse/loturi)
- [x] **Tranziție Stare Referat (Ciornă -> În Aprobare)** cu validări
- [x] **Flux de Aprobare/Respingere Referate** (cu motiv de respingere)
- [x] **Căutare și Paginare în Lista de Referate**
- [x] **Decizie de a separa Modulul de Stocuri**
- [x] **Refactorizare Creare Procedură (Super-Loturi)**
- [x] **Repararea fluxului de creare a contractelor (aliniere cu Super-Loturi)**
- [x] **Căutare și Paginare în Lista de Proceduri și Contracte**
- [x] **Implementare Modul Proceduri de Achiziție** (bază)
- [x] **Adăugare Dinamică de Entități** (Furnizori, Producători din formulare)
- [x] **Implementare Modul Contracte (Bază)**
