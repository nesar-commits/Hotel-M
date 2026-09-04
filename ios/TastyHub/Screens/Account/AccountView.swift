import SwiftUI

struct AccountView: View {
    let onLoginClick: () -> Void
    @EnvironmentObject private var authStore: AuthStore

    var body: some View {
        VStack(spacing: 16) {
            switch authStore.state {
            case .loading:
                ProgressView()
            case .loggedIn(let user):
                Text(user.name).font(.title2).fontWeight(.bold)
                Text(user.email).foregroundStyle(.secondary)
                Button("Log Out", role: .destructive) { authStore.logout() }
                    .buttonStyle(.bordered)
            case .loggedOut:
                Text("You're not logged in")
                Button("Log In / Sign Up", action: onLoginClick)
                    .buttonStyle(.borderedProminent)
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .navigationTitle("Account")
    }
}
