"""A module for classifying files in the /etc directory into predefined categories."""

import os
import json
from typing import Dict, AnyStr
from FileTypeIdentifier import FileTypeIdentifier, ScriptLikeCheck, CertLikeCheck
from FileNode import FileNode


def get_base_directory():
    """Return the base directory for classification."""
    return "/etc"


def get_categories():
    """Define categories and their associated file patterns for classification."""
    return {
        "System Configuration": [
            "/hostname",
            "/hosts",
            "/nsswitch.conf",
            "/networks",
            "/resolv.conf",
            "/fstab",
            "/mkinitcpio.conf",
            "/systemd",
            "/rc.local",
            "/modules-load.d",
            "/modprobe.d",
            "/udev",
            "/locale.gen",
            "/vconsole.conf",
            "/locale.conf",
            "/adjtime",
            "/timezone",
            "/localtime",
            "/zoneinfo",
        ],
        "Security and Authentication": [
            "/passwd",
            "/shadow",
            "/group",
            "/gshadow",
            "/subuid",
            "/subgid",
            "/pam.d",
            "/ssh",
            "/security",
            "/sudoers",
            "/polkit-1",
            "/gnupg",
            "/ssl",
            "/pki",
            "/selinux",
            "/ca-certificates",
            "/cifs-utils",
            "/private",
            "/authselect",
            "/keys",
        ],
        "Network Services Configuration": [
            "/dnsmasq.conf",
            "/dhcpcd.conf",
            "/ufw",
            "/iptables",
            "/httpd",
            "/nginx",
            "/postfix",
            "/dovecot",
            "/network",
            "/apache2",
            "/iproute2",
            "/ppp",
        ],
        "Package Management": [
            "/pacman.conf",
            "/pacman.d",
            "/apt",
            "/dpkg",
            "/yum.conf",
            "/yum.repos.d",
            "/rpm",
            "/dnf",
            "/vmware",
        ],
        "System Services and Daemons": [
            "/rsyslog.conf",
            "/syslog.conf",
            "/logrotate.d",
            "/crontab",
            "/cron.d",
            "/systemd/timers",
            "/cups",
            "/samba",
            "/nfs.conf",
            "/exports",
            "/sane.d",
            "/services",
            "/sysctl.d",
            "/init.d",
            "alsa",
        ],
        "Hardware and Drivers": [
            "/cups",
            "/pulse",
            "/asound.conf",
            "/vulkan",
            "/drirc",
            "/udev",
        ],
        "Desktop Environment and Display Managers": [
            "/lightdm",
            "/gdm",
            "/xdg",
            "/fonts",
            "/fontconfig",
            "/X11",
            "/dbus-1",
        ],
        "Miscellaneous": [
            "/profile",
            "/bash.bashrc",
            "/zsh",
            "/environment",
            "/fstab",
            "/exports",
            "/libvirt",
            "openjdk",
            "/speech-dispatcher",
        ],
        "Bootloaders": ["/grub.d", "grub"],
        "Cloud": ["/cloud", "/aws", "/azure", "/gcp"],
    }


def initialize_classification(categories: Dict) -> Dict:
    """Initialize a classification dictionary based on the provided categories."""
    return {category: [] for category in categories} | {"Others": []}


def classify_path(path: AnyStr, categories: Dict) -> AnyStr:
    """Classify a given path into one of the predefined categories."""
    for category, patterns in categories.items():
        for pattern in patterns:
            if pattern in path.replace("/usr/share", "").replace("/usr/lib", ""):
                return category
    return "Others"


def is_regular_file(path: AnyStr) -> bool:
    """Check if the path is a regular file."""
    return os.path.isfile(path)


def get_file_type_identifier() -> FileTypeIdentifier:
    """Return a file type identifier with registered checks."""
    file_identifier = FileTypeIdentifier.FileTypeIdentifier()
    file_identifier.register_check(ScriptLikeCheck.ScriptLikeCheck())
    file_identifier.register_check(CertLikeCheck.CertLikeCheck())
    return file_identifier


def walk_directory_and_classify(base_dir: AnyStr, categories: dict) -> dict:
    """Walk through the directory and classify files according to predefined categories."""
    classification = initialize_classification(categories)
    file_identifier = get_file_type_identifier()
    for root, _, files in os.walk(base_dir, followlinks=True):
        for name in files:
            source_path = os.path.join(root, name)
            full_path = os.path.realpath(source_path)

            if not is_regular_file(full_path):
                continue

            internal_types = file_identifier.identify(full_path)

            category = classify_path(full_path, categories)
            file_node = FileNode(full_path, internal_types)
            classification[category].append(file_node.to_dict())
    return classification


def save_classification_to_json(
    classification: dict, filename: AnyStr = "class.json"
) -> None:
    """Save the classification result to a JSON file."""
    with open(filename, "w", encoding="utf-8") as outfile:
        list_data = {k: list(v) for k, v in classification.items()}
        json.dump(list_data, outfile, indent=4)


def main() -> None:
    """Main function to classify files in the /etc directory."""
    base_dir = get_base_directory()
    categories = get_categories()
    classification = walk_directory_and_classify(base_dir, categories)
    save_classification_to_json(classification)
    print("Classification completed and saved to class.json.")


if __name__ == "__main__":
    main()
