#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import auth


class AutoLogout:

    def process_request(self, request):
        if not request.user.is_authenticated():

            # Can't log out if not logged in

            return

        try:
            if datetime.now() - request.session['last_touch'] \
                    > timedelta(0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                del request.session['last_touch']
                auth.logout(request)
                request.session['advise'] = 'true'
        except KeyError:

            # return HttpResponsePermanentRedirect(redirect_url)

            pass

        request.session['last_touch'] = datetime.now()
