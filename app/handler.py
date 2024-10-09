import os
import logging

from watchdog.events import FileSystemEventHandler
from pathlib import Path


class HostnameChangeHandler(FileSystemEventHandler):
    def __init__(
            self,
            root_directory,
            directory,
            segment_set: set[str],
            domain_set: set[str]):
        self.monitored_directory = directory

        self.registered_directory = Path(os.path.join(root_directory, ".registered_sites"))
        self.registered_directory.mkdir(parents=True, exist_ok=True)

        self.valid_hostnames = domain_set
        self.valid_hostnames |= self.scan_directory()
        self.segment_set = segment_set
    def scan_directory(self) -> set[str]:
        discovered_sites = set()
        p = Path(self.monitored_directory)
        for item in (x for x in p.iterdir() if x.is_dir()):
           discovered_sites.add(item.name)
           try:
               os.symlink(item.absolute(), os.path.join(self.registered_directory, item.name))
               logging.info(f"symlink created: {item.name}")
           except FileExistsError:
               pass
           a = 2
        return discovered_sites

    def check_hostname(self, hostname: str) -> bool:
        return hostname in self.valid_hostnames

    def on_created(self, event) -> None:
        if event.is_directory:
            impacted_dir = Path(event.src_path)
            self.valid_hostnames.add(impacted_dir.name)

            # We create a symbolic link for Caddy to read from. For delete, we delete and for moved
            # we unlink and link to the new spot. Caddy now just needs to check one directory for all validation.
            os.symlink(impacted_dir.absolute(), os.path.join(self.registered_directory, impacted_dir.name))
            logging.info(f'New hostname added: {impacted_dir}')

    def on_deleted(self, event) -> None:
        if event.is_directory and event.src_path not in self.segment_set:
            impacted_dir = Path(event.src_path)
            os.unlink(os.path.join(self.registered_directory, impacted_dir.name))
            self.valid_hostnames.remove(impacted_dir.name)
            logging.info(f'Hostname deleted: {impacted_dir}')

    def on_moved(self, event) -> None:
        original = Path(event.src_path)
        if event.is_directory and original.name not in self.segment_set:
            original = Path(event.src_path)
            target = Path(event.dest_path)
            os.unlink(os.path.join(self.registered_directory, original.name))
            os.symlink(target.absolute(), os.path.join(self.registered_directory, target.name))
            self.valid_hostnames.remove(original.name)
            self.valid_hostnames.add(target.name)
            logging.info(f'Hostname {original} renamed to {target}')
