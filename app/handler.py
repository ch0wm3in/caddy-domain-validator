import os
import logging

from watchdog.events import FileSystemEventHandler

class HostnameChangeHandler(FileSystemEventHandler):
    def __init__(self, directory, segment_set: set[str], domain_set: set[str]):
        self.monitored_directory = directory
        self.valid_hostnames = domain_set
        self.valid_hostnames |= self.scan_directory()
        self.segment_set = segment_set

    def scan_directory(self) -> set[str]:
        return set((item for item in os.listdir(self.monitored_directory)
                    if os.path.isdir(os.path.join(self.monitored_directory, item))))

    def check_hostname(self, hostname: str) -> bool:
        return hostname in self.valid_hostnames

    def on_created(self, event) -> None:
        if event.is_directory:
            impacted_dir = os.path.basename(event.src_path)
            self.valid_hostnames.add(impacted_dir)
            logging.info(f'New hostname added: {impacted_dir}')

    def on_deleted(self, event) -> None:
        if event.is_directory and event.src_path not in self.segment_set:
            impacted_dir = os.path.basename(event.src_path)
            self.valid_hostnames.remove(impacted_dir)
            logging.info(f'Hostname deleted: {impacted_dir}')

    def on_moved(self, event) -> None:
        if event.is_directory and event.src_path not in self.segment_set:
            original = os.path.basename(event.src_path)
            target = os.path.basename(event.dest_path)
            self.valid_hostnames.remove(original)
            self.valid_hostnames.add(target)
            logging.info(f'Hostname {original} renamed to {target}')
