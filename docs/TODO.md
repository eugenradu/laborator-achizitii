# Foaie de Parcurs (TODO)

Acest document inventariază sarcinile planificate pentru dezvoltarea aplicației, organizate pe priorități.

**Decizie Arhitecturală (2024-05-21):** Modulul de Gestiune a Stocurilor va fi dezvoltat ca o aplicație separată. Integrarea se va face printr-un API, unde aplicația de achiziții va notifica aplicația de stocuri la recepția unei livrări.

---

### Următorul Obiectiv Major

- [ ] **Implementare Dashboard Principal:**
  - [ ] Crearea unei rute noi în `main.py` pentru dashboard.
  - [ ] Implementarea de interogări pentru a extrage statistici cheie (ex: nr. referate în aprobare, valoare contracte pe lună, etc.).
  - [ ] Crearea unui template `dashboard.html` cu widget-uri vizuale pentru afișarea statisticilor.

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
- [x] **Implementare Modul de Livrări** (inclusiv API)
- [x] **Repararea fluxului de creare a contractelor (aliniere cu Super-Loturi)**
- [x] **Căutare și Paginare în Lista de Proceduri și Contracte**
- [x] **Implementare Modul Proceduri de Achiziție** (bază)
- [x] **Adăugare Dinamică de Entități** (Furnizori, Producători din formulare)
- [x] **Implementare Modul Contracte (Bază)**
