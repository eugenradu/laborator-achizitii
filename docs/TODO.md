# Foaie de Parcurs (TODO)

Acest document inventariază sarcinile planificate pentru dezvoltarea viitoare a aplicației.

---

### Module Noi (Funcționalități Majore)

- [ ] **Implementare Modul Proceduri de Achiziție:**
  - [x] Refactorizarea modelului `Licitatie` în `ProceduraAchizitie`.
  - [x] Adăugarea unui câmp `Tip_Procedura` (Enum).
  - [x] Crearea blueprint-ului `proceduri.py`.
  - [x] Implementarea unui formular de creare care grupează loturile pe referate.
  - [x] Integrarea cu `Oferte` (asociere și pre-selectare).
  - [x] Generare documentație text pentru o procedură.
- [ ] **Implementare Modul Contracte:**
  - [ ] Crearea blueprint-ului `contracte.py`.
  - [ ] Implementarea logicii de creare a unui contract pe baza unei oferte câștigătoare dintr-o procedură.
- [ ] **Implementare Modul Gestiune Stocuri:**
  - [ ] Crearea blueprint-ului `stocuri.py`.
  - [ ] Implementarea logicii de recepție a mărfii (creare `LotStoc` din `LivrareComanda`).
  - [ ] Implementarea logicii de consum de stoc.

- [x] **Refactorizare `Furnizor` (Finalizat):**
  - [x] Crearea entității `Furnizor` pentru a înlocui câmpul text `Nume_Distribuitor` din `Oferta`.
  - [x] Adăugarea unui modul de management CRUD pentru furnizori.
- [ ] **Refactorizare Entități:**
  - [ ] Crearea entității `Departament` și legarea eidif de `ReferatNecesitate` pentru trasabilitate bugetară.
  - [ ] Crearea entităților `UnitateMasura` și `Moneda` pentru a standardiza datele.
- [x] Adăugare dinamică de furnizori din pagina de oferte (similar cu variantele comerciale).
- [x] Adăugare dinamică de producători din pagina de oferte (flux secvențial).
- [ ] **Funcționalitate de Clonare a Referatelor:**
- [x] **Funcționalitate de Clonare a Referatelor (Finalizat)**
- [ ] Adăugarea unei funcționalități de căutare/filtrare în listele principale:
- [ ] Adăugarea unei funcționalități de căutare/filtrare în listele principale (oferte, referate, etc.).
- [ ] Implementarea paginării în toate listele lungi pentru a îmbunătăți performanța.
- [ ] Îmbunătățirea validărilor în formulare (atât pe frontend, cât și pe backend).
- [ ] Standardizarea mesajelor flash și a stilurilor CSS pentru butoane/alerte.
- [ ] Verificarea și adăugarea de indecși în baza de date pentru a optimiza interogările frecvente.
