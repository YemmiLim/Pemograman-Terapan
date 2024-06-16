from flask import Flask, jsonify, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
app = Flask(__name__)
app.config['SECRET_KEY'] = 'terapandebest'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"
db = SQLAlchemy(app)
CORS(app)

class TerimaBarang(db.Model):
    __tablename__ = 'terima_barang'
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    id_supplier = db.Column(db.Integer, db.ForeignKey('barang_supplier.id'), nullable=False)
    supplier = db.relationship("BarangSupplier", back_populates="pesanan")
    def json(self):
        return {
            'id': self.id,
            'id_supplier': self.id_supplier,
            'qty': self.qty,
        }

class BarangSupplier(db.Model):
    __tablename__ = 'barang_supplier'
    id = db.Column(db.Integer, primary_key=True)
    nama_barang = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    nama_supplier = db.Column(db.String(100), nullable=False)
    
    pesanan = db.relationship("TerimaBarang", back_populates="supplier")

    def json(self):
        return {
            'id': self.id,
            'nama_barang': self.nama_barang,
            'harga': self.harga,
            'nama_supplier': self.nama_supplier
        }



#home
@app.route('/')
def home():
    return render_template('/index.html')


@app.route('/barang_supplier', methods=['GET'])
def list_barang():
    barang = BarangSupplier.query.all()
    return render_template('/supplier/display.html', barang=barang)


@app.route('/barang_supplier/create', methods=['GET'])
def create_supplier():
    return render_template('/supplier/create.html')


## Get Semua Barang dalam Tabel
@app.route('/barang_supplier/update/<int:id>', methods=['GET'])
def get_all_barang(id):
    barang = BarangSupplier.query.get_or_404(id)
    return render_template('/supplier/update.html', barang=barang)


@app.route('/barang_supplier/create', methods=['POST'])
def add_supplier():
    data = request.form
    supplier = BarangSupplier(
        nama_barang=data['nama_barang'],
        harga=data['harga'],
        nama_supplier=data['nama_supplier']
    )
    db.session.add(supplier)
    db.session.commit()
    return redirect(url_for('list_barang'))


@app.route('/barang_supplier/update/<int:id>', methods=['POST'])
def update_supplier(id):
    data = request.form
    barang = BarangSupplier.query.get_or_404(id)
    barang.nama_barang = data.get('nama_barang', barang.nama_barang)
    barang.harga = data.get('harga', barang.harga)
    barang.nama_supplier = data.get('nama_supplier', barang.nama_supplier)
    db.session.commit()
    return redirect(url_for('list_barang'))


@app.route('/barang_supplier/delete/<int:id>', methods=['POST'])
def delete_supplier(id):
    barang = BarangSupplier.query.get_or_404(id)
    db.session.delete(barang)
    db.session.commit()
    return redirect(url_for('list_barang'))


### Terima Barang
@app.route('/terima_barang', methods=['GET'])
def list_pesan():
    pesan_list = TerimaBarang.query.all()
    return render_template('/terima/display.html', pesan_list=pesan_list)

@app.route('/terima_barang/create', methods=['GET'])
def create_pesan():
    return render_template('/terima/create.html')

## Get Semua Barang dalam Tabel
@app.route('/terima_barang/update/<int:id>', methods=['GET'])
def get_all_pesan(id):
    pesan = TerimaBarang.query.get_or_404(id)
    return render_template('/terima/update.html', pesan=pesan)

@app.route('/terima_barang/create', methods=['POST'])
def add_pesan():
    data = request.form
    supplier_id = int(data['id_supplier'])  
    qty = int(data['qty'])  
    supplier = BarangSupplier.query.get_or_404(supplier_id)
    new_pesan = TerimaBarang(
        id_supplier=supplier_id,
        qty=qty
    )
    

    db.session.add(new_pesan)
    db.session.commit()
    

    return redirect(url_for('list_pesan'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
