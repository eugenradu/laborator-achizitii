# Foaie de Parcurs (TODO)

Acest document inventariază sarcinile planificate pentru dezvoltarea viitoare a aplicației.

---

### Îmbunătățiri și Refactorizări

- [x] **Refactorizare `Furnizor` (Finalizat):**
  - [x] Crearea entității `Furnizor` pentru a înlocui câmpul text `Nume_Distribuitor` din `Oferta`.
  - [x] Adăugarea unui modul de management CRUD pentru furnizori.
- [ ] **Refactorizare Entități:**
  - [ ] Crearea entității `Departament` și legarea eidif de `ReferatNecesitate` pentru trasabilitate bugetară.
  - [ ] Crearea entităților `UnitateMasura` și `Moneda` pentru a standardiza datele.
- [x] Adăugare dinamică de furnizori din pagina de oferte (similar cu variantele comerciale).
- [x] Adăugare dinamică de producători din pagina de oferte (flux secvențial).
- [ ] Adăugarea unei funcționalități de căutare/filtrare în listele principale:
  - [x] Căutare/Filtrare în lista de produse.
  - [x] Căutare/Filtrare în lista de variante comerciale.
  - [x] Căutare în lista de oferte.
  - [ ] Filtrare avansată în lista de referate.
- [ ] Implementarea paginării în toate listele lungi:
  - [x] Paginare în lista de produse.
  - [x] Paginare în lista de variante comerciale.
  - [x] Paginare în lista de oferte.
  - [ ] Paginare în lista de referate.
- [ ] Îmbunătățirea validărilor în formulare (atât pe frontend, cât și pe backend).
- [ ] Standardizarea mesajelor flash și a stilurilor CSS pentru butoane/alerte.
- [ ] Verificarea și adăugarea de indecși în baza de date pentru a optimiza interogările frecvente.

### Module Noi (Funcționalități Majore)

- [ ] **Implementare Modul Licitatii:**
  - [ ] Crearea blueprint-ului `licitatii.py`.
  - [ ] Migrarea logicii de licitații din `app.py` în noul blueprint.
  - [ ] Integrarea cu noul sistem de `Oferte` (asocierea unei oferte la o licitație).
- [ ] **Implementare Modul Contracte:**
  - [ ] Crearea blueprint-ului `contracte.py`.
  - [ ] Implementarea logicii de creare a unui contract pe baza unei oferte câștigătoare.
- [ ] **Implementare Modul Gestiune Stocuri:**
  - [ ] Crearea blueprint-ului `stocuri.py`.
  - [ ] Implementarea logicii de recepție a mărfii (creare `LotStoc` din `LivrareComanda`).
  - [ ] Implementarea logicii de consum de stoc.
