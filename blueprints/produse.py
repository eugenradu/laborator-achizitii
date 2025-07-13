from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required
from sqlalchemy import or_
import json
from models import db, Produs, Categorie, Producator, VariantaComercialaProdus

produse_bp = Blueprint('produse', __name__)

# --- Secțiunea Produse Generice ---
@produse_bp.route('/produse')
@login_required
def produse():
    search_term = request.args.get('search', '').strip()
    category_filter_id = request.args.get('category_filter', type=int)
    page = request.args.get('page', 1, type=int)
    PER_PAGE = 15 # Poți ajusta numărul de produse pe pagină
    
    # Preluăm toate categoriile pentru a popula filtrul
    categorii_list = Categorie.query.order_by(Categorie.Nume_Categorie).all()

    # Start the base query
    query = db.session.query(Produs, Categorie).join(Categorie)

    if search_term:
        # Apply filter if a search term is provided
        search_filter = or_(
            Produs.Nume_Generic.ilike(f'%{search_term}%'),
            Produs.Specificatii_Tehnice.ilike(f'%{search_term}%')
        )
        query = query.filter(search_filter)

    # Aplicăm filtrul de categorie dacă este selectat
    if category_filter_id:
        query = query.filter(Produs.ID_Categorie == category_filter_id)

    # Apply ordering before pagination
    pagination = query.order_by(Categorie.Nume_Categorie, Produs.Nume_Generic).paginate(page=page, per_page=PER_PAGE, error_out=False)
    produse_list = pagination.items # The items for the current page

    return render_template('produse.html', 
                           produse=produse_list, pagination=pagination, 
                           search_term=search_term, categorii=categorii_list, 
                           category_filter_id=category_filter_id)

@produse_bp.route('/produse/adauga', methods=('GET', 'POST'))
@login_required
def adauga_produs():
    categorii_list = Categorie.query.order_by(Categorie.Nume_Categorie).all()
    if request.method == 'POST':
        nume_generic = request.form['nume_generic']
        specificatii = request.form['specificatii']
        unitate_masura = request.form['unitate_masura']
        id_categorie = request.form['id_categorie']

        new_produs = Produs(Nume_Generic=nume_generic, Specificatii_Tehnice=specificatii, Unitate_Masura=unitate_masura, ID_Categorie=id_categorie)
        db.session.add(new_produs)
        db.session.commit()
        flash('Produsul generic a fost adăugat cu succes!', 'success')
        return redirect(url_for('produse.produse'))
    return render_template('adauga_produs.html', categorii=categorii_list)

@produse_bp.route('/produse/edit/<int:produs_id>', methods=['GET', 'POST'])
@login_required
def edit_produs(produs_id):
    produs = Produs.query.get_or_404(produs_id)
    categorii_list = Categorie.query.order_by(Categorie.Nume_Categorie).all()

    if request.method == 'POST':
        produs.Nume_Generic = request.form['nume_generic']
        produs.Specificatii_Tehnice = request.form['specificatii']
        produs.Unitate_Masura = request.form['unitate_masura']
        produs.ID_Categorie = request.form['id_categorie']
        
        db.session.commit()
        flash('Produsul a fost actualizat cu succes!', 'success')
        return redirect(url_for('produse.produse'))

    # Pentru metoda GET, afișăm formularul pre-completat
    return render_template('edit_produs.html', produs=produs, categorii=categorii_list)

@produse_bp.route('/produse/sterge/<int:produs_id>', methods=['POST'])
@login_required
def sterge_produs(produs_id):
    produs = Produs.query.get_or_404(produs_id)

    # Verificare de siguranță: nu ștergem produse cu dependențe
    if produs.variante_comerciale or produs.produse_in_referate:
        flash(f'Produsul "{produs.Nume_Generic}" nu poate fi șters deoarece are variante comerciale asociate sau este inclus în referate de necesitate.', 'danger')
        return redirect(url_for('produse.produse'))

    try:
        db.session.delete(produs)
        db.session.commit()
        flash(f'Produsul "{produs.Nume_Generic}" a fost șters cu succes.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'A apărut o eroare la ștergerea produsului: {str(e)}', 'danger')
    return redirect(url_for('produse.produse'))

def _proceseaza_import_produse(data):
    """Funcție ajutătoare pentru a procesa importul efectiv al produselor dintr-o listă de dicționare."""
    added_count = 0
    updated_count = 0

    # Creăm un map pentru a evita interogări repetate în buclă
    categorii_map = {cat.Nume_Categorie: cat.ID_Categorie for cat in Categorie.query.all()}
    
    # Asigură existența categoriei "Necategorizat"
    default_category_name = "Necategorizat"
    if default_category_name not in categorii_map:
        new_default_category = Categorie(Nume_Categorie=default_category_name)
        db.session.add(new_default_category)
        db.session.flush() # Obținem ID-ul
        categorii_map[default_category_name] = new_default_category.ID_Categorie
    
    default_category_id = categorii_map[default_category_name]

    for item in data:
        nume_generic = item.get('Nume_Generic')
        specificatii = item.get('Specificatii_Tehnice')
        unitate_masura = item.get('Unitate_Masura')

        if not all([nume_generic, specificatii, unitate_masura]):
            flash(f'Intrarea "{nume_generic or "N/A"}" a fost omisă deoarece îi lipsesc câmpuri obligatorii.', 'warning')
            continue

        categorie_nume = item.get('Categorie', '').strip()
        categorie_id_to_assign = categorii_map.get(categorie_nume, default_category_id)

        produs_existent = Produs.query.filter_by(Nume_Generic=nume_generic).first()
        if produs_existent:
            produs_existent.Specificatii_Tehnice = specificatii
            produs_existent.Unitate_Masura = unitate_masura
            produs_existent.ID_Categorie = categorie_id_to_assign
            updated_count += 1
        else:
            new_produs = Produs(Nume_Generic=nume_generic, Specificatii_Tehnice=specificatii, Unitate_Masura=unitate_masura, ID_Categorie=categorie_id_to_assign)
            db.session.add(new_produs)
            added_count += 1

    db.session.commit()
    return added_count, updated_count


@produse_bp.route('/import-json', methods=['POST'])
@login_required
def import_produse_json():
    if 'fisier_json' not in request.files:
        flash('Niciun fișier selectat.', 'danger')
        return redirect(url_for('produse.produse'))

    file = request.files['fisier_json']

    if file.filename == '':
        flash('Niciun fișier selectat.', 'danger')
        return redirect(url_for('produse.produse'))

    if file and file.filename.endswith('.json'):
        try:
            content = file.read().decode('utf-8')
            data = json.loads(content)

            if not isinstance(data, list):
                flash('Fișierul JSON trebuie să conțină o listă de obiecte.', 'danger')
                return redirect(url_for('produse.produse'))
            
            # --- NOUA LOGICĂ: Detectare categorii noi ---
            categorii_din_json = {item.get('Categorie', '').strip() for item in data if item.get('Categorie', '').strip()}
            
            if categorii_din_json:
                categorii_existente_db = Categorie.query.with_entities(Categorie.Nume_Categorie).all()
                categorii_existente = {cat[0] for cat in categorii_existente_db}
                categorii_noi_de_creat = list(categorii_din_json - categorii_existente)

                if categorii_noi_de_creat:
                    session['import_data'] = data
                    session['categorii_noi'] = categorii_noi_de_creat
                    flash('Am detectat categorii noi. Vă rugăm confirmați crearea lor pentru a continua importul.', 'info')
                    return redirect(url_for('produse.confirm_import'))

            # Dacă nu sunt categorii noi, procesăm direct folosind funcția ajutătoare
            added_count, updated_count = _proceseaza_import_produse(data)
            flash(f'Import finalizat cu succes! Produse noi: {added_count}, Produse actualizate: {updated_count}.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'A apărut o eroare la procesarea fișierului: {str(e)}', 'danger')
    else:
        flash('Format de fișier invalid. Vă rugăm încărcați un fișier .json.', 'danger')
    
    return redirect(url_for('produse.produse'))

@produse_bp.route('/import-json/confirm', methods=['GET', 'POST'])
@login_required
def confirm_import():
    if 'import_data' not in session or 'categorii_noi' not in session:
        flash('Nu există date de import în sesiune. Vă rugăm reîncercați.', 'warning')
        return redirect(url_for('produse.produse'))

    if request.method == 'POST':
        if 'cancel' in request.form:
            session.pop('import_data', None)
            session.pop('categorii_noi', None)
            flash('Importul a fost anulat.', 'info')
            return redirect(url_for('produse.produse'))

        # --- Creare categorii noi ---
        categorii_noi = session.get('categorii_noi', [])
        for nume_cat in categorii_noi:
            new_cat = Categorie(Nume_Categorie=nume_cat)
            db.session.add(new_cat)
        db.session.commit()
        flash(f'Au fost create {len(categorii_noi)} categorii noi.', 'success')

        # --- Procesare import ---
        data = session.get('import_data')
        added_count, updated_count = _proceseaza_import_produse(data)
        flash(f'Import finalizat cu succes! Produse noi: {added_count}, Produse actualizate: {updated_count}.', 'success')
        
        # --- Curățare sesiune ---
        session.pop('import_data', None)
        session.pop('categorii_noi', None)

        return redirect(url_for('produse.produse'))

    # --- GET: Afișare pagină de confirmare ---
    categorii_noi = session.get('categorii_noi')
    return render_template('confirm_import.html', categorii_noi=categorii_noi)

# --- Secțiunea Categorii de Produse ---
@produse_bp.route('/categorii', methods=['GET', 'POST'])
@login_required
def categorii():
    if request.method == 'POST': # Gestionează formularul de adăugare
        nume_categorie = request.form.get('nume_categorie', '').strip()
        if not nume_categorie:
            flash('Numele categoriei nu poate fi gol.', 'danger')
        else:
            existing_category = Categorie.query.filter_by(Nume_Categorie=nume_categorie).first()
            if existing_category:
                flash(f'Categoria "{nume_categorie}" există deja.', 'danger')
            else:
                new_category = Categorie(Nume_Categorie=nume_categorie)
                db.session.add(new_category)
                db.session.commit()
                flash(f'Categoria "{nume_categorie}" a fost adăugată cu succes.', 'success')
        return redirect(url_for('produse.categorii'))

    # Pentru metoda GET, afișăm lista
    categorii_list = Categorie.query.order_by(Categorie.Nume_Categorie).all()
    return render_template('categorii.html', categorii=categorii_list)

@produse_bp.route('/categorii/modifica/<int:categorie_id>', methods=['POST'])
@login_required
def modifica_categorie(categorie_id):
    categorie = Categorie.query.get_or_404(categorie_id)
    nume_nou = request.form.get('nume_categorie_nou', '').strip()
    if not nume_nou:
        flash('Noul nume al categoriei nu poate fi gol.', 'danger')
    elif nume_nou != categorie.Nume_Categorie:
        existing_category = Categorie.query.filter_by(Nume_Categorie=nume_nou).first()
        if existing_category:
            flash(f'Categoria "{nume_nou}" există deja.', 'danger')
        else:
            categorie.Nume_Categorie = nume_nou
            db.session.commit()
            flash('Categoria a fost redenumită cu succes.', 'success')
    return redirect(url_for('produse.categorii'))

@produse_bp.route('/categorii/sterge/<int:categorie_id>', methods=['POST'])
@login_required
def sterge_categorie(categorie_id):
    categorie = Categorie.query.get_or_404(categorie_id)
    if categorie.produse:
        flash(f'Nu puteți șterge categoria "{categorie.Nume_Categorie}" deoarece are produse asociate.', 'danger')
    else:
        db.session.delete(categorie)
        db.session.commit()
        flash(f'Categoria "{categorie.Nume_Categorie}" a fost ștearsă.', 'success')
    return redirect(url_for('produse.categorii'))

# --- Secțiunea Producători ---
@produse_bp.route('/producatori', methods=['GET', 'POST'])
@login_required
def producatori():
    if request.method == 'POST':
        nume_producator = request.form.get('nume_producator', '').strip()
        if not nume_producator:
            flash('Numele producătorului nu poate fi gol.', 'danger')
        else:
            existing_producer = Producator.query.filter_by(Nume_Producator=nume_producator).first()
            if existing_producer:
                flash(f'Producătorul "{nume_producator}" există deja.', 'danger')
            else:
                new_producer = Producator(Nume_Producator=nume_producator)
                db.session.add(new_producer)
                db.session.commit()
                flash(f'Producătorul "{nume_producator}" a fost adăugat cu succes.', 'success')
        return redirect(url_for('produse.producatori'))

    # GET
    producatori_list = Producator.query.order_by(Producator.Nume_Producator).all()
    return render_template('producatori.html', producatori=producatori_list)

@produse_bp.route('/producatori/modifica/<int:producator_id>', methods=['POST'])
@login_required
def modifica_producator(producator_id):
    producator = Producator.query.get_or_404(producator_id)
    nume_nou = request.form.get('nume_producator_nou', '').strip()
    if not nume_nou:
        flash('Noul nume al producătorului nu poate fi gol.', 'danger')
    elif nume_nou != producator.Nume_Producator:
        existing_producer = Producator.query.filter_by(Nume_Producator=nume_nou).first()
        if existing_producer:
            flash(f'Producătorul "{nume_nou}" există deja.', 'danger')
        else:
            producator.Nume_Producator = nume_nou
            db.session.commit()
            flash('Producătorul a fost redenumit cu succes.', 'success')
    return redirect(url_for('produse.producatori'))

@produse_bp.route('/producatori/sterge/<int:producator_id>', methods=['POST'])
@login_required
def sterge_producator(producator_id):
    producator = Producator.query.get_or_404(producator_id)
    if producator.variante_comerciale:
        flash(f'Nu puteți șterge producătorul "{producator.Nume_Producator}" deoarece are variante comerciale asociate.', 'danger')
    else:
        db.session.delete(producator)
        db.session.commit()
        flash(f'Producătorul "{producator.Nume_Producator}" a fost șters.', 'success')
    return redirect(url_for('produse.producatori'))

# --- Secțiunea Variante Comerciale Produs ---
@produse_bp.route('/variante_comerciale')
@login_required
def variante_comerciale():
    search_term = request.args.get('search', '').strip()
    category_filter_id = request.args.get('category_filter', type=int)
    product_filter_id = request.args.get('product_filter', type=int)
    page = request.args.get('page', 1, type=int)
    PER_PAGE = 15

    # Preluăm categoriile pentru a popula filtrul
    categorii_list = Categorie.query.order_by(Categorie.Nume_Categorie).all()

    # Interogare de bază
    query = db.session.query(VariantaComercialaProdus, Produs, Categorie, Producator)\
        .join(Produs, VariantaComercialaProdus.ID_Produs_Generic == Produs.ID_Produs)\
        .join(Categorie, Produs.ID_Categorie == Categorie.ID_Categorie)\
        .join(Producator, VariantaComercialaProdus.ID_Producator == Producator.ID_Producator)

    # Aplicăm filtrele
    if search_term:
        search_filter = or_(
            VariantaComercialaProdus.Cod_Catalog.ilike(f'%{search_term}%'),
            VariantaComercialaProdus.Nume_Comercial_Extins.ilike(f'%{search_term}%'),
            VariantaComercialaProdus.Descriere_Ambalare.ilike(f'%{search_term}%'),
            Producator.Nume_Producator.ilike(f'%{search_term}%')
        )
        query = query.filter(search_filter)
    
    if category_filter_id:
        query = query.filter(Categorie.ID_Categorie == category_filter_id)
    
    if product_filter_id:
        query = query.filter(Produs.ID_Produs == product_filter_id)

    # Paginare
    pagination = query.order_by(Produs.Nume_Generic, VariantaComercialaProdus.Cod_Catalog).paginate(page=page, per_page=PER_PAGE, error_out=False)
    variante_list = pagination.items

    return render_template('variante_comerciale.html', variante=variante_list, pagination=pagination, categorii=categorii_list, search_term=search_term, category_filter_id=category_filter_id, product_filter_id=product_filter_id)

@produse_bp.route('/variante_comerciale/adauga', methods=['GET', 'POST'])
@login_required
def adauga_varianta_comerciala():
    if request.method == 'POST':
        id_produs_generic = request.form.get('id_produs_generic')
        id_producator = request.form.get('id_producator')
        cod_catalog = request.form.get('cod_catalog')
        nume_comercial_extins = request.form.get('nume_comercial_extins')
        descriere_ambalare = request.form.get('descriere_ambalare')
        cantitate_standard_ambalare = request.form.get('cantitate_standard_ambalare')

        if not all([id_produs_generic, id_producator, cod_catalog, descriere_ambalare, cantitate_standard_ambalare]):
            flash('Toate câmpurile, cu excepția numelui comercial extins, sunt obligatorii.', 'danger')
        else:
            existing_variant = VariantaComercialaProdus.query.filter_by(Cod_Catalog=cod_catalog).first()
            if existing_variant:
                flash(f'Codul de catalog "{cod_catalog}" există deja.', 'danger')
            else:
                new_varianta = VariantaComercialaProdus(
                    ID_Produs_Generic=id_produs_generic,
                    ID_Producator=id_producator,
                    Cod_Catalog=cod_catalog,
                    Nume_Comercial_Extins=nume_comercial_extins,
                    Descriere_Ambalare=descriere_ambalare,
                    Cantitate_Standard_Ambalare=cantitate_standard_ambalare
                )
                db.session.add(new_varianta)
                db.session.commit()
                flash('Varianta comercială a fost adăugată cu succes!', 'success')
                return redirect(url_for('produse.variante_comerciale'))
    
    # GET request
    categorii = Categorie.query.order_by(Categorie.Nume_Categorie).all()
    producatori = Producator.query.order_by(Producator.Nume_Producator).all()
    return render_template('adauga_varianta_comerciala.html', categorii=categorii, producatori=producatori)

@produse_bp.route('/variante_comerciale/edit/<int:varianta_id>', methods=['GET', 'POST'])
@login_required
def edit_varianta_comerciala(varianta_id):
    varianta = VariantaComercialaProdus.query.get_or_404(varianta_id)
    producatori = Producator.query.order_by(Producator.Nume_Producator).all()
    
    if request.method == 'POST':
        # Verificăm unicitatea noului cod de catalog, dacă a fost schimbat
        new_cod_catalog = request.form.get('cod_catalog')
        if new_cod_catalog != varianta.Cod_Catalog:
            existing_variant = VariantaComercialaProdus.query.filter_by(Cod_Catalog=new_cod_catalog).first()
            if existing_variant:
                flash(f'Codul de catalog "{new_cod_catalog}" există deja.', 'danger')
                return render_template('edit_varianta_comerciala.html', varianta=varianta, producatori=producatori)

        varianta.Cod_Catalog = new_cod_catalog
        varianta.ID_Producator = request.form.get('id_producator')
        varianta.Nume_Comercial_Extins = request.form.get('nume_comercial_extins')
        varianta.Descriere_Ambalare = request.form.get('descriere_ambalare')
        varianta.Cantitate_Standard_Ambalare = request.form.get('cantitate_standard_ambalare')
        
        db.session.commit()
        flash('Varianta comercială a fost actualizată cu succes!', 'success')
        return redirect(url_for('produse.variante_comerciale'))

    return render_template('edit_varianta_comerciala.html', varianta=varianta, producatori=producatori)

@produse_bp.route('/variante_comerciale/sterge/<int:varianta_id>', methods=['POST'])
@login_required
def sterge_varianta_comerciala(varianta_id):
    varianta = VariantaComercialaProdus.query.get_or_404(varianta_id)

    # Verificare de siguranță: nu ștergem variante cu dependențe
    if varianta.articole_oferta or varianta.articole_contractate or varianta.loturi_stoc:
        flash(f'Varianta comercială "{varianta.Cod_Catalog}" nu poate fi ștearsă deoarece este utilizată în oferte, contracte sau stocuri.', 'danger')
        return redirect(url_for('produse.variante_comerciale'))

    try:
        db.session.delete(varianta)
        db.session.commit()
        flash(f'Varianta comercială "{varianta.Cod_Catalog}" a fost ștearsă cu succes.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'A apărut o eroare la ștergerea variantei comerciale: {str(e)}', 'danger')
    
    return redirect(url_for('produse.variante_comerciale'))