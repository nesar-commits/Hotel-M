import Foundation

enum AppConfig {
    // The iOS Simulator shares the host Mac's network stack, so 127.0.0.1 reaches a backend
    // running locally with no special alias (unlike the Android emulator's 10.0.2.2). For a
    // physical device, point this at your machine's LAN IP and add an ATS exception for it
    // (see ios/README.md) since it won't be loopback traffic anymore.
    static let apiBaseURL = URL(string: "http://127.0.0.1:8000")!
}
