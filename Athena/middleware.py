from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.http import HttpResponsePermanentRedirect


class AutoLogout:
  def process_request(self, request):
    if not request.user.is_authenticated() :
      #Can't log out if not logged in
      return

    try:
      if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
	del request.session['last_touch']        
	auth.logout(request)
	request.session['advise'] = 'true';     
        #return HttpResponsePermanentRedirect(redirect_url)
    except KeyError:
      pass

    request.session['last_touch'] = datetime.now()
