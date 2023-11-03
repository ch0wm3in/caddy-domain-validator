import os
import logging

from watchdog.events import FileSystemEventHandler


class HostnameChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.monitored_directory = os.environ.get('SITE_DIRECTORY')
        self.valid_hostnames = set()

    def scan_hostnames(self):
        self.valid_hostnames = set((item for item in os.listdir(self.monitored_directory)
                                    if os.path.isdir(os.path.join(self.monitored_directory, item))))
        return self.valid_hostnames

    def on_created(self, event):
        if event.is_directory:
            impacted_dir = os.path.basename(event.src_path)
            self.valid_hostnames = self.valid_hostnames.add(impacted_dir)
            logging.info(f'New hostname added: {impacted_dir}')

    def on_deleted(self, event):
        if event.is_directory:
            impacted_dir = os.path.basename(event.src_path)
            self.valid_hostnames = self.valid_hostnames.remove(impacted_dir)
            logging.info(f'Hostname deleted: {impacted_dir}')

    def on_moved(self, event):
        if event.is_directory:
            self.scan_hostnames()
            original = os.path.basename(event.src_path)
            target = os.path.basename(event.dest_path)
            logging.info(f'Hostname {original} renamed to {target}')
