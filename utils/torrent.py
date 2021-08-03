import libtorrent as lt
import time
import threading
import sys

class TorrentNode(object):
    def __init__(self, magnet, path):
        self.magnet = magnet
        self.status = ""
        self.path = path
        self.progress = 0
        self.downspeed = 0
        self.name = ""
    def start(self):
        my_thread = threading.Thread(target=self.download)
        my_thread.daemon = True
        my_thread.start()
    def download(self):
        ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})
        params = {
            'save_path': self.path,
            'storage_mode': lt.storage_mode_t(2)}
        h = lt.add_magnet_uri(ses, self.magnet, params)
        s = h.status()
        self.status = "metadata"
        while (not s.is_seeding):
            s = h.status()
            self.status = "active"
            self.downspeed = s.download_rate / 1000
            self.progress = s.progress * 100
            self.name = s.name

            alerts = ses.pop_alerts()
            for a in alerts:
                if a.category() & lt.alert.category_t.error_notification:
                    print(a)
            time.sleep(1)

        self.status = "complete"
        self.downspeed = 0