#!/usr/bin/env python3
"""Update the cask only from a complete, checksum-verified stable release."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile


REPOSITORY = "benwbooth/lunchpail"
DMG = "Lunchpail-macos-arm64.dmg"
REQUIRED = {
    DMG, "Lunchpail-windows-x86_64.msi", "Lunchpail-windows-x86_64.zip",
    "Lunchpail-linux-x86_64.AppImage", "Lunchpail-linux-x86_64.flatpak",
    "Lunchpail-flatpak-repo.tar.gz", "lunchpail.rb", "SHA256SUMS",
}


def render(release, checksums):
    tag = release["tag_name"]
    if release["draft"] or release["prerelease"] or not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        raise ValueError("Expected a published stable version tag")
    assets = {asset["name"]: asset for asset in release["assets"]}
    required, dmg, app = REQUIRED, DMG, "Lunchpail.app"
    if not required <= assets.keys():
        required = {name.replace("Lunchpail", "Lunchbox").replace("lunchpail", "lunchbox")
                    for name in REQUIRED}
        dmg, app = "Lunchbox-macos-arm64.dmg", "Lunchbox.app"
    if not required <= assets.keys() or any(assets[name]["size"] <= 0 for name in required):
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
    sha = entries[dmg]
    if assets[dmg].get("digest") != "sha256:" + sha:
        raise ValueError("DMG digest disagrees with SHA256SUMS")
    version = tag[1:]
    return f'''cask "lunchpail" do
  version "{version}"
  sha256 "{sha}"

  url "https://github.com/benwbooth/lunchpail/releases/download/v#{{version}}/{dmg}"
  name "Lunchpail"
  desc "Retro game library and emulator frontend"
  homepage "https://github.com/benwbooth/lunchpail"

  depends_on arch: :arm64
  depends_on macos: :ventura

  app "{app}", target: "Lunchpail.app"

  zap trash: [
    "~/Library/Application Support/Lunchpail",
    "~/Library/Caches/Lunchpail",
    "~/Library/Preferences/io.github.benwbooth.Lunchpail.plist",
  ]
end
'''


def main():
    release = json.loads(subprocess.check_output(
        ["gh", "api", f"repos/{REPOSITORY}/releases/latest"], text=True))
    tag = release["tag_name"]
    with tempfile.TemporaryDirectory(prefix="lunchpail-cask-") as directory:
        subprocess.run([
            "gh", "release", "download", tag, "--repo", REPOSITORY,
            "--pattern", "SHA256SUMS", "--dir", directory,
        ], check=True)
        cask = render(release, (Path(directory) / "SHA256SUMS").read_bytes())
    destination = Path(__file__).resolve().parents[1] / "Casks" / "lunchpail.rb"
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(cask, encoding="utf-8")
    print(f"Cask verified against {tag}'s published checksums")


if __name__ == "__main__":
    main()
