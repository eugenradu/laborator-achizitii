from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date
from sqlalchemy.orm import joinedload
from models import (
    db, Oferta, ArticolOferta, VariantaComercialaProdus, Produs, Producator, Licitatie, ReferatNecesitate, Furnizor
)

oferte_bp = Blueprint('oferte', __name__, url_prefix='/oferte')

# Ruta pentru a lista toate ofertele
@oferte_bp.route('/')
@login_required
def list_oferte():
    """Afișează o listă cu toate ofertele înregistrate."""
    oferte_list = Oferta.query.options(joinedload(Oferta.furnizor)).order_by(Oferta.Data_Oferta.desc()).all()
    return render_template('oferte.html', oferte=oferte_list)

# Ruta pentru a adăuga o nouă ofertă
@oferte_bp.route('/adauga', methods=['GET', 'POST'])
@login_required
def adauga_oferta():
    """Gestionează crearea unei noi oferte cu antet și articole multiple."""
    if request.method == 'POST':
        # --- 1. Preluare date pentru antetul ofertei (Oferta) ---
        id_furnizor = request.form.get('id_furnizor', type=int)
        data_oferta_str = request.form.get('data_oferta')
        numar_inregistrare = request.form.get('numar_inregistrare')
        data_inregistrare_str = request.form.get('data_inregistrare')
        moneda = request.form.get('moneda', 'RON')
        id_licitatie = request.form.get('id_licitatie')
        id_referat = request.form.get('id_referat')

        if not id_furnizor or not data_oferta_str:
            flash('Selectarea unui furnizor și data ofertei sunt obligatorii.', 'danger')
            return redirect(url_for('oferte.adauga_oferta'))

        # --- 2. Creare obiect Oferta ---
        new_oferta = Oferta(
            ID_Furnizor=id_furnizor,
            Data_Oferta=date.fromisoformat(data_oferta_str),
            Numar_Inregistrare=numar_inregistrare,
            Data_Inregistrare=date.fromisoformat(data_inregistrare_str) if data_inregistrare_str else None,
            Moneda=moneda,
            ID_Licitatie=int(id_licitatie) if id_licitatie else None,
            ID_Referat=int(id_referat) if id_referat else None,
        )
        db.session.add(new_oferta)
        
        # --- 3. Preluare date pentru articolele ofertei (ArticolOferta) ---
        variante_ids = request.form.getlist('id_varianta_comerciala[]')
        preturi = request.form.getlist('pret_unitar_pachet[]')
        observatii_list = request.form.getlist('observatii[]')

        # --- 4. Creare obiecte ArticolOferta ---
        for i in range(len(variante_ids)):
            if variante_ids[i] and preturi[i]: # Adaugă articolul doar dacă varianta și prețul sunt specificate
                new_articol = ArticolOferta(
                    oferta_parinte=new_oferta, # Legătura cu antetul
                    ID_Varianta_Comerciala=int(variante_ids[i]),
                    Pret_Unitar_Pachet=float(preturi[i]),
                    Observatii=observatii_list[i]
                )
                db.session.add(new_articol)

        db.session.commit()
        flash('Oferta a fost adăugată cu succes!', 'success')
        return redirect(url_for('oferte.list_oferte'))

    # --- GET: Pregătire date pentru formular ---
    variante_comerciale = VariantaComercialaProdus.query.join(Produs).join(Producator).order_by(Producator.Nume_Producator, Produs.Nume_Generic).all()
    licitatii = Licitatie.query.order_by(Licitatie.Nume_Licitatie.desc()).all()
    referate = ReferatNecesitate.query.order_by(ReferatNecesitate.ID_Referat.desc()).all()
    furnizori = Furnizor.query.order_by(Furnizor.Nume_Furnizor).all()
    producatori = Producator.query.order_by(Producator.Nume_Producator).all()
    produse_generice = Produs.query.order_by(Produs.Nume_Generic).all()
    referat_id_preselectat = request.args.get('referat_id', type=int)
    
    return render_template('adauga_oferta.html', 
                           variante_comerciale=variante_comerciale,
                           licitatii=licitatii,
                           referate=referate,
                           furnizori=furnizori,
                           producatori=producatori,
                           produse_generice=produse_generice,
                           today=date.today().isoformat(),
                           referat_id_preselectat=referat_id_preselectat)

# Ruta pentru a edita o ofertă existentă
@oferte_bp.route('/<int:oferta_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_oferta(oferta_id):
    """Gestionează editarea unei oferte existente."""
    oferta = Oferta.query.options(joinedload(Oferta.articole)).get_or_404(oferta_id)

    if request.method == 'POST':
        # --- 1. Actualizare date antet (Oferta) ---
        oferta.ID_Furnizor = request.form.get('id_furnizor', type=int)
        oferta.Data_Oferta = date.fromisoformat(request.form.get('data_oferta'))
        oferta.Numar_Inregistrare = request.form.get('numar_inregistrare')
        data_inregistrare_str = request.form.get('data_inregistrare')
        oferta.Data_Inregistrare = date.fromisoformat(data_inregistrare_str) if data_inregistrare_str else None
        oferta.Moneda = request.form.get('moneda', 'RON')
        id_licitatie = request.form.get('id_licitatie')
        oferta.ID_Licitatie = int(id_licitatie) if id_licitatie else None
        id_referat = request.form.get('id_referat')
        oferta.ID_Referat = int(id_referat) if id_referat else None

        if not oferta.ID_Furnizor:
            flash('Selectarea unui furnizor este obligatorie.', 'danger')

        # --- 2. Actualizare articole (șterge și re-adaugă) ---
        # Golim lista de articole existente. Datorită cascade, acestea vor fi șterse din DB la commit.
        oferta.articole = []

        # Preluare și creare articole noi
        variante_ids = request.form.getlist('id_varianta_comerciala[]')
        preturi = request.form.getlist('pret_unitar_pachet[]')
        observatii_list = request.form.getlist('observatii[]')

        for i in range(len(variante_ids)):
            if variante_ids[i] and preturi[i]:
                new_articol = ArticolOferta(
                    ID_Varianta_Comerciala=int(variante_ids[i]),
                    Pret_Unitar_Pachet=float(preturi[i]),
                    Observatii=observatii_list[i]
                )
                oferta.articole.append(new_articol)

        db.session.commit()
        flash('Oferta a fost actualizată cu succes!', 'success')
        return redirect(url_for('oferte.detalii_oferta', oferta_id=oferta.ID_Oferta))

    # --- GET: Pregătire date pentru formularul de editare ---
    variante_comerciale = VariantaComercialaProdus.query.join(Produs).join(Producator).order_by(Producator.Nume_Producator, Produs.Nume_Generic).all()
    licitatii = Licitatie.query.order_by(Licitatie.Nume_Licitatie.desc()).all()
    referate = ReferatNecesitate.query.order_by(ReferatNecesitate.ID_Referat.desc()).all()
    furnizori = Furnizor.query.order_by(Furnizor.Nume_Furnizor).all()
    producatori = Producator.query.order_by(Producator.Nume_Producator).all()
    produse_generice = Produs.query.order_by(Produs.Nume_Generic).all()

    return render_template('edit_oferta.html', oferta=oferta, 
                           variante_comerciale=variante_comerciale, 
                           licitatii=licitatii, referate=referate,
                           furnizori=furnizori,
                           producatori=producatori, produse_generice=produse_generice)

# Ruta pentru a șterge o ofertă
@oferte_bp.route('/<int:oferta_id>/sterge', methods=['POST'])
@login_required
def sterge_oferta(oferta_id):
    oferta = Oferta.query.get_or_404(oferta_id)
    db.session.delete(oferta)
    db.session.commit()
    flash(f'Oferta #{oferta_id} de la {oferta.furnizor.Nume_Furnizor} a fost ștearsă cu succes.', 'success')
    return redirect(url_for('oferte.list_oferte'))

# Ruta pentru a vedea detaliile unei oferte
@oferte_bp.route('/<int:oferta_id>/detalii')
@login_required
def detalii_oferta(oferta_id):
    """Afișează detaliile complete ale unei oferte, inclusiv articolele sale."""
    oferta = Oferta.query.options(
        joinedload(Oferta.furnizor),
        joinedload(Oferta.articole).joinedload(ArticolOferta.varianta_comerciala_ofertata).joinedload(VariantaComercialaProdus.produs_generic),
        joinedload(Oferta.articole).joinedload(ArticolOferta.varianta_comerciala_ofertata).joinedload(VariantaComercialaProdus.producator),
        joinedload(Oferta.licitatie_parinte),
        joinedload(Oferta.referat_asociat)
    ).get_or_404(oferta_id)
    
    return render_template('detalii_oferta.html', oferta=oferta)