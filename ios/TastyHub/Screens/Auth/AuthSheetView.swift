import SwiftUI

/// Combines login and signup into one sheet (toggled with `isSignup`) rather than the Android
/// app's two separate pushed screens — a modal is the more idiomatic iOS pattern for an auth gate
/// reached from several different tabs.
struct AuthSheetView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject private var authStore: AuthStore
    @State private var isSignup = false
    @State private var name = ""
    @State private var email = ""
    @State private var password = ""

    var body: some View {
        NavigationStack {
            VStack(spacing: 16) {
                Text(isSignup ? "Create account" : "Welcome back")
                    .font(.title2).fontWeight(.bold)
                    .frame(maxWidth: .infinity, alignment: .leading)

                if isSignup {
                    TextField("Name", text: $name)
                        .textFieldStyle(.roundedBorder)
                }
                TextField("Email", text: $email)
                    .textFieldStyle(.roundedBorder)
                    .textInputAutocapitalization(.never)
                    .keyboardType(.emailAddress)
                SecureField("Password", text: $password)
                    .textFieldStyle(.roundedBorder)

                if let error = authStore.errorMessage {
                    Text(error).foregroundStyle(.red).font(.caption)
                }

                Button {
                    submit()
                } label: {
                    if authStore.isSubmitting {
                        ProgressView().tint(.white)
                    } else {
                        Text(isSignup ? "Sign Up" : "Log In").frame(maxWidth: .infinity)
                    }
                }
                .buttonStyle(.borderedProminent)
                .disabled(!isValid || authStore.isSubmitting)

                Button(isSignup ? "Already have an account? Log in" : "Don't have an account? Sign up") {
                    isSignup.toggle()
                    authStore.errorMessage = nil
                }
                .font(.footnote)

                Spacer()
            }
            .padding()
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
            }
        }
    }

    private var isValid: Bool {
        !email.isEmpty && !password.isEmpty && (!isSignup || !name.isEmpty)
    }

    private func submit() {
        Task {
            let success = isSignup
                ? await authStore.signup(name: name, email: email, password: password)
                : await authStore.login(email: email, password: password)
            if success { dismiss() }
        }
    }
}
