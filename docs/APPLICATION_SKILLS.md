# Application skills and Teach mode

The app includes **132 macOS tasks across 32 application areas**, **399 task evaluation specifications**, and **15 shared runtime scenarios**. The extra Finder rename lesson separates renaming an existing item from creating a folder. All workflows remain **hands-on unverified**. Compilation and contract tests do not establish accuracy in a particular app version.

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

Profiles map internal application IDs to aliases, known bundle IDs and domains. Unknown bundle IDs are left empty. Browser matching checks exact domains or subdomains; a known website takes priority over its browser. Missing identity asks for application selection. Ambiguous task matches present choices; no match presents the application catalogue. Figma and Canva currently target their **web editors**, with their own account and network requirements. Zoom Workplace, Microsoft Teams and Microsoft Outlook have distinct desktop profiles for the five meeting/scheduling tasks. Their bundle IDs are unconfirmed and remain empty; desktop domains remain empty to avoid claiming browser workflow support. Google Meet and Google Calendar have distinct browser profiles, exact service domains (`meet.google.com` and `calendar.google.com`) and empty bundle IDs. Calendar events can link to Meet, but their recurrence/booking controls belong to Calendar. App selection and visible identity still require Mac testing. Sheets, Forms, Gmail and Drive now have distinct browser profiles (`google.sheets`, `google.forms`, `google.gmail`, `google.drive`) and empty bundle IDs. Sheets/Forms include their service entry domains and shared `docs.google.com`; the current hostname matcher intentionally returns both profiles on that shared host, so the existing application picker asks for selection. It does not identify `/spreadsheets` versus `/forms` paths or distinguish Docs/Slides there. Confirm the visible editor and use an isolated window; host matching and Resume alone cannot establish editor identity. Gmail and Drive match `mail.google.com` and `drive.google.com` separately. Study/classroom profiles add Anki desktop (no domains), Classroom browser (`classroom.google.com`) and Kahoot creator browser (`create.kahoot.it`); unknown bundle IDs remain empty. Kahoot player `kahoot.it` is not a host workflow, and Google Classroom is distinct from Apple Classroom.

Acrobat adds a desktop `adobe.acrobat` profile with no domains, while Overleaf adds browser `overleaf.web` on `overleaf.com`; both have unknown bundle IDs left empty. Word integration reuses the existing Word profile.

The productivity/content batch chooses **browser on Mac** for both Notion and Slack after inspecting the profile contract: one profile has exactly one `surface`, and bundled task surfaces must match it. No desktop profile/instructions are mixed into these lessons. Notion uses `notion.com`/`notion.so`, Slack uses `app.slack.com`, and Trello uses `trello.com`; all new bundle-ID arrays remain empty. Canva reuses `canva.web` unchanged. Host matching identifies a service, not its signed-in editor, plan or permissions: confirm the visible database/editor/workspace and use an isolated browser window. Slack workspace URL redirects require identity review; unsupported hosts use manual app selection, not an invented domain alias.

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

The Zotero lesson starts in Word under the existing `microsoft.word` profile. `TutorSession.activity()` pauses on target changes; `resume()` requires the original PID, so it cannot transfer watching to Zotero or a Zotero-owned plugin dialog. Library organization and plugin dialogs are manual `user_confirmation` steps while paused. Use **I checked this result** after each manual action; bring the original Word document forward before **Resume watching**. Same-process Word dialogs/windows can be adopted by explicit Resume; restarting Word changes the PID and needs a new lesson. Generic Zotero citation wording also matches the retained built-in `word.citations` lesson; choose the explicitly titled Zotero task in the picker. No Zotero app alias/profile is added because automatic Zotero-window watching is not supported by this Word-anchored lesson.

## Author and validate

```powershell
py -B tools/application_skills.py --bundle PinDo/Resources/ApplicationSkills.json
py -B tools/application_skills.py --check-bundle PinDo/Resources/ApplicationSkills.json
py -B -m unittest discover -s tests -v
```

Use `python3` on Mac. Edit the task JSON, add English, Taglish and recovery cases, then regenerate the resource. Bundle checking detects source changes not packaged into the app. Xcode's synchronized `PinDo` group includes new Swift files and the JSON resource automatically.

The study/classroom batch adds nine specifications and three manually prepared synthetic setups in `setups.json`; no new static media assets are required. Anki uses a local writable practice collection, Classroom an authorized teacher and ungraded draft, and Kahoot a permitted host with plan-available assignment controls and consenting test sharing destination.

The research/document batch adds nine specifications and three manual synthetic setups (`zotero_word`, `acrobat`, `overleaf`). Zotero needs the bundled Mac Word plugin and its separate Automation permission. Acrobat requires an active Pro form-authoring entitlement and unsigned editable PDF; Reader/Fill & Sign are not authoring substitutes. Overleaf needs a signed-in editor in a supported Mac browser; generated auxiliary files are traced to editable sources. No new static media assets or external uploads are part of this batch.

The productivity/content batch adds 12 evaluation specifications and four manual synthetic setups (`notion`, `canva_bulk`, `slack`, `trello`); no new static assets are needed. Notion distinguishes data sources/views and requires schema access beyond Can edit content, then checks exact related pages and an independently computed rollup. Canva Bulk Create is distinct from manual multipage/branding lessons and requires an eligible plan, explicit column-to-element mapping, previews and complete generated-record review. Slack requires a paid plan, permitted builder/manager role and channel posting access; choose request/event versus scheduled recurrence, order steps and pass actual variables. Draft-only is supported; publishing/testing is user-scoped live service activity. Trello compares Rules, Card buttons, Board buttons, Scheduled and Due Date commands, shared Workspace quotas, private button visibility and account time zones. Save activates automation; Run now does not prove future timing. Neither authoring nor evaluation specifications execute service actions.

Cases specify starting state, request, expected next action, results and failure criteria. They are specifications, not executions. `evaluations/fixtures/setups.json` supplies concrete practice setups. `tools/practice_assets.py` creates original PNG, SVG, PDF, CSV, WAV and text assets in a new directory, refusing to overwrite an existing session. The three original evaluation IDs are preserved alongside the three-per-task cases. The desktop meeting batch adds 15 specifications and account-based Zoom, Teams and Outlook practice setups. The Google meetings/calendar batch adds 12 specifications and two browser/account practice setups for tab/window/display sharing, host restrictions and eligible co-hosts, recurring edit scopes, and office-hours rules. Consenting participants, calendar availability, account entitlements and configured room resources must be prepared in the live services; static assets cannot supply them. No new media assets are needed. The Google Workspace administration/data batch adds 12 specifications and four concrete setups for Sheets source boundaries and totals, Forms alternative paths, Gmail matching/nonmatching messages and Drive child/parent/sibling grants. These synthetic data and account-based setups are in `setups.json`; they require manual service preparation, with no new media assets. Review changes using practice content; do not publish forms or send messages during these lessons.

Python tests cover contracts, routing and packaging. The Swift executable tests the actual decoder, matching, domain boundaries, completion gate and stale-result predicate. GitHub also builds the native app and checks its packaged resource; it does not launch third-party applications.

Desktop meetings batch validation on 2026-10-10: generation and bundle checking passed for 114 tasks and 345 evaluation specifications; all 32 Python tests passed, including distinct meeting workflow routing. All 109 prior bundled tasks and 15 profiles were preserved exactly as data. Native Xcode/Swift checks and live Mac application execution were unavailable on the Linux authoring host. The existing `qwen3-vl:8b` runtime selection is unchanged.

Google meetings/calendar batch validation on 2026-10-10: generation and bundle checking passed for 118 tasks and 357 evaluation specifications; all 33 Python tests passed, including English/Taglish/recovery routing and separation of Meet from Calendar. All 114 prior tasks and 18 profiles are preserved exactly as data. Swift domain-boundary checks were added for both Google profiles but not executed on this Linux host; native Xcode/Swift checks and live Mac browser execution are unavailable. The existing `qwen3-vl:8b` model selection is unchanged.

Google Workspace administration/data batch validation on 2026-10-10: generation and bundle checking passed for 122 tasks and 369 specifications; all 34 Python tests passed, including the new four-application routing coverage. All 118 previous tasks, 20 profiles and 357 cases are retained unchanged as data. Shared-host ambiguity uses existing application selection; Swift domain/ambiguity checks were added but cannot run on this Linux host. Native Xcode/Swift checks and live Mac browser workflows are unavailable; all four tasks remain unverified with empty tested-version arrays. The existing `qwen3-vl:8b` runtime selection is unchanged.

Study and classroom activities batch validation on 2026-10-10: generation and bundle checking passed for 125 tasks and 378 specifications; all 35 Python tests passed, including English/Taglish/recovery routing and distinct Mac surfaces. All 122 prior tasks, 24 profiles and 369 cases are retained unchanged as data. Swift Classroom/creator-versus-player domain checks were added but not executed on this Linux host. Native Xcode/Swift checks and live Mac Anki/Classroom/Kahoot execution are unavailable; all three tasks remain unverified with empty tested-version arrays. The existing `qwen3-vl:8b` selection is unchanged.

Research and document preparation batch validation on 2026-10-10: generation and bundle checking passed for 128 tasks and 387 specifications; all 36 Python tests passed, including Mac surfaces, English/Taglish/recovery routing, preserved built-in citation choices and manual observation boundaries. All 125 prior tasks, 27 profiles and 378 cases are retained unchanged as data. Word uses its existing profile; Acrobat desktop and Overleaf browser add two profiles, with unknown bundle IDs empty. Swift Overleaf domain checks were added but not executed on this Linux host. Native Xcode/Swift checks and live Mac workflows are unavailable; all three tasks remain unverified with empty tested-version arrays. The existing `qwen3-vl:8b` selection is unchanged.

Productivity and content workflows batch validation on 2026-10-10: generation and bundle checking passed for 132 tasks and 399 specifications; all 37 Python tests passed, including English/Taglish/recovery routing, distinct Bulk Create intents, Mac browser surfaces and confirmation boundaries. All 128 prior tasks, 29 profiles and 387 cases are retained unchanged as data. Canva reuses its existing web profile; Notion, Slack and Trello add browser profiles with unknown bundle IDs empty. Swift domain checks were added but not executed on this Linux host. Native Xcode/Swift checks and live Mac workflows are unavailable; all four tasks remain unverified with empty tested-version arrays. The existing `qwen3-vl:8b` selection is unchanged.

## Evidence boundaries

Sources are official Microsoft, Zoom, Apple, Google, Image-Line, Adobe, CapCut, Figma, Canva, Anki, Kahoot, Zotero, Overleaf, Notion, Slack and Atlassian documentation reviewed on 2026-10-10. Each task records URLs and dates. Some pages cover a feature family rather than every recovery detail; recovery guidance is a conservative interpretation, still unverified. Documented applicability is distinct from actual tested versions.

All initial tested-version arrays are empty and case versions null. Mark verified only after a real run with exact versions and evidence. The built-in `word.citations` reference applies specifically to Word 2019 for Mac; the separate Zotero integration documents Word for Mac 2016–2024/Microsoft 365. Check the installed layouts. CapCut build/region gates, Figma modes, Canva plan features, FL Studio editions/plugins and Adobe codecs require local confirmation.

No hands-on completion rate, grounding accuracy, baseline improvement or latency result is claimed. First validation targets are Office, CapCut, Figma web, Canva web and Photoshop. Other areas remain candidates for later testing. Record unsupported features as blocked for the tested version and leave the task unverified. Zoom scheduling requires a signed-in host or granted scheduling privilege; host/co-host roles manage breakout rooms and administrator locks remain read-only. Calendar integration is required for automatic Zoom invitation emails. Teams classrooms require the Mac desktop organizer or an explicitly delegated in-meeting room manager; presenter status alone is insufficient. Outlook Scheduling Assistant/Room Finder require a Microsoft 365/Exchange calendar, available free/busy information and access to configured organization room data. Unknown availability and pending/declined room responses cannot establish a booking. Menus, scheduling dialogs, invitation submission and cross-window participant/response checks use user confirmation. Meet sharing distinguishes tab, window and whole display; browser screen-recording grants are separate from PinDo permissions and Mac pickers/Allow prompts may be outside the capture. Host management and co-host promotion depend on role, edition and main-room status; leaving alone differs from ending for all. Calendar series edits require explicit scope and comparison of affected/unaffected dates. Appointment schedules require an eligible account (personal/Business Starter: one page; Frontline/Essentials/unsupported legacy plans: unavailable); premium features vary. Availability, notice windows, buffer and daily cap are checked where enabled. Required unavailable settings pause the lesson, and previews do not establish booking enforcement or delivery. Sheets requires native editor access, header-inclusive source ranges, explicit aggregation/display settings and manual source-total comparisons; a saved value filter may exclude new categories. Forms answer navigation supports Multiple choice/Dropdown only and needs per-answer destinations plus section exits; preview every path without publishing/submitting, and report blocked preview navigation honestly. Gmail requires Search preview before creating a filter, exact label/action review and an explicit retroactive scope; thread display does not establish that all replies match, and deleting a rule does not undo prior actions. Drive My Drive file roles differ from shared-drive membership. Child grants cannot reduce higher inherited folder access; Restricted general access does not revoke parent/group grants. Inspect parent and sibling impacts without altering folder permissions. Organization policy and permitted-editor authority may disable sharing. Recipient-side effective access, new-mail behavior and all off-screen dialogs remain manual/unverified.

Anki tags belong to notes and decks hold cards; Notes-mode card operations may include sibling cards. Duplicate field matches are candidates for manual review, not deletion instructions. Classroom manual rubrics need a titled ungraded assignment and teacher controls; scoring/level sorting and saved attachment review do not prove publication or grading. Kahoot deadline/optional features depend on plan; creation makes the assignment available immediately. Review audience before sharing and verify submission/recipient access manually. Existing assignments retain earlier quiz content, so later source edits require a newly created session and newly shared access details. Empty reports do not establish learner completion.
