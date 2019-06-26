import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.jinja2')

    if request.method == 'POST':
        try:
            donor = Donor.get(Donor.name == request.form['name'])
            new_donation = Donation(value=int(request.form['donation']),
                                    donor=donor)
            new_donation.save()
            return redirect(url_for('all'))
        except Donor.DoesNotExist:
            print('no donor found')
            return render_template('create.jinja2',
                                   error="!!!ERROR - Donor not in database!!!")

@app.route('/view')
def view():
    name = request.args.get('name', None)

    if name is None:
        return render_template('view.jinja2')

    try:
        donor = Donor.get(Donor.name == name)
        donations = Donation.select().where(Donation.donor == donor)
        return render_template('view.jinja2', donations=donations,
                               donor_name=donor.name)
    except Donor.DoesNotExist:
        return render_template('view.jinja2',
                               error="!!!ERROR - Donor not in database!!!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
