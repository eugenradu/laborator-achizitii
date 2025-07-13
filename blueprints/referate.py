from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from datetime import date
from models import (
    db, Utilizator, Categorie, Producator, Produs, VariantaComercialaProdus, ReferatNecesitate,
    Lot, ProdusInReferat, ProdusInLot, Oferta
)

referate_bp = Blueprint('referate', __name__)

# --- Secțiunea Referate de Necesitate ---
@referate_bp.route('/referate')
@login_required
def referate():
    # Pentru a afișa și numele creatorului
    referate_list = db.session.query(ReferatNecesitate, Utilizator)\
                            .outerjoin(Utilizator, ReferatNecesitate.ID_Utilizator_Creare == Utilizator.ID_Utilizator)\
                            .order_by(ReferatNecesitate.Data_Creare.desc())\
                            .all()
    return render_template('referate.html', referate=referate_list)

@referate_bp.route('/referate/adauga', methods=('GET', 'POST'))
@login_required
def adauga_referat():
    if request.method == 'POST':
        numar_referat = request.form['numar_referat']
        data_creare = request.form['data_creare']
        stare = request.form['stare']
        numar_inregistrare_doc = request.form.get('numar_inregistrare_doc')
        data_inregistrare_doc = request.form.get('data_inregistrare_doc')
        link_scan_pdf = request.form.get('link_scan_pdf')
        observatii = request.form.get('observatii')

        new_referat = ReferatNecesitate(
            Numar_Referat=numar_referat,
            Data_Creare=date.fromisoformat(data_creare),
            Stare=stare,
            Numar_Inregistrare_Document=numar_inregistrare_doc,
            Data_Inregistrare_Document=date.fromisoformat(data_inregistrare_doc) if data_inregistrare_doc else None,
            Link_Scan_PDF=link_scan_pdf,
            ID_Utilizator_Creare=current_user.ID_Utilizator, # Setează utilizatorul curent
            Observatii=observatii
        )
        db.session.add(new_referat)
        db.session.commit()
        flash('Referatul de necesitate a fost creat cu succes!', 'success')
        return redirect(url_for('referate.referate'))
    return render_template('adauga_referat.html', today=date.today().isoformat())

@referate_bp.route('/referate/<int:referat_id>')
@login_required
def detalii_referat(referat_id):
    referat = ReferatNecesitate.query.get_or_404(referat_id)
    
    produse_in_referat_objects = db.session.query(ProdusInReferat, Produs)\
                                .select_from(ProdusInReferat) \
                                .join(Produs, ProdusInReferat.ID_Produs_Generic == Produs.ID_Produs)\
                                .filter(ProdusInReferat.ID_Referat == referat.ID_Referat)\
                                .all()
    
    loturi_referat = Lot.query.filter_by(ID_Referat=referat_id).all()

    produse_in_loturi = {}
    for lot in loturi_referat:
        produse_in_loturi[lot.ID_Lot] = db.session.query(ProdusInLot, ProdusInReferat, Produs) \
                                        .select_from(ProdusInLot) \
                                        .join(ProdusInReferat, ProdusInLot.ID_Produs_Referat == ProdusInReferat.ID_Produs_Referat) \
                                        .join(Produs, ProdusInReferat.ID_Produs_Generic == Produs.ID_Produs) \
                                        .filter(ProdusInLot.ID_Lot == lot.ID_Lot) \
                                        .all()
    categorii_disponibile = Categorie.query.order_by(Categorie.Nume_Categorie).all()

    produse_alocate_ids = {pil.ID_Produs_Referat for lot_id, prods_data in produse_in_loturi.items() for pil, _, _ in prods_data}
    produse_nealocate = []
    for pir, prod in produse_in_referat_objects:
        if pir.ID_Produs_Referat not in produse_alocate_ids:
            produse_nealocate.append((pir, prod))

    # Preluăm ofertele noi, flexibile, asociate cu acest referat
    oferte_asociate = referat.oferte

    return render_template('detalii_referat.html', 
                        referat=referat, 
                        produse_in_referat=produse_in_referat_objects,
                        loturi_referat=loturi_referat,
                        produse_in_loturi=produse_in_loturi,
                        categorii_disponibile=categorii_disponibile,
                        produse_nealocate=produse_nealocate,
                        oferte_asociate=oferte_asociate)

@referate_bp.route('/referate/<int:referat_id>/adauga_produs_referat', methods=['POST'])
@login_required
def adauga_produs_referat(referat_id):
    referat = ReferatNecesitate.query.get_or_404(referat_id) 
    produs_id_generic = request.form['id_produs_generic']
    cantitate = request.form['cantitate_solicitata']

    new_prod_in_ref = ProdusInReferat(
        ID_Referat=referat.ID_Referat, 
        ID_Produs_Generic=produs_id_generic,
        Cantitate_Solicitata=cantitate
    )
    db.session.add(new_prod_in_ref)
    db.session.commit()
    flash('Produsul a fost adăugat în referat!', 'success')
    return redirect(url_for('referate.detalii_referat', referat_id=referat.ID_Referat))

@referate_bp.route('/referate/<int:referat_id>/adauga_lot', methods=['POST'])
@login_required
def adauga_lot_referat(referat_id):
    referat = ReferatNecesitate.query.get_or_404(referat_id)
    nume_lot = request.form['nume_lot']
    descriere_lot = request.form['descriere_lot']

    new_lot = Lot(
        ID_Referat=referat.ID_Referat,
        Nume_Lot=nume_lot,
        Descriere_Lot=descriere_lot
    )
    db.session.add(new_lot)
    db.session.commit()
    flash(f'Lotul "{nume_lot}" a fost creat cu succes!', 'success')
    return redirect(url_for('referate.detalii_referat', referat_id=referat.ID_Referat))

@referate_bp.route('/referate/<int:referat_id>/aloca_produs_lot/<int:lot_id>', methods=['POST'])
@login_required
def aloca_produs_lot(referat_id, lot_id):
    id_produs_referat = request.form['id_produs_referat_alloc']

    loturi_in_acest_referat = Lot.query.filter_by(ID_Referat=referat_id).all()
    lot_ids_in_referat = [lot.ID_Lot for lot in loturi_in_acest_referat]

    existing_allocation_in_referat = ProdusInLot.query.filter(
        ProdusInLot.ID_Produs_Referat == id_produs_referat,
        ProdusInLot.ID_Lot.in_(lot_ids_in_referat)
    ).first()

    if existing_allocation_in_referat:
        flash('Acest produs a fost deja alocat unui lot din acest referat!', 'danger')
    else:
        new_prod_in_lot = ProdusInLot(
            ID_Lot=lot_id,
            ID_Produs_Referat=id_produs_referat
        )
        db.session.add(new_prod_in_lot)
        db.session.commit()
        flash('Produsul a fost alocat lotului cu succes!', 'success')

    return redirect(url_for('referate.detalii_referat', referat_id=referat_id))

@referate_bp.route('/referate/<int:referat_id>/genereaza_referat')
@login_required
def genereaza_referat_doc(referat_id):
    """Generează un fișier .txt cu detaliile referatului de necesitate."""
    referat = ReferatNecesitate.query.get_or_404(referat_id)

    # Construim conținutul text al documentului
    referat_text = f"REFERAT DE NECESITATE\n"
    referat_text += f"{'='*40}\n"
    referat_text += f"Număr: {referat.Numar_Referat or 'N/A'}\n"
    referat_text += f"Data: {referat.Data_Creare.strftime('%d-%m-%Y')}\n"
    referat_text += f"Stare: {referat.Stare}\n"
    if referat.creator_referat:
        referat_text += f"Creat de: {referat.creator_referat.Nume_Utilizator}\n"
    referat_text += f"{'='*40}\n"

    # Preluăm loturile și produsele grupate pe lot
    loturi = Lot.query.filter_by(ID_Referat=referat_id).order_by(Lot.Nume_Lot).all()
    produse_alocate_ids = set()

    for lot in loturi:
        referat_text += f"\n--- LOT: {lot.Nume_Lot.upper()} ---\n"
        if lot.Descriere_Lot:
            referat_text += f"Descriere: {lot.Descriere_Lot}\n"
        referat_text += "\n"

        produse_in_lot = db.session.query(Produs, ProdusInReferat)\
            .join(ProdusInReferat, Produs.ID_Produs == ProdusInReferat.ID_Produs_Generic)\
            .join(ProdusInLot, ProdusInReferat.ID_Produs_Referat == ProdusInLot.ID_Produs_Referat)\
            .filter(ProdusInLot.ID_Lot == lot.ID_Lot)\
            .order_by(Produs.Nume_Generic).all()

        for i, (produs, pir) in enumerate(produse_in_lot):
            referat_text += f"{i+1}. {produs.Nume_Generic}\n"
            referat_text += f"   - Cantitate solicitată: {pir.Cantitate_Solicitata} {produs.Unitate_Masura}\n"
            referat_text += f"   - Specificații tehnice: {produs.Specificatii_Tehnice or 'N/A'}\n\n"
            produse_alocate_ids.add(pir.ID_Produs_Referat)

    # Preluăm produsele nealocate
    produse_nealocate = db.session.query(Produs, ProdusInReferat)\
        .join(ProdusInReferat, Produs.ID_Produs == ProdusInReferat.ID_Produs_Generic)\
        .filter(ProdusInReferat.ID_Referat == referat_id, ProdusInReferat.ID_Produs_Referat.notin_(produse_alocate_ids))\
        .order_by(Produs.Nume_Generic).all()

    if produse_nealocate:
        referat_text += f"\n--- PRODUSE NEALOCATE ---\n\n"
        for i, (produs, pir) in enumerate(produse_nealocate):
            referat_text += f"{i+1}. {produs.Nume_Generic}\n"
            referat_text += f"   - Cantitate solicitată: {pir.Cantitate_Solicitata} {produs.Unitate_Masura}\n"
            referat_text += f"   - Specificații tehnice: {produs.Specificatii_Tehnice or 'N/A'}\n\n"

    response = make_response(referat_text)
    response.headers["Content-Disposition"] = f"attachment; filename=referat_necesitate_{referat_id}.txt"
    response.headers["Content-type"] = "text/plain; charset=utf-8"
    return response

@referate_bp.route('/referate/<int:referat_id>/edit_observatii', methods=['POST'])
@login_required
def edit_observatii_referat(referat_id):
    """Actualizează câmpul de observații pentru un referat existent."""
    referat = ReferatNecesitate.query.get_or_404(referat_id)
    
    noi_observatii = request.form.get('observatii')
    referat.Observatii = noi_observatii
    db.session.commit()
    
    flash('Observațiile au fost actualizate cu succes!', 'success')
    return redirect(url_for('referate.detalii_referat', referat_id=referat.ID_Referat))