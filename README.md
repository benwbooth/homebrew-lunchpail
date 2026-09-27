# Lunchpail for Homebrew

Install [Lunchpail](https://github.com/benwbooth/lunchpail), the retro game library
and emulator frontend, on an Apple Silicon Mac running macOS 13 or later.

```sh
brew install --cask benwbooth/lunchpail/lunchpail
```

To update:

```sh
brew update
brew upgrade --cask lunchpail
```

To uninstall the application without deleting your library settings:

```sh
brew uninstall --cask lunchpail
```

This tap installs the same DMG as the official
[Lunchpail releases](https://github.com/benwbooth/lunchpail/releases).
The current stable release predates the rename. Its original DMG is verified
unchanged and installed as `Lunchpail.app`; its UI adopts the new name in the
next release. New packages will use the new name throughout.
Intel Macs are not supported. The app is not notarized yet; follow macOS's
per-app security prompt if required, rather than disabling Gatekeeper.

The tap checks for new stable releases hourly. Maintainers can also run
**Actions → Update Lunchpail → Run workflow** to refresh it immediately.

For all other platforms, see the [installation instructions](https://github.com/benwbooth/lunchpail#install).
