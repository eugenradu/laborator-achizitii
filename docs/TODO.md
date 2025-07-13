# Foaie de Parcurs (TODO)

Acest document inventariază sarcinile planificate pentru dezvoltarea aplicației, organizate pe priorități.

---

### Următorul Obiectiv Major

- [ ] **Implementare Modul Contracte:**
  - [x] Definirea modelelor de date `Contract` și `ArticolContractat` (cu relație M-M între Contract și Lot).
  - [ ] Implementarea interfeței de adjudecare în pagina de detalii a procedurii.
  - [ ] Crearea formularului de adăugare contract (`adauga_contract.html`).
  - [ ] Implementarea logicii de pre-populare a formularului cu datele ofertei și lotului inițial.
  - [ ] Adăugarea în formular a funcționalității de a selecta loturi suplimentare (de la același furnizor, din aceeași procedură).
  - [ ] Implementarea logicii de salvare a contractului consolidat.
  - [x] Implementarea paginii de listare a contractelor.
  - [x] Implementarea paginii de detalii pentru contracte.

---

### Funcționalități Noi Planificate

- [ ] **Implementare Modul Gestiune Stocuri:**
  - [ ] Crearea blueprint-ului `stocuri.py`.
  - [ ] Implementarea logicii de recepție a mărfii (creare `LotStoc` din `LivrareComanda`).
  - [ ] Implementarea logicii de consum de stoc.

---

### Îmbunătățiri și Refactorizări Planificate

- [ ] **Refactorizare Creare Procedură (Super-Loturi):**
  - [ ] Modificarea modelului de date pentru a permite crearea de loturi specifice unei proceduri (`LotProcedura`).
  - [ ] Implementarea unei interfețe de editare a procedurii care permite crearea de "super-loturi".
  - [ ] Utilizatorul va putea aloca produse din loturile originale (din referate) în noile "super-loturi", având opțiunea de a exclude anumite produse.
- [ ] **Îmbunătățiri Generale de Utilizabilitate și Performanță:**
  - [ ] Adăugarea unei funcționalități de căutare și filtrare în listele principale (oferte, referate, proceduri, etc.).
  - [ ] Implementarea paginării în toate listele lungi pentru a îmbunătăți performanța.
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
- [x] **Implementare Modul Proceduri de Achiziție** (bază)
- [x] **Adăugare Dinamică de Entități** (Furnizori, Producători din formulare)
- [x] **Refactorizare `Furnizor`** (entitate dedicată)
