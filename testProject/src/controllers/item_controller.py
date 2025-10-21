from flask import Blueprint, render_template, request, redirect, url_for, session
from src.services.item_service import ItemService
from src.services.auth_service import AuthService  # assuming you have helper functions like getUserId etc
from src.utils.error_utils import get_error_message
from src.config.db_config import SessionLocal
from src.models.User import User
from src.middlewares.auth_middleware import login_required
from src.middlewares.owner_middleware import check_owner, check_not_owner


item_controller = Blueprint('item_controller', __name__)

# Commenting out middleware imports for later implementation
# from src.middlewares.auth_middleware import is_auth
# from src.middlewares.owner_middleware import check_owner, check_not_owner, check_is_liked


@item_controller.route('/catalog')
def catalog():
    db = SessionLocal()
    try:
        query = request.args.to_dict()
        items = ItemService.get_all(db, query)
        return render_template('item/catalog.html', items=items, title='Catalog Page')
    except Exception as err:
        error = get_error_message(err)
        return render_template('item/catalog.html', title='Catalog Page', error=error)
    finally:
        db.close()


@item_controller.route('/create', methods=['GET'])
@login_required
def create_get():
    empty_item = {
        'name': '',
        'category': '',
        'color': '',
        'image': '',
        'location': '',
        'formula': '',
        'description': ''
    }
    return render_template('item/create.html', title='Create Page', item=empty_item)


@item_controller.route('/create', methods=['POST'])
@login_required
def create_post():
    db = SessionLocal()
    try:
        item_data = request.form.to_dict()
        owner_id = session.get('user_id')  # or however you store the logged user id
        item = ItemService.create(db, item_data, owner_id)
        return redirect(url_for('item_controller.catalog'))
    except Exception as err:
        error = get_error_message(err)
        return render_template('item/create.html', item=item_data, title='Create Page', error=error)
    finally:
        db.close()


@item_controller.route('/<int:item_id>/details')
def details(item_id):
    db = SessionLocal()
    try:
        item = ItemService.get_item(db, item_id)
        owner_id = item.owner_id if item else None
        user_id = session.get('user_id')

        is_owner = (owner_id == user_id)
        owner = db.query(User).filter(User.id == owner_id).first() if owner_id else None

        is_voted = user_id in [user.id for user in item.userList] if item else False
        vote_count = len(item.userList) if item else 0

        users = item.userList if item else []
        user_list_str = ', '.join([user.username for user in users])

        is_authenticated = 'user_id' in session  # <-- added this line

        return render_template(
            'item/details.html',
            item=item,
            title='Details Page',
            is_owner=is_owner,
            owner=owner,
            is_voted=is_voted,
            vote_count=vote_count,
            users=users,
            user_list=user_list_str,
            is_authenticated=is_authenticated  # <-- pass it here
        )
    finally:
        db.close()


@item_controller.route('/<int:item_id>/delete')
@login_required
# @check_owner
def delete(item_id):
    db = SessionLocal()
    try:
        ItemService.remove(db, item_id)
        return redirect(url_for('item_controller.catalog'))
    except Exception as err:
        error = get_error_message(err)
        return render_template('404.html', title='404 Page', error=error)
    finally:
        db.close()


@item_controller.route('/<int:item_id>/edit', methods=['GET'])
@login_required
# @check_owner  # middleware decorator commented out
def edit_get(item_id):
    db = SessionLocal()
    try:
        item = ItemService.get_by_id(db, item_id)
        return render_template('item/edit.html', item=item, title='Edit Page')
    except Exception as err:
        error = get_error_message(err)
        return render_template('item/edit.html', title='Edit Page', error=error)
    finally:
        db.close()


@item_controller.route('/<int:item_id>/edit', methods=['POST'])
@login_required
# @check_owner  # middleware decorator commented out
def edit_post(item_id):
    db = SessionLocal()
    try:
        item_data = request.form.to_dict()
        ItemService.edit(db, item_id, item_data)
        return redirect(url_for('item_controller.details', item_id=item_id))
    except Exception as err:
        error = get_error_message(err)
        return render_template('item/edit.html', item=item_data, title='Edit Page', error=error)
    finally:
        db.close()


@item_controller.route('/<int:item_id>/like')
@login_required
# @check_not_owner  # middleware decorator commented out
# @check_is_liked  # middleware decorator commented out
def like(item_id):
    db = SessionLocal()
    try:
        user_id = session.get('user_id')
        ItemService.like(db, item_id, user_id)
        return redirect(url_for('item_controller.details', item_id=item_id))
    except Exception:
        return redirect(url_for('item_controller.catalog'))
    finally:
        db.close()

