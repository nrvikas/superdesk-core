# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from flask import g, current_app as app
from superdesk.resource import Resource
from superdesk.notification import push_notification
from superdesk.services import BaseService
from .user_mentions import get_users, get_desks, get_mentions, notify_mentioned_users, notify_mentioned_desks
from superdesk.errors import SuperdeskApiError

comments_schema = {
    'text': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 500,
        'required': True,
    },
    'item': {'type': 'string'},
    'user': Resource.rel('users', True),
    'mentioned_users': {
        'type': 'dict'
    },
    'mentioned_desks': {
        'type': 'dict'
    }
}


class CommentsResource(Resource):
    """Reusable implementation for comments."""

    schema = comments_schema
    resource_methods = ['GET', 'POST', 'DELETE']
    datasource = {'default_sort': [('_created', -1)]}
    privileges = {'POST': 'archive', 'DELETE': 'archive'}


class CommentsService(BaseService):
    notification_key = 'comments'

    def on_create(self, docs):
        for doc in docs:
            sent_user = doc.get('user', None)
            user = g.user
            if sent_user and sent_user != str(user.get('_id')):
                message = 'Commenting on behalf of someone else is prohibited.'
                raise SuperdeskApiError.forbiddenError(message)
            doc['user'] = str(user.get('_id'))
            user_names, desk_names = get_mentions(doc.get('text'))
            doc['mentioned_users'] = get_users(user_names)
            doc['mentioned_desks'] = get_desks(desk_names)

    def on_created(self, docs):
        for doc in docs:
            push_notification(self.notification_key, item=str(doc.get('item')))

        notify_mentioned_users(docs, app.config.get('CLIENT_URL', ''))
        notify_mentioned_desks(docs)

    def on_updated(self, updates, original):
        push_notification(self.notification_key, updated=1)

    def on_deleted(self, doc):
        push_notification(self.notification_key, deleted=1)
