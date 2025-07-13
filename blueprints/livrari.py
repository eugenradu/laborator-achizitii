from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from models import (db, ComandaGeneral, DetaliiComandaProdus, LivrareComanda, DocumentLivrare, TipDocument,
                    ArticolContractat, VariantaComercialaProdus, Produs, Contract, Furnizor)

livrari_bp = Blueprint('livrari', __name__, url_prefix='/livrari')

@livrari_bp.route('/')
@login_required
def list_livrari():
    """Afișează lista tuturor livrărilor, cu căutare și paginare."""
    search_term = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    PER_PAGE = 20

    # Interogare de bază complexă pentru a aduna toate informațiile necesare
    query = db.session.query(
        LivrareComanda,
        Produs,
        ComandaGeneral,
        Furnizor
    ).join(DetaliiComandaProdus, LivrareComanda.ID_Detalii_Comanda_Produs == DetaliiComandaProdus.ID_Detalii_Comanda_Produs)\
     .join(ComandaGeneral, DetaliiComandaProdus.ID_Comanda_General == ComandaGeneral.ID_Comanda_General)\
     .join(Contract, ComandaGeneral.ID_Contract == Contract.ID_Contract)\
     .join(Furnizor, Contract.ID_Furnizor == Furnizor.ID_Furnizor)\
     .join(ArticolContractat, DetaliiComandaProdus.ID_Articol_Contractat == ArticolContractat.ID_Articol_Contractat)\
     .join(VariantaComercialaProdus, ArticolContractat.ID_Varianta_Comerciala == VariantaComercialaProdus.ID_Varianta_Comerciala)\
     .join(Produs, VariantaComercialaProdus.ID_Produs_Generic == Produs.ID_Produs)

    if search_term:
        search_filter = or_(
            LivrareComanda.Numar_Lot_Producator.ilike(f'%{search_term}%'),
            ComandaGeneral.Numar_Comanda.ilike(f'%{search_term}%'),
            Furnizor.Nume_Furnizor.ilike(f'%{search_term}%'),
            Produs.Nume_Generic.ilike(f'%{search_term}%')
        )
        query = query.filter(search_filter)

    pagination = query.order_by(LivrareComanda.Data_Livrare.desc(), LivrareComanda.ID_Livrare.desc()).paginate(page=page, per_page=PER_PAGE, error_out=False)

    return render_template('livrari.html', pagination=pagination, search_term=search_term)

@livrari_bp.route('/adauga/<int:comanda_id>', methods=['GET', 'POST'])
@login_required
def adauga_livrare(comanda_id):
    """Gestionează înregistrarea unei livrări pentru o comandă specifică."""
    comanda = ComandaGeneral.query.options(
        joinedload(ComandaGeneral.detalii_produse_comanda_rel).joinedload(DetaliiComandaProdus.articol_contractat_rel).joinedload('varianta_comerciala_contractata').joinedload('produs_generic'),
        joinedload(ComandaGeneral.detalii_produse_comanda_rel).joinedload(DetaliiComandaProdus.livrari_rel)
    ).get_or_404(comanda_id)

    # --- Logica POST (Salvarea formularului) ---
    if request.method == 'POST':
        try:
            prima_livrare_creata = None
            cel_putin_o_livrare = False

            # Iterăm prin fiecare linie de detaliu a comenzii pentru a prelua datele
            for detaliu in comanda.detalii_produse_comanda_rel:
                cantitate_livrata_str = request.form.get(f'cantitate_{detaliu.ID_Detalii_Comanda_Produs}')
                cantitate_livrata = int(cantitate_livrata_str) if cantitate_livrata_str else 0

                if cantitate_livrata > 0:
                    cel_putin_o_livrare = True
                    lot_producator = request.form.get(f'lot_producator_{detaliu.ID_Detalii_Comanda_Produs}')
                    data_expirare_str = request.form.get(f'data_expirare_{detaliu.ID_Detalii_Comanda_Produs}')
                    data_expirare = date.fromisoformat(data_expirare_str) if data_expirare_str else None

                    # Validare cantitate
                    total_deja_livrat = sum(liv.Cantitate_Livrata_Pachete for liv in detaliu.livrari_rel)
                    if cantitate_livrata > (detaliu.Cantitate_Comandata_Pachete - total_deja_livrat):
                        flash(f'Cantitatea livrată pentru produsul {detaliu.articol_contractat_rel.varianta_comerciala_contractata.produs_generic.Nume_Generic} depășește cantitatea rămasă de livrat.', 'danger')
                        raise Exception("Validation Error")

                    new_livrare = LivrareComanda(
                        ID_Detalii_Comanda_Produs=detaliu.ID_Detalii_Comanda_Produs,
                        Cantitate_Livrata_Pachete=cantitate_livrata,
                        Data_Livrare=date.today(),
                        Numar_Lot_Producator=lot_producator,
                        Data_Expirare=data_expirare,
                        ID_Utilizator_Inregistrare=current_user.ID_Utilizator
                    )
                    db.session.add(new_livrare)

                    # Asociem documentele doar cu prima livrare creată în această tranzacție
                    if not prima_livrare_creata:
                        prima_livrare_creata = new_livrare

            if not cel_putin_o_livrare:
                flash('Nu a fost înregistrată nicio livrare. Introduceți o cantitate mai mare ca zero pentru cel puțin un articol.', 'warning')
                return redirect(url_for('livrari.adauga_livrare', comanda_id=comanda_id))

            # Procesăm documentele și le atașăm la prima livrare
            if prima_livrare_creata:
                tipuri_doc = request.form.getlist('tip_document')
                numere_doc = request.form.getlist('numar_document')
                date_doc = request.form.getlist('data_document')
                linkuri_doc = request.form.getlist('link_scan_pdf')

                for i in range(len(tipuri_doc)):
                    if tipuri_doc[i] and numere_doc[i]:
                        new_doc = DocumentLivrare(
                            livrare_parinte=prima_livrare_creata,
                            Tip_Document=TipDocument[tipuri_doc[i]],
                            Numar_Document=numere_doc[i],
                            Data_Document=date.fromisoformat(date_doc[i]) if date_doc[i] else None,
                            Link_Scan_PDF=linkuri_doc[i]
                        )
                        db.session.add(new_doc)

            # Actualizăm starea comenzii
            db.session.flush() # Asigurăm că noile livrări sunt luate în calcul
            total_comandat = sum(d.Cantitate_Comandata_Pachete for d in comanda.detalii_produse_comanda_rel)
            total_livrat_acum = sum(liv.Cantitate_Livrata_Pachete for d in comanda.detalii_produse_comanda_rel for liv in d.livrari_rel)
            
            if total_livrat_acum >= total_comandat:
                comanda.Stare_Comanda = "Livrata Complet"
            else:
                comanda.Stare_Comanda = "Livrata Partial"

            db.session.commit()
            flash('Livrarea a fost înregistrată cu succes!', 'success')
            return redirect(url_for('comenzi.detalii_comanda', comanda_id=comanda_id))

        except Exception as e:
            db.session.rollback()
            if str(e) != "Validation Error":
                flash(f'A apărut o eroare la salvarea livrării: {str(e)}', 'danger')
            return redirect(url_for('livrari.adauga_livrare', comanda_id=comanda_id))

    # --- Logica GET (Pregătirea formularului) ---
    articole_de_livrat = []
    for detaliu in comanda.detalii_produse_comanda_rel:
        total_deja_livrat = sum(liv.Cantitate_Livrata_Pachete for liv in detaliu.livrari_rel)
        cantitate_ramasa = detaliu.Cantitate_Comandata_Pachete - total_deja_livrat
        if cantitate_ramasa > 0:
            articole_de_livrat.append({
                'detaliu_comanda': detaliu,
                'articol_contractat': detaliu.articol_contractat_rel,
                'cantitate_ramasa': cantitate_ramasa
            })

    if not articole_de_livrat:
        flash('Toate articolele din această comandă au fost deja livrate integral.', 'info')
        return redirect(url_for('comenzi.detalii_comanda', comanda_id=comanda_id))

    return render_template('adauga_livrare.html', 
                        comanda=comanda, 
                        articole_de_livrat=articole_de_livrat,
                        tipuri_document=TipDocument)
