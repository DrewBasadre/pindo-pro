import Foundation

@main
struct SkillLibraryTests {
    static func main() throws {
        let library = try SkillLibrary.decode(Data(contentsOf: URL(fileURLWithPath: CommandLine.arguments[1])))
        for skill in library.skills {
            for intent in skill.intents {
                precondition(library.candidates(applicationID: skill.application_id, instruction: intent).contains { $0.id == skill.id }, "Unmatched intent: \(skill.id): \(intent)")
            }
            for step in skill.steps {
                precondition(!TeachingProgress.canAdvance(step: step, status: "not_yet", evidence: "A click occurred", userConfirmed: false))
                precondition(!TeachingProgress.canAdvance(step: step, status: "observed", evidence: "  ", userConfirmed: false))
                precondition(TeachingProgress.canAdvance(step: step, status: "observed", evidence: "Visible result", userConfirmed: false) == (step.verification == "visual"))
                precondition(TeachingProgress.canAdvance(step: step, status: "uncertain", evidence: "", userConfirmed: true) == (step.verification == "user_confirmation"))
            }
        }
        precondition(library.candidates(applicationID: "unknown.app", instruction: "insert image").isEmpty)
        let profile = ApplicationProfile(id: "test.browser", name: "Example", aliases: ["Example"], bundle_ids: [], domains: ["example.com"], surface: "browser", terminology: ["page"])
        precondition(profile.matches(name: "Safari", bundleID: nil, host: "www.example.com"))
        precondition(!profile.matches(name: "Safari", bundleID: nil, host: "example.com.evil.test"))
        precondition(!profile.matches(name: "Example", bundleID: nil, host: nil))
        for (applicationID, domain, otherDomain) in [
            ("google.meet", "meet.google.com", "calendar.google.com"),
            ("google.calendar", "calendar.google.com", "meet.google.com"),
            ("google.sheets", "sheets.google.com", "forms.google.com"),
            ("google.forms", "forms.google.com", "sheets.google.com"),
            ("google.gmail", "mail.google.com", "drive.google.com"),
            ("google.drive", "drive.google.com", "mail.google.com"),
            ("google.classroom", "classroom.google.com", "docs.google.com"),
            ("kahoot.web", "create.kahoot.it", "kahoot.it"),
            ("overleaf.web", "www.overleaf.com", "docs.google.com")
        ] {
            let googleProfile = library.applications.first { $0.id == applicationID }!
            precondition(googleProfile.matches(name: "Google Chrome", bundleID: nil, host: domain))
            precondition(!googleProfile.matches(name: "Google Chrome", bundleID: nil, host: otherDomain))
            precondition(!googleProfile.matches(name: "Safari", bundleID: nil, host: domain + ".evil.test"))
            precondition(!googleProfile.matches(name: googleProfile.name, bundleID: nil, host: nil))
        }
        let sharedEditorProfiles = library.applications.filter {
            $0.matches(name: "Safari", bundleID: nil, host: "docs.google.com")
        }
        precondition(Set(sharedEditorProfiles.map(\.id)) == Set(["google.sheets", "google.forms"]))
        // A shared host requires explicit app selection, never array-order selection.
        precondition(sharedEditorProfiles.count != 1)
        for changed in 0..<7 {
            let accepted = TeachingProgress.isCurrent(session: 1, currentSession: changed == 1 ? 2 : 1,
                step: 2, currentStep: changed == 2 ? 3 : 2, observation: 3, currentObservation: changed == 3 ? 4 : 3,
                paused: changed == 4, sameTarget: changed != 5)
            precondition(accepted == (changed == 0 || changed == 6), "Stale or paused observation was accepted")
        }
        print("Swift matching, application identity, and completion gates passed for \(library.skills.count) skills.")
    }
}
