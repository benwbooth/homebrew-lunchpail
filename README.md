# Lunchbox for Homebrew

Install [Lunchbox](https://github.com/benwbooth/lunchbox), the retro game library
and emulator frontend, on an Apple Silicon Mac running macOS 13 or later.

```sh
brew install --cask benwbooth/lunchbox/lunchbox
```

To update:

```sh
brew update
brew upgrade --cask lunchbox
```

To uninstall the application without deleting your library settings:

```sh
brew uninstall --cask lunchbox
```

This tap installs the same DMG as the official
[Lunchbox releases](https://github.com/benwbooth/lunchbox/releases).
Intel Macs are not supported. The app is not notarized yet; follow macOS's
per-app security prompt if required, rather than disabling Gatekeeper.

The tap checks for new stable releases hourly. Maintainers can also run
**Actions → Update Lunchbox → Run workflow** to refresh it immediately.

For all other platforms, see the [installation instructions](https://github.com/benwbooth/lunchbox#install).
