# Application skills and Teach mode

The app includes **114 macOS tasks across 18 application areas**, **345 task evaluation specifications**, and **15 shared runtime scenarios**. The extra Finder rename lesson separates renaming an existing item from creating a folder. All workflows remain **hands-on unverified**. Compilation and contract tests do not establish accuracy in a particular app version.

Windows can author and validate the data. Building or running the AppKit/SwiftUI application requires macOS. See [the Mac handoff](MAC_HANDOFF.md), [the catalogue](SKILL_CATALOGUE.md), and [the complete file inventory](CHANGED_FILES.md).

## Data flow

```text
skills/*.json + application_profiles.json
  -> Python validation and deterministic bundle
  -> PinDo/Resources/ApplicationSkills.json
  -> SkillLibrary decodes the bundled data
  -> Teach request + application identity -> matching tasks
  -> user selects a task and supplies required details
  -> TutorSession displays one step
  -> activity -> debounce -> window image + Accessibility controls
  -> local tutor returns instruction, status and evidence
  -> host checks session, step, observation revision and target
  -> advance one step, keep guiding, or pause
```

With Teach disabled, `QuickBarModel.send()` retains the existing `Agent.run()` action path. With Teach enabled, it starts `TutorSession`. The teaching client has no executable-action response and never calls the action executor. It uses the read-only Accessibility snapshot helper and labels menu capabilities as potentially closed, not visibility evidence.

`@Observable` makes session changes update SwiftUI. The main actor serializes UI state changes. Capture and network calls can suspend, but generation, step and observation counters must still match before a response can advance the lesson.

## Version 2 contract

The Python validator rejects unknown fields, duplicate JSON keys, duplicate IDs, broken references and unsupported verification methods. No schema dependency is needed. Version 1 remains readable for compatibility; runtime bundling requires version 2.

Skills retain `id`, `application_id`, `application`, `platform`, `title`, `intents`, `prerequisites`, ordered `steps`, `success_criteria`, `recovery`, `constraints`, `sources` and `validation`.

| Added field | Purpose |
| --- | --- |
| `surface` | Desktop or browser, separate from the macOS platform |
| `difficulty` | Foundation, intermediate or advanced |
| `concepts` | Named explanations of underlying ideas |
| `inputs` | Named questions answered before beginning |
| `requirements` | Version, access, account, plugin, network or media prerequisites |
| `match_groups` | Every group must match; any whole phrase within a group can satisfy it |
| `related_skills` | References to existing prerequisite or follow-up tasks |
| step `why` | Reason for this step |
| step `verification` | `visual` or `user_confirmation` |

Each step has an objective, semantic target (`role`, `semantic_name`) and expected results. There are no saved coordinates or executable command fields. Terminal commands are teaching text for the user to review and enter.

Profiles map internal application IDs to aliases, known bundle IDs and domains. Unknown bundle IDs are left empty. Browser matching checks exact domains or subdomains; a known website takes priority over its browser. Missing identity asks for application selection. Ambiguous task matches present choices; no match presents the application catalogue. Figma and Canva currently target their **web editors**, with their own account and network requirements. Zoom Workplace, Microsoft Teams and Microsoft Outlook have distinct desktop profiles for the five meeting/scheduling tasks. Their bundle IDs are unconfirmed and remain empty; desktop domains remain empty to avoid claiming browser workflow support. App selection and visible identity still require Mac testing.

## Watching and progression

- Watching begins only after the user starts the lesson. The panel stays visible during work in the target app.
- Accessibility notifications and global input activity schedule a **750 ms debounce**. Input events are discarded; no key text is retained.
- One capture/inference job runs at a time. Further activity invalidates the old response and schedules a fresh observation.
- ScreenCaptureKit captures the selected window at a maximum 1280-pixel longest edge. Images stay in memory and go only to the existing loopback runtime.
- Accepted image/text fingerprints suppress repeated inference on identical state.
- Only the current step, task details, prerequisites, up to three recovery entries and final criteria enter a request. Accessibility text is capped at 12,000 characters; request and answers at 1,500 and 3,000; serialized task context at 25,000 bytes. The whole catalogue is never sent.
- Automatic advancement requires `observed` and nonempty evidence for the current visual step. The trusted prompt requires every expected result. This remains a probabilistic visual judgment requiring Mac testing.
- Listening, subjective review, exported-file integrity and menu-open states outside the capture require **I checked this result**. Confirmation works while paused so the user can inspect an output elsewhere.
- Pause, Stop, closing the panel, target changes, permission failures, uncertainty and missing inputs prevent automatic progression. Resume takes a fresh observation. Details can be corrected while paused.
- Teach mode saves no screenshots, Accessibility dumps or prompts. Timing and token counts remain in session memory for recording by the tester.

Separate menus/popovers may be outside a window capture. Modal changes can pause a lesson; explicit Resume can adopt another window within the original app. Browser URL discovery uses the focused window's Accessibility document attribute; browser-title changes provide another signal. If neither distinguishes tabs, same-window tab changes cannot be reliably detected. Use an isolated practice window and record this limitation.

## Author and validate

```powershell
py -B tools/application_skills.py --bundle PinDo/Resources/ApplicationSkills.json
py -B tools/application_skills.py --check-bundle PinDo/Resources/ApplicationSkills.json
py -B -m unittest discover -s tests -v
```

Use `python3` on Mac. Edit the task JSON, add English, Taglish and recovery cases, then regenerate the resource. Bundle checking detects source changes not packaged into the app. Xcode's synchronized `PinDo` group includes new Swift files and the JSON resource automatically.

Cases specify starting state, request, expected next action, results and failure criteria. They are specifications, not executions. `evaluations/fixtures/setups.json` supplies concrete practice setups. `tools/practice_assets.py` creates original PNG, SVG, PDF, CSV, WAV and text assets in a new directory, refusing to overwrite an existing session. The three original evaluation IDs are preserved alongside the three-per-task cases. The desktop meeting batch adds 15 specifications and account-based Zoom, Teams and Outlook practice setups. Consenting participants, calendar availability and configured room resources must be prepared in the live services; static assets cannot supply them.

Python tests cover contracts, routing and packaging. The Swift executable tests the actual decoder, matching, domain boundaries, completion gate and stale-result predicate. GitHub also builds the native app and checks its packaged resource; it does not launch third-party applications.

Desktop meetings batch validation on 2026-10-10: generation and bundle checking passed for 114 tasks and 345 evaluation specifications; all 32 Python tests passed, including distinct meeting workflow routing. All 109 prior bundled tasks and 15 profiles were preserved exactly as data. Native Xcode/Swift checks and live Mac application execution were unavailable on the Linux authoring host. The existing `qwen3-vl:8b` runtime selection is unchanged.

## Evidence boundaries

Sources are official Microsoft, Zoom, Apple, Image-Line, Adobe, CapCut, Figma and Canva documentation reviewed on 2026-10-10. Each task records URLs and dates. Some pages cover a feature family rather than every recovery detail; recovery guidance is a conservative interpretation, still unverified. Documented applicability is distinct from actual tested versions.

All initial tested-version arrays are empty and case versions null. Mark verified only after a real run with exact versions and evidence. The Word citation reference applies specifically to Word 2019 for Mac; check newer layouts. CapCut build/region gates, Figma modes, Canva plan features, FL Studio editions/plugins and Adobe codecs require local confirmation.

No hands-on completion rate, grounding accuracy, baseline improvement or latency result is claimed. First validation targets are Office, CapCut, Figma web, Canva web and Photoshop. Other areas remain candidates for later testing. Record unsupported features as blocked for the tested version and leave the task unverified. Zoom scheduling requires a signed-in host or granted scheduling privilege; host/co-host roles manage breakout rooms and administrator locks remain read-only. Calendar integration is required for automatic Zoom invitation emails. Teams classrooms require the Mac desktop organizer or an explicitly delegated in-meeting room manager; presenter status alone is insufficient. Outlook Scheduling Assistant/Room Finder require a Microsoft 365/Exchange calendar, available free/busy information and access to configured organization room data. Unknown availability and pending/declined room responses cannot establish a booking. Menus, scheduling dialogs, invitation submission and cross-window participant/response checks use user confirmation.
