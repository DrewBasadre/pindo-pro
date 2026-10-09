# Mac continuation and validation

## Get and build

Continue on the local branch `qwen-skills-more` in `~/pindo-pro`. Retain previous batch commits and unrelated local work. This batch must remain local; do not fetch, pull, push, publish or deploy.

```bash
cd ~/pindo-pro
git rev-parse --show-toplevel
git status --short
git branch --show-current
git switch qwen-skills-more
python3 -B tools/application_skills.py --check-bundle PinDo/Resources/ApplicationSkills.json
python3 -B -m unittest discover -s tests -v
```

If this local branch is absent, inspect the working tree/index and create it from current local HEAD with `git switch -c qwen-skills-more`. Stop if switching would disturb unrelated work; do not reset or rewrite earlier commits.

Requirements: macOS 15+, Xcode 26, and the existing local runtime configured according to the README. Teach requires image input and structured responses. No cloud service is added.

```bash
DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcodebuild \
  -project PinDo.xcodeproj -scheme PinDo -derivedDataPath build build
open build/Build/Products/Debug/PinDo.app
```

Allow **Accessibility** and **Screen Recording** for PinDo in System Settings → Privacy & Security. A permission change or ad-hoc rebuild may require reopening the app and renewing the grant. CI's unsigned build establishes compilation; build locally for interactive testing.

## First focused test

```bash
python3 -B tools/practice_assets.py
```

This creates `build/practice-assets`. Use another `--output` directory for a fresh session; existing directories are not overwritten. The eight assets are original synthetic fixtures. The WAV contains tones, not speech. Record permitted spoken counting for caption tests as described in the fixture setups.

1. Open Finder at the disposable practice directory.
2. Press Fn+Space, enable **Teach**, and enter `Paano gumawa ng folder na Lesson Files?`.
3. Confirm the app/task if prompted, provide the parent directory and name, and choose **Requirements met — begin**.
4. Follow one instruction at a time. The panel should stay visible. Inspect **Why this step?** and **What to check**.
5. Confirm the new folder's name and parent. Clicking New Folder alone is insufficient evidence.
6. Repeat while switching windows and stopping during a response. No late response should advance a paused or stopped lesson.

## Available-app validation

Record exact macOS version, application build, browser, account plan, language and hardware. Use the relevant subset of `evaluations/fixtures/setups.json`.

| App | Start here | Then test |
| --- | --- | --- |
| PowerPoint | `powerpoint.insert_image` | slide masters and PDF output |
| Excel | `excel.totals_averages` | PivotTables and Mac CSV import |
| Word | `word.headings` | section numbering and citation layout |
| CapCut Mac | `capcut.import_trim` | captions, tracked blur and export gates |
| Figma web | `figma.nested_auto_layout` | interactive states and variable modes |
| Canva web | `canva.frames_crop` | video timing and accessible PDF output |
| Photoshop Mac | `photoshop.layer_mask` | Smart Filters, edge refinement and export |
| Zoom Workplace Mac | `zoom.meeting_setup` | `zoom.breakout_rooms`, administrator locks, host/co-host vs participant controls |
| Teams Mac | `teams.meeting_scheduling` | `teams.breakout_classrooms`, organizer/manager permissions and automatic/manual assignment |
| Outlook Mac | `outlook.scheduling` | availability, Room Finder account/directory access and attendee/room responses |
| Google Meet on Mac browser | `meet.presentation_controls` | `meet.host_management`, tab/window/display boundaries, Mac grants, role/edition limits and leave versus end |
| Google Sheets on Mac browser | `google_sheets.pivot_analysis` | source boundaries, Rows/Columns/Values/Filters, aggregation versus Show as, independently checked totals |
| Google Forms on Mac browser | `google_forms.branching` | supported question types, answer destinations, section exits and every alternative preview path |
| Gmail on Mac browser | `gmail.labels_and_filters` | advanced-search preview, exclusions, labels, automatic actions and retroactive scope |
| Google Drive on Mac browser | `drive.sharing_permissions` | direct versus inherited roles, General access, disabled changes and parent/sibling impacts |
| Anki Mac desktop | `anki.deck_maintenance` | note/card modes, tags, scoped filters, sibling deck placement and duplicate candidate review |
| Google Classroom on Mac browser | `classroom.rubric_builder` | teacher/student controls, scoring/order, ungraded edit availability and saved attachment |
| Kahoot! creator on Mac browser | `kahoot.assignments_and_reports` | deadline/zone, plan gates, consenting sharing, assigned-session reports and source-edit boundary |
| Google Calendar on Mac browser | `google_calendar.recurring_events` | `google_calendar.office_hours`, occurrence/series scope, appointment eligibility, availability, booking windows, buffers and daily cap |

For meeting practice use consenting test accounts and organization-approved room resources from `setups.json`. Record Zoom calendar integration and policy locks, Teams calendar mode/Exchange access/organizer role, and Outlook account type/free-busy/room-directory access. Verify invitee identities, time zones, actual transfers, room booking responses and invitation submission with the user when outside the pinned capture. Unknown availability is not free and a pending room is not reserved. No extra raster/media assets or plugin are needed for these five tasks.

For Google practice use the `meet` and `google_calendar` setups. Record both exact browser builds and service account editions; verify the focused service domain even when a Calendar event opens a Meet call. PinDo Screen Recording permission does not grant Chrome screen-sharing access. Confirm Mac sharing pickers/permission prompts, remote content/audio, co-host access and participant exit outcomes manually. Repeat sharing for each boundary, and leave/end in separate consenting calls. For recurring edits compare an earlier, selected and later occurrence for each supported scope. Review saved appointment rules and booking-page preview without a real booking; use separate consenting runs for busy conflicts and actual buffer/cap enforcement or invitation delivery. Required unavailable features are blocked for that account. No new plugin or static asset is required.

For Google Workspace administration/data use `google_sheets`, `google_forms`, `gmail` and `drive` setups. Record exact Mac/browser versions, editor language, account access and policy. On shared `docs.google.com`, PinDo asks for Sheets versus Forms: confirm the visible editor, not just the host, before selecting or resuming. The matcher cannot distinguish Docs/Slides or same-host editor paths. Compare pivot source boundaries, numeric types and SUM/filter subtotals with the synthetic records. Preview both Forms paths through the intended final section, stopping before Submit; leave a path blocked if preview restrictions prevent navigation. Search Gmail matches and exclusions before either Create filter action; inspect the saved rule and retroactive changes, with future-arrival checks in separate consenting runs. Compare Drive child/parent/sibling grants and manually test effective recipient access. Do not change parent grants to force a child downgrade, enable public link access, publish forms or send mail. No new media assets or plugin are required.

Run each task's English, Taglish and recovery cases. Begin with one lesson per app. Generated guidance can follow the request language; stored objectives/explanations currently provide an English fallback. Test language quality rather than assuming intent matching proves translation quality.

Run the shared scenarios in `evaluations/runtime_cases.json`. Some require a controlled local response; there is no automatic live-app test driver. A predicate unit test does not establish that a live runtime scenario passed.

For study/classroom practice use `anki`, `classroom` and `kahoot` setups. Record actual Mac/app or browser versions, roles and plan/policy. Keep Anki local without sync; compare note identity before calling similar cards duplicates and verify moved/untouched siblings. Use an ungraded titled Classroom draft, configure fields one at a time and review the saved rubric without posting. Kahoot creation is immediately available; review test audience before sharing and manually verify submission and learner access. Match reports by session/deadline, not source title alone; quiz edits do not update previous assignments. Test missing controls, student/player views and plan gates as separate recovery cases.

## Record evidence

Copy `evaluations/run_template.json` into a local results directory for each real run. Use null for unavailable metrics and explain why. Do not commit screenshots of personal documents.

- Record actual controls, expected-result evidence, failed steps, permissions and UI differences.
- **Response timing** reports observation-to-response latency and returned token counts. It excludes debounce and time before observation starts; measure request-to-usable-guidance separately.
- Separate cold and warm runs. Report sample count, median and P95. Performance targets remain hypotheses until measured.
- Compare baseline teaching without a task reference against teaching with the bounded reference using the same synthetic observation, instruction and runtime configuration. The existing action mode is not a comparable tutoring baseline. A controlled replay harness is still needed for this experiment; do not claim improvement from unrelated runs.
- Update `tested_versions`, case `application_version` and validation notes only after real evidence. Preserve failures and blocked-version results.

## Read the implementation

1. `skills/finder/create_folder.json` defines inputs, steps and evidence.
2. `tools/application_skills.py` validates and bundles the data.
3. `PinDo/SkillLibrary.swift` decodes, matches and supplies progression predicates.
4. `PinDo/QuickBar.swift` selects Teach or the existing action path.
5. `PinDo/TutorSession.swift` owns the step, pause/resume and stale-result rejection.
6. `PinDo/TutorObservation.swift` captures the pinned window and receives activity notifications.
7. `PinDo/TutorClient.swift` sends bounded context and parses non-executable guidance.
8. `PinDo/TutorView.swift` shows requirements, explanations and controls.

Task files describe procedures; they are not macros. The host owns progression while inference supplies guidance and evidence. Preserve this separation while continuing development.

## Known limits to investigate

- Study and classroom activities batch validation on 2026-10-10: generation and bundle checking passed for 125 tasks and 378 specifications; all 35 Python tests passed, including English/Taglish/recovery routing and distinct Mac surfaces. All 122 prior tasks, 24 profiles and 369 cases are retained unchanged as data. Swift Classroom/creator-versus-player domain checks were added but not executed on this Linux host. Native Xcode/Swift checks and live Mac Anki/Classroom/Kahoot execution are unavailable; all three tasks remain unverified with empty tested-version arrays. The existing `qwen3-vl:8b` selection is unchanged.

- Single-window capture may exclude menus; menu availability is not proof of an open menu. Affected seed steps require confirmation.
- Modal windows pause watching; Resume can adopt a window in the same app. Return from an external viewer before further visual checks, or confirm a designated manual-review step while paused.
- Domain detection depends on Accessibility metadata. Same-title tabs without exposed URLs are not reliably distinguishable.
- Figma tasks target the web editor; native Figma needs separate surface validation.
- Creative canvases and audio have limited Accessibility representation. Visual judgments remain unverified; listening and subjective checks require the user.
- Watching reacts to input and supported Accessibility notifications, not continuous video. A background render with no notification may require fresh user activity.
- Recovery cases check the next guidance and pause behavior; full end-to-end workflows require manual runs.
- The Google Workspace administration/data batch was authored on Linux. Generation/check-bundle validated 122 tasks and 369 cases; all 34 Python tests passed. Swift shared-host/domain checks, Xcode builds and live Mac browser execution were unavailable. Pivot integrity, all preview paths, future-mail behavior and effective/inherited sharing need real Mac evidence; new tasks are unverified with empty tested versions.
- The Google meetings/calendar batch was authored on Linux. Generation/check-bundle validated 118 tasks and 357 cases; all 33 Python tests passed. New Swift Google domain checks, native app builds and live Mac browser workflows could not run here. Account/role eligibility, Mac sharing dialogs, recurrence integrity and appointment rule enforcement still need live evidence.
- The desktop meetings batch was authored on Linux. Native Xcode/Swift checks and live Zoom/Teams/Outlook GUI execution are unavailable here; all tested-version arrays remain empty and cases retain null versions. Portable schema/routing validation cannot establish Mac GUI correctness.

See [CHANGED_FILES.md](CHANGED_FILES.md) for every created/modified file and its purpose. No project redesign or dependency migration is included.
