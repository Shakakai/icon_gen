import cgi
import datetime
import logging

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import images

logging.getLogger().setLevel(logging.DEBUG)


class Greeting(db.Model):
    iphone4_app = db.BlobProperty()
    iphone_app = db.BlobProperty()
    ipad_app = db.BlobProperty()
    
    iphone4_spot = db.BlobProperty()
    iphone_spot = db.BlobProperty()
    ipad_spot = db.BlobProperty()
    
    appstore = db.BlobProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""<html><body>
              <h1>iPhone Icon Generator</h1>
              <p>Provide a 512x512 PNG-format icon image and we'll create the rest.</p>
              <form action="/generate" enctype="multipart/form-data" method="post">
                <div><label>Icon File:</label><input type="file" name="img"/></div>
                <div><input type="submit" value="Generate Icons"></div>
              </form>
            </body>
          </html>""")




class Image (webapp.RequestHandler):
    def get(self):
        greeting = db.get(self.request.get("img_id"))
        img_type = self.request.get("type")
        img = getattr(greeting, img_type)
        if img:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(img)
        else:
            self.response.out.write("No image")




class Guestbook(webapp.RequestHandler):
    
    def resize(self, w, h):
        return images.resize(self.request.get("img"), w, h)
    
    def post(self):
        g = Greeting()
        g.iphone4_app = db.Blob(self.resize(114,114))
        g.iphone_app = db.Blob(self.resize(57,57))
        g.ipad_app = db.Blob(self.resize(72,72))
        g.iphone4_spot = db.Blob(self.resize(58,58))
        g.iphone_spot = db.Blob(self.resize(50,50))
        g.ipad_spot = db.Blob(self.resize(29,29))
        g.appstore = db.Blob(self.request.get("img"))
        g.put()
        
        icon_types = {
            'iphone4_app' : 'iPhone 4 Appstore Icon',
            'iphone_app' : 'iPhone Appstore Icon',
            'ipad_app' : 'iPad Appstore Icon',
            'iphone4_spot' : 'iPhone 4 Spotlight',
            'iphone_spot' : 'iPhone Spotlight',
            'ipad_spot' : 'iPad Spotlight',
            'appstore' : 'Original' }
        
        for k in icon_types.keys():
            self.response.out.write("<h2>%s</h2><img src='img?img_id=%s&type=%s'/>" % (icon_types[k], g.key(), k))




application = webapp.WSGIApplication([
    ('/', MainPage)
    ,('/img', Image)
    ,('/generate', Guestbook)
], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
