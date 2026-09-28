cask "lunchpail" do
  version "0.1.3"
  sha256 "b101bbd7603ed943869dc75e792867c20949b386126868b1c17ef7c364866a07"

  url "https://github.com/benwbooth/lunchpail/releases/download/v#{version}/Lunchpail-macos-arm64.dmg"
  name "Lunchpail"
  desc "Retro game library and emulator frontend"
  homepage "https://github.com/benwbooth/lunchpail"

  depends_on arch: :arm64
  depends_on macos: :ventura

  app "Lunchpail.app", target: "Lunchpail.app"

  zap trash: [
    "~/Library/Application Support/Lunchpail",
    "~/Library/Caches/Lunchpail",
    "~/Library/Preferences/io.github.benwbooth.Lunchpail.plist",
  ]
end
