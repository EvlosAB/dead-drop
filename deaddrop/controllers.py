from flask import Blueprint, render_template, request
from cryptography.exceptions import InvalidKey
from deaddrop import crypto
from deaddrop.db import db
from deaddrop.models import EncryptedInformation

dd_blueprint = Blueprint(
    'dead-drop',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@dd_blueprint.route('/')
def index():
    return render_template(
        'encrypt.html'
    )


@dd_blueprint.route('/encrypt', methods=['POST'])
def encrypt():
    encrypt_text = request.form.get('encrypt-text')
    crypto_response = crypto.encrypt(encrypt_text)

    key = crypto_response[0].decode('UTF-8')
    token = crypto_response[1]

    db_row = EncryptedInformation(token=token)
    db.session.add(db_row)
    db.session.commit()

    url = f'{request.url_root}decrypt/{db_row.uuid}'

    return render_template(
        'encrypted.html',
        key=key,
        url=url,
    )


@dd_blueprint.route('/decrypt/<uuid>', methods=['GET'])
def decryption(uuid):
    return render_template(
        'decrypt.html',
        uuid=uuid,
    )


@dd_blueprint.route('/decrypt/<uuid>', methods=['POST'])
def decrypt(uuid):
    db_row = EncryptedInformation.query.filter_by(uuid=uuid).first()
    if not db_row:
        return render_template(
            'error.html',
            error='Informationen kunde inte hittas',
        )

    try:
        decrypted = crypto.decrypt(
            request.form.get('key').encode('UTF-8'),
            db_row.token,
        )
    except InvalidKey:
        # Delete information from database
        db.session.delete(db_row)
        db.session.commit()

        return render_template(
            'error.html',
            error='Nyckeln är ogiltig, informationen '
                  'du försökte hämta ut har blivit raderad.',
        )
    except Exception:
        # Delete information from database
        db.session.delete(db_row)
        db.session.commit()

        return render_template(
            'error.html',
            error='Nyckeln är antingen ogiltig eller '
                  'så uppstod annat fel, informationen '
                  'du försökte hämta ut har blivit raderad.',
        )

    # Delete information from database
    db.session.delete(db_row)
    db.session.commit()

    return render_template(
        'decrypted.html',
        text=decrypted,
    )
