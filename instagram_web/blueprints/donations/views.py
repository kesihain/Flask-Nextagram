from flask import Blueprint, render_template,Flask, request,redirect,url_for,flash
from flask_login import login_required, login_user, current_user
from instagram_web.util.helpers import gateway
from instagram_web.util.helpers import generate_client_token, transact, find_transaction
from models.donation import Donation
from models.user import User
from models.image import Image
import braintree

donations_blueprint = Blueprint('donations',
                                __name__,
                                template_folder='templates')

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

@donations_blueprint.route('/new')
@login_required
def new(image_id):
    client_token = gateway.client_token.generate({
        # "user_id":
    })
    return render_template('donations/new.html',client_token=client_token,image_id=image_id)


@donations_blueprint.route("/donate", methods=["POST"])
def create_donate(image_id):
    nonce_from_the_client = request.form["nonce"]
    amount=request.form['amount']
    # Use payment method nonce here...
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce_from_the_client,
        # "device_data": device_data_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success or result.transaction:
        donation = Donation(user_id=User.get_by_id(current_user.id),image_id=image_id,amount=amount)
        if donation.save():
            return redirect(url_for('users.show',username=Image.get_by_id(image_id).user_id.username))
        else:
            flash('Oops.. there may be some issue. transaction went through but donation was not saved. Please contact customer support')
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('donations.new',image_id=image_id))
    return redirect(url_for('users.show',username=current_user.username))
