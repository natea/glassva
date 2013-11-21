"""Request Handler for /api endpoint."""

import io
import json
import logging
import webapp2

from oauth2client.appengine import StorageByKeyName

from model import Credentials
import util


class ApiHandler(webapp2.RequestHandler):
  """Request Handler for API pings."""

  def post(self):
    """Handles API pings."""
    logging.info('Got a post with payload %s', self.request.body)
    data = json.loads(self.request.body)
    logging.info("data: %s" % data)

    # TODO: evil, evil, evil hack to hardcode userToken
    userid = '105628305597873001570'

    self.mirror_service = util.create_service(
        'mirror', 'v1',
        StorageByKeyName(Credentials, userid, 'credentials').get())

    # Insert a timeline item user can reply to.
    logging.info('Inserting timeline item')
    body = {
        'creator': {
            'displayName': 'Your virtual assistant',
            'id': 'PYTHON_STARTER_PROJECT',
            'imageUrls': [
              'https://cloudanswers-concierge.herokuapp.com/public/img/cloudonly-glass.png'
            ]
        },
        'notification': {'level': 'DEFAULT'},
        'menuItems': [
          {'action': 'REPLY'}
        ]
    }

    # if self.request.get('html') == 'on':
    #   body['html'] = [self.request.get('message')]
    # else:
    
    body['text'] = data[0]['message']

    # media_link = self.request.get('imageUrl')
    # if media_link:
    #   if media_link.startswith('/'):
    #     media_link = util.get_full_url(self, media_link)
    #   resp = urlfetch.fetch(media_link, deadline=20)
    #   media = MediaIoBaseUpload(
    #       io.BytesIO(resp.content), mimetype='image/jpeg', resumable=True)
    # else:
    #   media = None

    # self.mirror_service is initialized in util.auth_required.
    self.mirror_service.timeline().insert(body=body).execute()
    ### TODO: return legit response codes
    return True

API_ROUTES = [
    ('/api', ApiHandler)
]