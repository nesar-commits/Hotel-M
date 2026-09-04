import Foundation

enum AuthState {
    case loading
    case loggedIn(UserOut)
    case loggedOut
}

@MainActor
final class AuthStore: ObservableObject {
    @Published private(set) var state: AuthState = .loading
    @Published var errorMessage: String?
    @Published private(set) var isSubmitting = false

    private let api = APIClient.shared
    private let tokenStore = TokenStore()

    var isLoggedIn: Bool {
        if case .loggedIn = state { return true }
        return false
    }

    init() {
        Task { await restoreSession() }
    }

    private func restoreSession() async {
        guard let token = tokenStore.read(), !token.isEmpty else {
            state = .loggedOut
            return
        }
        api.authToken = token
        do {
            state = .loggedIn(try await api.getMe())
        } catch {
            tokenStore.clear()
            api.authToken = nil
            state = .loggedOut
        }
    }

    func login(email: String, password: String) async -> Bool {
        isSubmitting = true
        errorMessage = nil
        defer { isSubmitting = false }
        do {
            let token = try await api.login(email: email, password: password)
            tokenStore.save(token.accessToken)
            api.authToken = token.accessToken
            state = .loggedIn(token.user)
            return true
        } catch {
            errorMessage = "Invalid email or password"
            return false
        }
    }

    func signup(name: String, email: String, password: String) async -> Bool {
        isSubmitting = true
        errorMessage = nil
        defer { isSubmitting = false }
        do {
            let token = try await api.signup(name: name, email: email, password: password)
            tokenStore.save(token.accessToken)
            api.authToken = token.accessToken
            state = .loggedIn(token.user)
            return true
        } catch let error as APIError {
            errorMessage = error.errorDescription
            return false
        } catch {
            errorMessage = "Signup failed"
            return false
        }
    }

    func logout() {
        tokenStore.clear()
        api.authToken = nil
        state = .loggedOut
    }
}
