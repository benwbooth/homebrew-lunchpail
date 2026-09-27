cask "lunchpail" do
  version "0.1.2"
  sha256 "8335d7672dd431c6c4c47e248e92ae57ac6a8f4ffe94487afe32c99803a14914"

  url "https://github.com/benwbooth/lunchpail/releases/download/v#{version}/Lunchbox-macos-arm64.dmg"
  name "Lunchpail"
  desc "Retro game library and emulator frontend"
  homepage "https://github.com/benwbooth/lunchpail"

  depends_on arch: :arm64
  depends_on macos: :ventura

  app "Lunchbox.app", target: "Lunchpail.app"

  zap trash: [
    "~/Library/Application Support/Lunchpail",
    "~/Library/Caches/Lunchpail",
    "~/Library/Preferences/io.github.benwbooth.Lunchpail.plist",
  ]
end
