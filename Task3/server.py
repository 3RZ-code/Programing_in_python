from flask import Flask, render_template, request, make_response, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataset.db'

db.init_app(app)

class Dataset(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Gender: Mapped[int] = mapped_column(Integer, nullable=False)
    Age: Mapped[float] = mapped_column(Float, nullable=False)
    EstimatedSalary: Mapped[float] = mapped_column(Float, nullable=False)
    Purchased: Mapped[int] = mapped_column(Integer, nullable=False)


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('404.html'), 404)
    return resp

@app.errorhandler(400)
def bad_request(error):
    resp = make_response(render_template('400.html'), 400)
    return resp

@app.route('/')
def home():
    data = db.session.execute(db.select(Dataset)).scalars().all()
    print(data)
    return render_template('index.html', data = data)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        obj = [request.form['gender'], request.form['age'], request.form['estimated_salary'], request.form['purchased']]
        for i in obj:
            if i.isnumeric() == False:
                return bad_request(400)
        new_entry = Dataset(
            Gender=int(obj[0]),
            Age=float(obj[1]),
            EstimatedSalary=float(obj[2]),
            Purchased=int(obj[3])
        )
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/delete/<int:record_id>')
def delete(record_id):
    entry = Dataset.query.get(record_id)
    print(entry)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return not_found(404)
    

@app.route('/api/data', methods=['GET','POST'])
def api_data():
    if request.method == 'POST':
        obj = request.get_json()
        for key, value in obj.items():
            if value is None or str(value).isnumeric() == False:
                return jsonify({
                    'error 400': 'Invalid data'
                }), 400
        new_entry = Dataset(
            Gender=int(obj['Gender']),
            Age=float(obj['Age']),
            EstimatedSalary=float(obj['EstimatedSalary']),
            Purchased=int(obj['Purchased'])
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({
            'id' : new_entry.id,
        })
    elif request.method == 'GET':
        data = db.session.execute(db.select(Dataset)).scalars().all()
        return jsonify([{
            'id': row.id,
            'Gender': row.Gender,
            'Age': row.Age,
            'EstimatedSalary': row.EstimatedSalary,
            'Purchased': row.Purchased
        } for row in data])

@app.route('/api/data/<int:record_id>', methods=['DELETE'])
def delete_api(record_id):
    record = Dataset.query.get(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()
        return jsonify({f'{record}': 'Record has been deleted'})
    else:
        return jsonify({'Error 404': 'Entry not found'}), 404





# GRADE 5

df = pd.read_csv('DATA/Social_Network_Ads.csv')
x = df.drop(columns=['Purchased', 'User ID'])
x['Gender'] = x['Gender'].replace({'Male' : 0, 'Female' : 1})
x['Gender'] = x['Gender'].astype(int)
x['Age'] = x['Age'].astype(float)
x['EstimatedSalary'] = x['EstimatedSalary'].astype(float)
y = df['Purchased'].astype(int)
model = RandomForestClassifier()
model.fit(x, y)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        obj = [request.form['gender'], request.form['age'], request.form['estimated_salary']]
        for i in obj:
            if i.isnumeric() == False or i is None:
                return bad_request(400)
        x = [[int(obj[0]), float(obj[1]), float(obj[2])]]
        x_pred = model.predict(x)
        print(x_pred)
        return render_template('prediction.html', communicat="Prediction", pred=x_pred[0])
    return render_template('prediction.html', communicat=None, pred=None)


@app.route('/api/predictions', methods=['POST'])
def predict_api():
    if request.method == 'POST':
        obj = [request.args.get('Gender'), request.args.get('Age'), request.args.get('EstimatedSalary')]
        for i in obj:
            if str(i).isnumeric() == False or i is None:
                return jsonify({'Error 400': 'Invalid data'}), 400
        x = [obj]
        x_pred = model.predict(x)
        return jsonify({'Prediction' : int(x_pred[0])})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    