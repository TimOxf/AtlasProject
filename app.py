from flask import Flask, render_template, request, Response, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from zillow import getZillow


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='xxxxxxxxxxxx'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Address_Owner(db.Model):
    __table__ = db.Table('address_owner_table', db.metadata, autoload=True, autoload_with=db.engine)

    def as_dict(self):
	       return {'Address': self.premiseadd}

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/search_address", methods=['POST','GET'])
def search_address():
    if request.method == 'POST':
        address_to_search = request.form["address_name"].upper() #normalise to upper case
        results = Address_Owner.query.filter(Address_Owner.fullpremise.like("%{}%".format(address_to_search)))
        #for result in results:
        #    print(result.ssl)
    return render_template('search.html',term=address_to_search, results=results)

@app.route("/search_owner", methods=['POST','GET'])
def search_owner():
    if request.method == 'POST':
        name_to_search = request.form["owner_name"].upper() #normalise to upper case
        #print(name_to_search)
        results = Address_Owner.query.filter(Address_Owner.ownername.like("%{}%".format(name_to_search)))
        #for result in results:
        #    print(result.ssl)
    return render_template('search.html',term=name_to_search, results=results)


@app.route('/address_autocomplete', methods=['GET'])
def address_autocomplete():
    search_term = request.args['search_term']
    #print(search_term)

    res = Address_Owner.query.filter(Address_Owner.fullpremise.like("%{}%".format(search_term))).limit(10)
    response_list = []
    for r in res:
        response_list.append(r.fullpremise)

    return jsonify(response_list)

@app.route('/owner_autocomplete', methods=['GET'])
def owner_autocomplete():
    search_term = request.args['search_term']
    #print(search_term)

    res = Address_Owner.query.filter(Address_Owner.ownername.like("%{}%".format(search_term))).limit(10)
    response_list = []
    for r in res:
        response_list.append(r.ownername)

    return jsonify(response_list)

@app.route('/zillow_status', methods=['GET'])
def zillow_status():
    address = request.args['address']
    citystatezip = request.args['citystatezip']
    #print(address + '   '+citystatezip)
    return jsonify(getZillow(address,citystatezip))


if __name__ == "__main__":
    #app.run(debug=True)
    app.run()
