from flask_sqlalchemy import SQLAlchemy
from datetime import date
import enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class StareReferat(enum.Enum):
    CIORNA = "Ciornă"
    IN_APROBARE = "În Aprobare"
    APROBAT = "Aprobat"

# 1. Model pentru Utilizatori
class Utilizator(db.Model, UserMixin):
    __tablename__ = 'Utilizatori'
    ID_Utilizator = db.Column(db.Integer, primary_key=True)
    Nume_Utilizator = db.Column(db.Text, unique=True, nullable=False)
    Email = db.Column(db.Text, unique=True, nullable=False)
    Parola_Hash = db.Column(db.Text, nullable=False)
    Data_Creare = db.Column(db.Date, nullable=False, default=date.today)
    Este_Activ = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relații inverse
    referate_create = db.relationship('ReferatNecesitate', backref='creator_referat', lazy=True)
    proceduri_create = db.relationship('ProceduraAchizitie', backref='creator_procedura', lazy=True)
    comenzi_create = db.relationship('ComandaGeneral', backref='creator_comanda', lazy=True)
    livrari_inregistrate = db.relationship('LivrareComanda', backref='inregistrator_livrare', lazy=True)
    
    def set_password(self, password):
        self.Parola_Hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Parola_Hash, password)

    def get_id(self):
        return str(self.ID_Utilizator)

    def is_active(self):
        return self.Este_Activ

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return f"<Utilizator {self.Nume_Utilizator}>"

# 2. Model pentru Categorii de Produse
class Categorie(db.Model):
    __tablename__ = 'Categorii'
    ID_Categorie = db.Column(db.Integer, primary_key=True)
    Nume_Categorie = db.Column(db.Text, unique=True, nullable=False)

    # Relație inversă pentru a accesa produsele dintr-o categorie
    produse = db.relationship('Produs', backref='categorie', lazy=True)

    def __repr__(self):
        return f"<Categorie {self.Nume_Categorie}>"

# 3. Model pentru Producători
class Producator(db.Model):
    __tablename__ = 'Producatori'
    ID_Producator = db.Column(db.Integer, primary_key=True)
    Nume_Producator = db.Column(db.Text, unique=True, nullable=False)
    variante_comerciale = db.relationship('VariantaComercialaProdus', backref='producator', lazy=True)

    def __repr__(self):
        return f"<Producator {self.Nume_Producator}>"

# Model nou pentru Furnizori/Distribuitori
class Furnizor(db.Model):
    __tablename__ = 'Furnizori'
    ID_Furnizor = db.Column(db.Integer, primary_key=True)
    Nume_Furnizor = db.Column(db.Text, unique=True, nullable=False)
    CUI = db.Column(db.Text, unique=True)
    Adresa = db.Column(db.Text)
    Persoana_Contact = db.Column(db.Text)
    Email_Contact = db.Column(db.Text)
    Telefon_Contact = db.Column(db.Text)

    # Relații inverse
    oferte = db.relationship('Oferta', backref='furnizor', lazy=True)
    contracte = db.relationship('Contract', backref='furnizor', lazy=True)

    def __repr__(self):
        return f"<Furnizor {self.Nume_Furnizor}>"

# 4. Model pentru Produse (Generic Products)
class Produs(db.Model):
    __tablename__ = 'Produse'
    ID_Produs = db.Column(db.Integer, primary_key=True)
    Nume_Generic = db.Column(db.Text, nullable=False)
    Specificatii_Tehnice = db.Column(db.Text)
    Unitate_Masura = db.Column(db.Text)
    ID_Categorie = db.Column(db.Integer, db.ForeignKey('Categorii.ID_Categorie'), nullable=False)

    # Relații
    variante_comerciale = db.relationship('VariantaComercialaProdus', backref='produs_generic', lazy=True)
    produse_in_referate = db.relationship('ProdusInReferat', backref='produs_generic_req', lazy=True)

    def __repr__(self):
        return f"<Produs {self.Nume_Generic}>"

# 5. Model pentru Variante_Comerciale_Produs (Commercial Product Variants / Catalog Items)
class VariantaComercialaProdus(db.Model):
    __tablename__ = 'Variante_Comerciale_Produs'
    ID_Varianta_Comerciala = db.Column(db.Integer, primary_key=True)
    ID_Produs_Generic = db.Column(db.Integer, db.ForeignKey('Produse.ID_Produs'), nullable=False)
    ID_Producator = db.Column(db.Integer, db.ForeignKey('Producatori.ID_Producator'), nullable=False)
    Cod_Catalog = db.Column(db.Text, unique=True, nullable=False)
    Nume_Comercial_Extins = db.Column(db.Text)
    Descriere_Ambalare = db.Column(db.Text, nullable=False)
    Cantitate_Standard_Ambalare = db.Column(db.Integer, nullable=False)

    # Relații
    articole_oferta = db.relationship('ArticolOferta', backref='varianta_comerciala_ofertata', lazy=True)
    articole_contractate = db.relationship('ArticolContractat', backref='varianta_comerciala_contractata', lazy=True)

    def __repr__(self):
        return f"<VariantaComercialaProdus {self.Cod_Catalog}>"


# 6. Model pentru Referate_Necesitate
class ReferatNecesitate(db.Model):
    __tablename__ = 'Referate_Necesitate'
    ID_Referat = db.Column(db.Integer, primary_key=True)
    Data_Creare = db.Column(db.Date, nullable=False, default=date.today)
    Stare = db.Column(db.Enum(StareReferat), nullable=False, default=StareReferat.CIORNA)
    Numar_Referat = db.Column(db.Text)
    Numar_Inregistrare_Document = db.Column(db.Text)
    Data_Inregistrare_Document = db.Column(db.Date)
    Link_Scan_PDF = db.Column(db.Text)
    ID_Utilizator_Creare = db.Column(db.Integer, db.ForeignKey('Utilizatori.ID_Utilizator')) # NULLABLE as per DATA_MODEL.md
    Observatii = db.Column(db.Text)
    Observatii_Aprobare = db.Column(db.Text, nullable=True)

    # Relații
    loturi = db.relationship('Lot', backref='referat_parinte', lazy=True, cascade="all, delete-orphan")
    produse_in_referate = db.relationship('ProdusInReferat', backref='referat_necesitate', lazy=True, cascade="all, delete-orphan")
    oferte = db.relationship('Oferta', backref='referat_asociat', lazy=True)

    def __repr__(self):
        return f"<ReferatNecesitate {self.Numar_Referat or self.ID_Referat}>"

# 7. Model pentru Loturi (Lots for Tenders)
class Lot(db.Model):
    __tablename__ = 'Loturi'
    ID_Lot = db.Column(db.Integer, primary_key=True)
    ID_Referat = db.Column(db.Integer, db.ForeignKey('Referate_Necesitate.ID_Referat'), nullable=False)
    Nume_Lot = db.Column(db.Text, nullable=False)
    Descriere_Lot = db.Column(db.Text)

    # Relații
    produse_in_loturi = db.relationship('ProdusInLot', backref='lot_parinte', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Lot {self.Nume_Lot}>"

# 8. Model pentru Produse_In_Referate (Products in Necessity Requests)
class ProdusInReferat(db.Model):
    __tablename__ = 'Produse_In_Referate'
    ID_Produs_Referat = db.Column(db.Integer, primary_key=True)
    ID_Referat = db.Column(db.Integer, db.ForeignKey('Referate_Necesitate.ID_Referat'), nullable=False)
    ID_Produs_Generic = db.Column(db.Integer, db.ForeignKey('Produse.ID_Produs'), nullable=False)
    Cantitate_Solicitata = db.Column(db.Integer, nullable=False)

    # Relații
    produse_in_loturi = db.relationship('ProdusInLot', backref='produs_referat_alloc', lazy=True, cascade="all, delete-orphan")
    articole_oferta = db.relationship('ArticolOferta', backref='produs_referat_ofertat', lazy=True)
    articole_contractate = db.relationship('ArticolContractat', backref='produs_referat_contractat', lazy=True)

    def __repr__(self):
        return f"<ProdusInReferat {self.ID_Produs_Referat} (Ref: {self.ID_Referat})>"

# 9. Model pentru Produse_In_Loturi (Products in Lots)
class ProdusInLot(db.Model):
    __tablename__ = 'Produse_In_Loturi'
    ID_Produs_Lot = db.Column(db.Integer, primary_key=True)
    ID_Lot = db.Column(db.Integer, db.ForeignKey('Loturi.ID_Lot'), nullable=False)
    ID_Produs_Referat = db.Column(db.Integer, db.ForeignKey('Produse_In_Referate.ID_Produs_Referat'), nullable=False)
    
    # Adaugăm o constrângere UNIQUE pentru a asigura că un ProdusInReferat este într-un singur ProdusInLot per Lot
    __table_args__ = (db.UniqueConstraint('ID_Lot', 'ID_Produs_Referat', name='_lot_produs_referat_uc'),)

    def __repr__(self):
        return f"<ProdusInLot {self.ID_Produs_Lot} (Lot: {self.ID_Lot}, ProdRef: {self.ID_Produs_Referat})>"

# --- Tabele de Asociere (Many-to-Many) ---

# Enum pentru tipurile de proceduri de achiziție
class TipProcedura(enum.Enum):
    LICITATIE_DESCHISA = "Licitatie deschisa"
    PROCEDURA_SIMPLIFICATA = "Procedura simplificata"
    ACHIZITIE_DIRECTA = "Achizitie directa"
    NEGOCIERE_COMPETITIVA = "Negociere competitiva"
    ALTELE = "Altele"

# Enum pentru tipurile de contracte
class TipContract(enum.Enum):
    CONTRACT_FERM = "Contract de furnizare (livrare integrala)"
    ACORD_CADRU = "Acord-cadru (comenzi subsecvente)"

# Tabela de legătură pentru Contracte <-> Loturi
# Enum pentru tipurile de documente de livrare
class TipDocument(enum.Enum):
    FACTURA = "Factură"
    AVIZ_EXPEDITIE = "Aviz de expediție"
    CERTIFICAT_CALITATE = "Certificat de calitate"
    ALTUL = "Alt document"

# Tabelă nouă de asociere pentru LotProcedura <-> ProdusInReferat
lot_procedura_articole_asociere = db.Table(
    'lot_procedura_articole_asociere',
    db.Column('lot_procedura_id', db.Integer, db.ForeignKey('Loturi_Procedura.ID_Lot_Procedura'), primary_key=True),
    db.Column('produs_referat_id', db.Integer, db.ForeignKey('Produse_In_Referate.ID_Produs_Referat'), primary_key=True)
)

# Tabelă nouă de asociere pentru Contracte <-> LoturiProcedura
contracte_loturi_procedura_asociere = db.Table(
    'contracte_loturi_procedura_asociere',
    db.Column('contract_id', db.Integer, db.ForeignKey('Contracte.ID_Contract'), primary_key=True),
    db.Column('lot_procedura_id', db.Integer, db.ForeignKey('Loturi_Procedura.ID_Lot_Procedura'), primary_key=True)
)



# Model nou pentru "Super-Loturi"
class LotProcedura(db.Model):
    __tablename__ = 'Loturi_Procedura'
    ID_Lot_Procedura = db.Column(db.Integer, primary_key=True)
    ID_Procedura = db.Column(db.Integer, db.ForeignKey('Proceduri_Achizitie.ID_Procedura'), nullable=False)
    Nume_Lot = db.Column(db.Text, nullable=False)
    Descriere_Lot = db.Column(db.Text)

    # Relație Many-to-Many cu articolele din referate
    articole_incluse = db.relationship(
        'ProdusInReferat',
        secondary=lot_procedura_articole_asociere,
        backref='loturi_procedura_asociate'
    )
# Modelul LotProcedura are acum o relație One-to-Many cu ProceduraAchizitie (vezi procedura_parinte in ProceduraAchizitie)
# 11. Model pentru Proceduri de Achiziție (fostul Licitatii)
class ProceduraAchizitie(db.Model):
    __tablename__ = 'Proceduri_Achizitie'
    ID_Procedura = db.Column(db.Integer, primary_key=True)
    Nume_Procedura = db.Column(db.Text, nullable=False)
    Tip_Procedura = db.Column(db.Enum(TipProcedura), nullable=False)
    Data_Creare = db.Column(db.Date, nullable=False, default=date.today)
    Stare = db.Column(db.Text, nullable=False, default='In Desfasurare')
    Numar_Inregistrare_Caiet_Sarcini = db.Column(db.Text)
    Data_Inregistrare_Caiet_Sarcini = db.Column(db.Date)
    Link_Scan_Caiet_Sarcini_PDF = db.Column(db.Text)
    ID_Utilizator_Creare = db.Column(db.Integer, db.ForeignKey('Utilizatori.ID_Utilizator'))

    # Relație nouă One-to-Many către noile loturi de procedură
    loturi_procedura = db.relationship('LotProcedura', backref='procedura_parinte', lazy=True, cascade="all, delete-orphan")
    oferte = db.relationship('Oferta', backref='procedura_parinte', lazy=True)
    contracte_rel = db.relationship('Contract', backref='procedura_contract', lazy=True)

    def __repr__(self):
        return f"<ProceduraAchizitie {self.Nume_Procedura}>"

# 12. Model nou pentru Oferte (Antet)
class Oferta(db.Model):
    __tablename__ = 'Oferte'
    ID_Oferta = db.Column(db.Integer, primary_key=True)
    ID_Furnizor = db.Column(db.Integer, db.ForeignKey('Furnizori.ID_Furnizor'), nullable=False)
    Data_Oferta = db.Column(db.Date, nullable=False, default=date.today)
    Numar_Inregistrare = db.Column(db.Text)
    Data_Inregistrare = db.Column(db.Date)
    Moneda = db.Column(db.Text, nullable=False, default='RON')
    
    # Legături opționale către alte module
    ID_Procedura = db.Column(db.Integer, db.ForeignKey('Proceduri_Achizitie.ID_Procedura'), nullable=True)
    ID_Referat = db.Column(db.Integer, db.ForeignKey('Referate_Necesitate.ID_Referat'), nullable=True)
    
    # Relație către articolele din ofertă
    articole = db.relationship('ArticolOferta', backref='oferta_parinte', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Oferta {self.ID_Oferta} de la {self.furnizor.Nume_Furnizor if self.furnizor else 'N/A'}>"

# Model nou pentru Articolele dintr-o Ofertă (Linii)
class ArticolOferta(db.Model):
    __tablename__ = 'Articole_Oferta'
    ID_Articol_Oferta = db.Column(db.Integer, primary_key=True)
    ID_Oferta = db.Column(db.Integer, db.ForeignKey('Oferte.ID_Oferta'), nullable=False)
    ID_Varianta_Comerciala = db.Column(db.Integer, db.ForeignKey('Variante_Comerciale_Produs.ID_Varianta_Comerciala'), nullable=False)
    ID_Produs_Referat = db.Column(db.Integer, db.ForeignKey('Produse_In_Referate.ID_Produs_Referat'), nullable=True)
    Pret_Unitar_Pachet = db.Column(db.Float, nullable=False)
    ID_Lot_Procedura = db.Column(db.Integer, db.ForeignKey('Loturi_Procedura.ID_Lot_Procedura'), nullable=True) # Adăugat
    Observatii = db.Column(db.Text)

    def __repr__(self):
        return f"<ArticolOferta {self.ID_Articol_Oferta} (Oferta: {self.ID_Oferta})>"


# 13. Model pentru Contracte
class Contract(db.Model):
    __tablename__ = 'Contracte'
    Tip_Contract = db.Column(db.Enum(TipContract), nullable=False, default=TipContract.ACORD_CADRU)
    ID_Contract = db.Column(db.Integer, primary_key=True)
    ID_Procedura = db.Column(db.Integer, db.ForeignKey('Proceduri_Achizitie.ID_Procedura'), nullable=False)
    ID_Furnizor = db.Column(db.Integer, db.ForeignKey('Furnizori.ID_Furnizor'), nullable=False)
    Pret_Total_Contract = db.Column(db.Float, nullable=False)
    Moneda = db.Column(db.Text, nullable=False, default='RON')
    ID_Utilizator_Creare = db.Column(db.Integer, db.ForeignKey('Utilizatori.ID_Utilizator'))
    Data_Semnare = db.Column(db.Date, nullable=False, default=date.today)
    Numar_Contract = db.Column(db.Text, nullable=False)
    Numar_Inregistrare_Document = db.Column(db.Text)
    Data_Inregistrare_Document = db.Column(db.Date)
    Link_Scan_PDF = db.Column(db.Text)
    ID_Utilizator_Creare = db.Column(db.Integer, db.ForeignKey('Utilizatori.ID_Utilizator'))
    # Relație Many-to-Many cu Loturile de Procedură
    loturi_procedura_contractate = db.relationship(
        'LotProcedura',
        secondary=contracte_loturi_procedura_asociere,
        backref='contracte_asociate'
    )
    articole_contractate = db.relationship('ArticolContractat', backref='contract_parinte', lazy=True, cascade="all, delete-orphan")
    comenzi_rel = db.relationship('ComandaGeneral', backref='contract_comanda', lazy=True)
    def __repr__(self):
        return f"<Contract {self.Numar_Contract}>"

# 14. Model pentru Articole_Contractate (fost ArticolContractatInLot)
class ArticolContractat(db.Model):
    __tablename__ = 'Articole_Contractate'
    ID_Articol_Contractat = db.Column(db.Integer, primary_key=True)
    ID_Contract = db.Column(db.Integer, db.ForeignKey('Contracte.ID_Contract'), nullable=False)
    ID_Produs_Referat = db.Column(db.Integer, db.ForeignKey('Produse_In_Referate.ID_Produs_Referat'), nullable=False)
    ID_Varianta_Comerciala = db.Column(db.Integer, db.ForeignKey('Variante_Comerciale_Produs.ID_Varianta_Comerciala'), nullable=False)
    Cantitate_Contractata_Pachete = db.Column(db.Integer, nullable=False)
    Pret_Unitar_Pachet_Contract = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<ArticolContractat {self.ID_Articol_Contractat}>"

# 15. Model pentru Comanda_General
class ComandaGeneral(db.Model):
    __tablename__ = 'Comanda_General'
    ID_Comanda_General = db.Column(db.Integer, primary_key=True)
    ID_Contract = db.Column(db.Integer, db.ForeignKey('Contracte.ID_Contract'), nullable=False)
    Data_Comanda = db.Column(db.Date, nullable=False, default=date.today)
    Numar_Comanda = db.Column(db.Text)
    Stare_Comanda = db.Column(db.Text, nullable=False, default='Emisa') # Ex: Emisa, Livrata Partial, Livrata Complet, Anulata
    Numar_Inregistrare_Document = db.Column(db.Text)
    Data_Inregistrare_Document = db.Column(db.Date)
    Link_Scan_PDF = db.Column(db.Text)
    ID_Utilizator_Creare = db.Column(db.Integer, db.ForeignKey('Utilizatori.ID_Utilizator'))

    # Relații
    detalii_produse_comanda_rel = db.relationship('DetaliiComandaProdus', backref='comanda_parinte', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ComandaGeneral {self.Numar_Comanda or self.ID_Comanda_General}>"

# 16. Model pentru Detalii_Comanda_Produs
class DetaliiComandaProdus(db.Model):
    __tablename__ = 'Detalii_Comanda_Produs'
    ID_Detalii_Comanda_Produs = db.Column(db.Integer, primary_key=True)
    ID_Comanda_General = db.Column(db.Integer, db.ForeignKey('Comanda_General.ID_Comanda_General'), nullable=False)
    ID_Articol_Contractat = db.Column(db.Integer, db.ForeignKey('Articole_Contractate.ID_Articol_Contractat'), nullable=False)
    Cantitate_Comandata_Pachete = db.Column(db.Integer, nullable=False)

    # Relații
    livrari_rel = db.relationship('LivrareComanda', backref='detalii_comanda_rel', lazy=True, cascade="all, delete-orphan")
    articol_contractat_rel = db.relationship('ArticolContractat', backref='comenzi_asociate', lazy=True)

    def __repr__(self):
        return f"<DetaliiComandaProdus {self.ID_Detalii_Comanda_Produs}>"

# 17. Model pentru Livrare_Comenzi
class LivrareComanda(db.Model):
    __tablename__ = 'Livrare_Comenzi'
    ID_Livrare = db.Column(db.Integer, primary_key=True)
    ID_Detalii_Comanda_Produs = db.Column(db.Integer, db.ForeignKey('Detalii_Comanda_Produs.ID_Detalii_Comanda_Produs'), nullable=False)
    Cantitate_Livrata_Pachete = db.Column(db.Integer, nullable=False)
    Data_Livrare = db.Column(db.Date, nullable=False, default=date.today)
    Numar_Lot_Producator = db.Column(db.Text, nullable=True) # Cheie pentru stocuri
    Data_Expirare = db.Column(db.Date, nullable=True) # Cheie pentru stocuri
    ID_Utilizator_Inregistrare = db.Column(db.Integer, db.ForeignKey('Utilizatori.ID_Utilizator'))

    # Relații
    documente_asociate = db.relationship('DocumentLivrare', backref='livrare_parinte', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<LivrareComanda {self.ID_Livrare}>"

# 18. Model pentru Documente Livrare
class DocumentLivrare(db.Model):
    __tablename__ = 'Documente_Livrare'
    ID_Document = db.Column(db.Integer, primary_key=True)
    ID_Livrare = db.Column(db.Integer, db.ForeignKey('Livrare_Comenzi.ID_Livrare'), nullable=False)
    Tip_Document = db.Column(db.Enum(TipDocument), nullable=False)
    Numar_Document = db.Column(db.Text, nullable=False)
    Data_Document = db.Column(db.Date, nullable=True)
    Link_Scan_PDF = db.Column(db.Text)

    def __repr__(self):
        return f"<DocumentLivrare {self.Tip_Document.value} {self.Numar_Document}>"