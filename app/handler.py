import os
import logging

from watchdog.events import FileSystemEventHandler


class HostnameChangeHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.monitored_directory = directory
        self.valid_hostnames = set()

    def scan_hostnames(self) -> set[str]:
        self.valid_hostnames = set((item for item in os.listdir(self.monitored_directory)
                                    if os.path.isdir(os.path.join(self.monitored_directory, item))))
        return self.valid_hostnames

    def on_created(self, event) -> None:
        if event.is_directory:
            impacted_dir = os.path.basename(event.src_path)
            self.valid_hostnames.add(impacted_dir)
            logging.info(f'New hostname added: {impacted_dir}')

    def on_deleted(self, event) -> None:
        if event.is_directory:
            impacted_dir = os.path.basename(event.src_path)
            self.valid_hostnames.remove(impacted_dir)
            logging.info(f'Hostname deleted: {impacted_dir}')

    def on_moved(self, event) -> None:
        if event.is_directory:
            original = os.path.basename(event.src_path)
            target = os.path.basename(event.dest_path)
            self.valid_hostnames.remove(original)
            self.valid_hostnames.add(target)
            logging.info(f'Hostname {original} renamed to {target}')
