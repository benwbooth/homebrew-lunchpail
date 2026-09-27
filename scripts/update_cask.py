#!/usr/bin/env python3
"""Update the cask only from a complete, checksum-verified stable release."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile


REPOSITORY = "benwbooth/lunchbox"
DMG = "Lunchbox-macos-arm64.dmg"
REQUIRED = {
    DMG, "Lunchbox-windows-x86_64.msi", "Lunchbox-windows-x86_64.zip",
    "Lunchbox-linux-x86_64.AppImage", "Lunchbox-linux-x86_64.flatpak",
    "Lunchbox-flatpak-repo.tar.gz", "lunchbox.rb", "SHA256SUMS",
}


def render(release, checksums):
    tag = release["tag_name"]
    if release["draft"] or release["prerelease"] or not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        raise ValueError("Expected a published stable version tag")
    assets = {asset["name"]: asset for asset in release["assets"]}
    if not REQUIRED <= assets.keys() or any(assets[name]["size"] <= 0 for name in REQUIRED):
        raise ValueError("Release upload is incomplete; leaving the existing cask untouched")
    digest = "sha256:" + hashlib.sha256(checksums).hexdigest()
    if assets["SHA256SUMS"].get("digest") != digest:
        raise ValueError("SHA256SUMS does not match the published asset digest")
    entries = {}
    for line in checksums.decode("utf-8").splitlines():
        checksum, filename = line.split(maxsplit=1)
        name = Path(filename.lstrip("*")).name
        if name in entries or not re.fullmatch(r"[0-9a-f]{64}", checksum):
            raise ValueError("Invalid or duplicate checksum entry")
        entries[name] = checksum
    sha = entries[DMG]
    if assets[DMG].get("digest") != "sha256:" + sha:
        raise ValueError("DMG digest disagrees with SHA256SUMS")
    version = tag[1:]
    return f'''cask "lunchbox" do
  version "{version}"
  sha256 "{sha}"

  url "https://github.com/benwbooth/lunchbox/releases/download/v#{{version}}/Lunchbox-macos-arm64.dmg"
  name "Lunchbox"
  desc "Retro game library and emulator frontend"
  homepage "https://github.com/benwbooth/lunchbox"

  depends_on arch: :arm64
  depends_on macos: ">= :ventura"

  app "Lunchbox.app"

  zap trash: [
    "~/Library/Application Support/Lunchbox",
    "~/Library/Caches/Lunchbox",
    "~/Library/Preferences/io.github.benwbooth.Lunchbox.plist",
  ]
end
'''


def main():
    release = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/{REPOSITORY}/releases/latest"], text=True))
    tag = release["tag_name"]
    with tempfile.TemporaryDirectory(prefix="lunchbox-cask-") as directory:
        subprocess.run([
            "gh", "release", "download", tag, "--repo", REPOSITORY,
            "--pattern", "SHA256SUMS", "--dir", directory,
        ], check=True)
        cask = render(release, (Path(directory) / "SHA256SUMS").read_bytes())
    destination = Path(__file__).resolve().parents[1] / "Casks" / "lunchbox.rb"
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(cask, encoding="utf-8")
    print(f"Cask verified against {tag}'s published checksums")


if __name__ == "__main__":
    main()
