import flask
import flask.views
from annie.api.users import models
from annie import db


class UserApi(flask.views.MethodView):

    # GET /users/
    # GET /users/<user_id>/
    #@requires_auth
    def get(self, user_id):
        """
        200, 404, 400, 403
        """
        if user_id:
            user = models.User.query.filter_by(user_id=user_id).first()
            if user:
                return flask.jsonify(user=user.toJSON())
            else:
                return flask.Response(
                    status=404
                )
        else:
            result = models.User.query.all()
            if result:
                return flask.jsonify(users=[i.toJSON() for i in result])
            else:
                return flask.Response(
                    status=404
                )

    # POST /users/
    def post(self):
        """
        201, 400, 409
        """
        user_name = flask.request.form['user_name']
        user_password = flask.request.form['user_password']
        user_email = flask.request.form['user_email']

        user = models.User.query.filter_by(user_email=user_email).first()
        if user:
            return flask.Response(
                status=409
            )
        else:
            new_user = models.User(user_name, user_password, user_email)
            try:
                db.session.add(new_user)
                db.session.commit()
                return flask.Response(
                    status=201,
                    headers={
                        "Location": "http://localhost:5000/users/%s/%s/" %
                        (new_user.user_id, new_user.user_name)
                    }
                )
            except:
                return flask.Response(
                    status=400
                )

    # PUT /users/<user_id>/
    #@requires_auth
    def put(self, user_id):
        """
        200, 301, 400, 404, 409
        """
        user = models.User.query.filter_by(user_id=user_id).first()
        if user:
            # new user_name already exist
            if 'user_name' in flask.request.form:
                new_name = flask.request.form['user_name']
            old_name = user.user_name
            if old_name != new_name and \
                    models.User.query.filter_by(user_name=new_name).first():
                return flask.Response(
                    status=409
                )
            else:
                try:
                    # update user name
                    if new_name != old_name:
                        user.user_name = new_name
                        db.session.commit()
                        return flask.Response(
                            status=301
                        )
                    else:
                        # nothing change
                        return flask.Response(
                            status=200
                        )
                except:
                    return flask.Response(
                        status=400
                    )
        else:
            return flask.Response(
                status=404
            )

    # DELETE /users/<user_id>/
    #@requires_auth
    def delete(self, user_id):
        """
        200, 400, 404
        """
        user = models.User.query.filter_by(user_id=user_id).first()
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                return flask.Response(
                    status=200
                )
            except:
                return flask.Response(
                    status=400
                )
        else:
            return flask.Response(
                status=404
            )
