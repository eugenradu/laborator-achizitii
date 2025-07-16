# Plan de Testare - Aplicație Achiziții

Acest document descrie pașii necesari pentru a testa funcționalitățile cheie ale aplicației. Fiecare secțiune corespunde unui modul principal.

## Partea 1: Pregătirea Mediului de Test

[ ] P-01: Rularea Aplicației: Asigură-te că aplicația rulează (local sau pe serverul de test).
[ ] P-02: Creare Utilizator: Asigură-te că ai un cont de utilizator și ești autentificat.
[ ] P-03: Date Inițiale: Asigură-te că există date de bază în sistem:

* Cel puțin 2-3 Categorii.
* Cel puțin 2-3 Producatori.
* Cel puțin 5-6 Produse generice, cu Variante Comerciale definite.
* Cel puțin 2 Furnizori.

## Partea 2: Modulul Referate (/referate)

### Secțiunea R: Creare și Management Referat (Starea CIORNĂ)

[ ] R-01: Creare Referat Nou:

1. Navighează la /referate.
2. Click pe "Adaugă Referat".
3. Completează toate câmpurile și salvează.
4. Așteptat: Referatul apare în listă, cu starea "Ciornă" și creatorul corect. Ești redirecționat la lista de referate.

[ ] R-02: Adăugare Produse în Referat:

1. Intră pe pagina de detalii a referatului creat la R-01.
2. În secțiunea "Adaugă Produs", selectează o categorie.
3. Așteptat: Dropdown-ul de produse se populează dinamic.
4. Selectează un produs, o cantitate și apasă "Adaugă Produs".
5. Așteptat: Produsul apare în lista de "Produse Solicitate". Repetă pentru a adăuga 2-3 produse.

[ ] R-03: Creare Loturi:

1. Pe aceeași pagină, în secțiunea "Creează Lot Nou", adaugă 2 loturi.
2. Așteptat: Ambele loturi apar în secțiunea "Loturi definite în Referat".

[ ] R-04: Alocare Produse în Loturi:

1. Sub primul lot, în secțiunea "Adaugă Produs la Acest Lot", selectează un produs din cele adăugate la R-02.
2. Click "Alocă Produs".
3. Așteptat: Produsul apare în tabelul lotului respectiv și dispare din lista de produse nealocate.
4. Repetă pentru a aloca toate produsele în loturi.

[ ] R-05: Management Produse și Loturi (în starea Ciornă):

1. Șterge un produs dintr-un lot: Dă click pe "Scoate din Lot" pentru un produs.
2. Așteptat: Produsul dispare din lot și reapare în lista de produse nealocate.
3. Șterge un produs din referat: Dă click pe "Șterge" pentru un produs din lista principală.
4. Așteptat: Produsul dispare complet.
5. Șterge un lot: Dă click pe "Șterge Lot" pentru un lot gol.
6. Așteptat: Lotul dispare.

[ ] R-06: Clonare Referat:

1. Pe pagina de detalii, click pe "Clonează Referat".
2. Așteptat: Ești redirecționat la un referat nou, cu starea "Ciornă", care conține aceleași produse ca originalul (dar fără alocare în loturi).

### Secțiunea RA: Fluxul de Aprobare Referat

[ ] RA-01: Validare Trimitere spre Aprobare (Eșec):

1. Asigură-te că un produs din referat nu este alocat niciunui lot.
2. Click pe "Trimite spre Aprobare".
3. Așteptat: Acțiunea eșuează și apare un mesaj de eroare care specifică faptul că toate produsele trebuie alocate.

[ ] RA-02: Trimitere spre Aprobare (Succes):

1. Alocă toate produsele în loturi.
2. Click pe "Trimite spre Aprobare".
3. Așteptat: Starea referatului devine "În Aprobare". Butoanele de editare (adăugare/ștergere produse/loturi) dispar. Apare secțiunea "Procesare Aprobare".

[ ] RA-03: Respingere Referat:

1. În secțiunea "Procesare Aprobare", lasă câmpul de observații gol și apasă "Respinge".
2. Așteptat: Acțiunea eșuează, cu un mesaj care cere completarea observațiilor.
3. Completează observațiile și apasă "Respinge".
4. Așteptat: Starea referatului revine la "Ciornă". Butoanele de editare reapar. Motivul respingerii este afișat vizibil pe pagină.

[ ] RA-04: Aprobare Referat:

1. Trimite din nou referatul spre aprobare (pasul RA-02).
2. În secțiunea "Procesare Aprobare", apasă "Aprobă".
3. Așteptat: Starea referatului devine "Aprobat". Secțiunea de aprobare dispare.

## Partea 3: Modulul Proceduri (/proceduri)

[ ] P-01: Creare Procedură Nouă:

1. Navighează la /proceduri.
2. Click "Adaugă Procedură", completează detaliile și salvează.
3. Așteptat: Ești redirecționat la pagina de detalii a noii proceduri.

[ ] P-02: Verificare Produse Disponibile:

1. Pe pagina de detalii a procedurii, în secțiunea "Produse Disponibile pentru Alocare", verifică lista.
2. Așteptat: Lista conține produsele din referatul aprobat la pasul RA-04.

[ ] P-03: Management Super-Loturi:

1. Creează un "Super-Lot" nou folosind formularul din stânga.
2. Așteptat: Lotul apare în lista de "Loturi în Procedură" și în dropdown-ul "Selectează lotul destinație".
3. În lista de produse disponibile, bifează câteva produse, selectează lotul destinație și apasă "Adaugă Produsele Selectate".
4. Așteptat: Produsele selectate apar în cardul Super-Lotului și dispar din lista de produse disponibile.
5. În cardul Super-Lotului, apasă X pentru a scoate un produs.
6. Așteptat: Produsul dispare din Super-Lot și reapare în lista de produse disponibile.

## Partea 4: Modulul Oferte (/oferte)

### Secțiunea O: Creare și Management Oferte

[ ] O-01: Adăugare Ofertă din Context Referat:

1. Navighează la un referat (stare Ciornă sau Aprobat).
2. Click pe "Adaugă Ofertă".
3. Așteptat: Ești pe pagina de adăugare ofertă, iar formularul conține produsele din acel referat.
4. Completează o ofertă parțială (doar pentru 1 din 2 produse) și salvează.
5. Așteptat: Ești redirecționat la pagina referatului. Noua ofertă apare în listă. Pe pagina de detalii a ofertei, apare doar articolul completat.

[ ] O-02: Adăugare Ofertă din Context Procedură:

1. Navighează la procedura creată la P-01.
2. Click "Adaugă Ofertă pentru Această Procedură".
3. Așteptat: Formularul de ofertă este structurat pe Super-Loturile definite.
4. Completează și salvează oferta.
5. Așteptat: Ești redirecționat la pagina procedurii. Noua ofertă apare în tabelul de analiză comparativă al lotului respectiv.

[ ] O-03: Editare Ofertă:

1. Navighează la lista de oferte (/oferte).
2. Click "Editează" pe oferta creată la O-01.
3. Schimbă un preț și adaugă preț/variantă pentru al doilea produs (care era gol). Salvează.
4. Așteptat: Ești redirecționat la detalii ofertă, iar ambele modificări sunt vizibile.
5. Editează din nou. Șterge prețul și deselectează varianta pentru un articol. Salvează.
6. Așteptat: Articolul respectiv a fost șters din ofertă.

[ ] O-04: Ștergere Ofertă și Redirecționare:

1. Mergi la detalii ofertă (cea creată din referat) și apasă "Șterge Oferta".
2. Așteptat: Ești redirecționat la pagina de detalii a referatului de la care ai creat-o.
3. Repetă pentru o ofertă creată din procedură.
4. Așteptat: Ești redirecționat la pagina de detalii a procedurii.

## Partea 5: Testarea Fluxului Complet (End-to-End)

[ ] F-01: Generare Contract:

1. Navighează la pagina de detalii a procedurii (P-01) care are o ofertă (O-02).
2. În tabelul de analiză, pentru un lot, click pe "Generează Contract" pentru oferta respectivă.
3. Așteptat: Ești pe formularul de creare contract, cu datele pre-completate din ofertă și procedură.
4. Completează restul detaliilor (tip: CONTRACT_FERM) și salvează.
5. Așteptat: Contractul este creat cu succes.

[ ] F-02: Verificare Comandă Automată:

1. Navighează la lista de comenzi (/comenzi).
2. Așteptat: O nouă comandă a fost generată automat pentru contractul ferm de la F-01.

[ ] F-03: Înregistrare Livrare:

1. Navighează la detaliile comenzii de la F-02.
2. Click "Adaugă Livrare".
3. Completează formularul de livrare, inclusiv Număr Lot Producător și Data Expirare pentru fiecare articol.
4. Așteptat: Livrarea este înregistrată cu succes, iar starea comenzii se actualizează (ex: Livrata Complet).
