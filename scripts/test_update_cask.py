import hashlib
import unittest

from update_cask import DMG, REQUIRED, render


class CaskTests(unittest.TestCase):
    def setUp(self):
        self.checksums = ("a" * 64 + "  release/mac/" + DMG + "\n").encode()
        self.release = {
            "tag_name": "v1.2.3", "draft": False, "prerelease": False,
            "assets": [{"name": name, "size": 1, "digest": "sha256:" + "a" * 64}
                       for name in REQUIRED],
        }
        self.asset("SHA256SUMS")["digest"] = "sha256:" + hashlib.sha256(self.checksums).hexdigest()

    def asset(self, name):
        return next(asset for asset in self.release["assets"] if asset["name"] == name)

    def test_verified_cask(self):
        cask = render(self.release, self.checksums)
        self.assertIn('version "1.2.3"', cask)
        self.assertIn('sha256 "' + "a" * 64 + '"', cask)
        self.assertIn('depends_on arch: :arm64', cask)

    def test_rejects_partial_release(self):
        self.release["assets"].pop()
        with self.assertRaises(ValueError):
            render(self.release, self.checksums)

    def test_rejects_bad_manifest(self):
        with self.assertRaises(ValueError):
            render(self.release, b"wrong checksum file")

    def test_rejects_mismatched_dmg(self):
        self.asset(DMG)["digest"] = "sha256:" + "b" * 64
        with self.assertRaises(ValueError):
            render(self.release, self.checksums)

    def test_rejects_unpublished_version(self):
        self.release["draft"] = True
        with self.assertRaises(ValueError):
            render(self.release, self.checksums)


if __name__ == "__main__":
    unittest.main()
