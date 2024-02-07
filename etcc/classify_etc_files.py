"""A module for classifying files in the /etc directory into predefined categories."""

import os
import json


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


def initialize_classification(categories: dict) -> dict:
    """Initialize a classification dictionary based on the provided categories."""
    return {category: set() for category in categories} | {"Others": set()}


def classify_path(path: str, categories: dict) -> str:
    """Classify a given path into one of the predefined categories."""
    for category, patterns in categories.items():
        for pattern in patterns:
            if pattern in path.replace("/usr/share", "").replace("/usr/lib", ""):
                return category
    return "Others"


def walk_directory_and_classify(base_dir: str, categories: dict) -> dict:
    """Walk through the directory and classify files according to predefined categories."""
    classification = initialize_classification(categories)
    for root, _, files in os.walk(base_dir, followlinks=True):
        for name in files:
            source_path = os.path.join(root, name)
            full_path = os.path.realpath(source_path)
            if not full_path.startswith(base_dir):
                continue
            category = classify_path(full_path, categories)
            classification[category].add(full_path)
    return classification


def save_classification_to_json(
    classification: dict, filename: str = "class.json"
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
