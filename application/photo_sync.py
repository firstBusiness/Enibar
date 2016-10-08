import settings
import requests
import api.notes
from urllib.parse import urljoin
import os.path
import api.redis
import datetime

last_updated = api.redis.get_key_blocking('photos_last_update')

if last_updated:
    photos = requests.get(settings.WEB_URL + "photos", params={'last_updated': last_updated}).json()
else:
    photos = requests.get(settings.WEB_URL + "photos").json()

notes = api.notes.get()

for mail, photo in photos.items():
    for note in notes:
        if note['mail'] == mail:
            print(mail, photo)
            url = urljoin(settings.WEB_URL, "/static/medias/profile_pictures/" + photo)
            data = requests.get(url).content
            _, ext = os.path.splitext(photo)
            img_path = os.path.join(settings.IMG_BASE_DIR, note['mail'] + ext)
            with open(img_path, 'wb') as fd:
                fd.write(data)
            api.notes.change_values(note['nickname'], do_not=True, photo_path=note['mail'] + ext)
            break

last_updated = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S")
api.redis.set_key_blocking('photos_last_update', last_updated)

