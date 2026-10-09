"""Regression coverage for routing, packaged resources and evaluation completeness."""
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from tools.application_skills import ValidationError, bundle_data, load_library, load_profiles, match_skills, _skill

ROOT = Path(__file__).resolve().parents[1]

class RichSkillsTests(unittest.TestCase):
    def test_bundle_is_current_and_profiles_cover_every_skill(self) -> None:
        self.assertEqual((ROOT / 'PinDo/Resources/ApplicationSkills.json').read_text(encoding='utf-8'), bundle_data(ROOT))
        profiles = load_profiles(ROOT)
        skills, _ = load_library(ROOT)
        self.assertEqual({profile['id'] for profile in profiles}, {skill['application_id'] for skill in skills})

    def test_meeting_requests_keep_applications_and_workflows_distinct(self) -> None:
        skills, cases = load_library(ROOT)
        meeting_ids = {
            'zoom.meeting_setup': 'zoom.workplace',
            'zoom.breakout_rooms': 'zoom.workplace',
            'teams.meeting_scheduling': 'microsoft.teams',
            'teams.breakout_classrooms': 'microsoft.teams',
            'outlook.scheduling': 'microsoft.outlook',
        }
        for case in cases:
            if case['skill_id'] not in meeting_ids:
                continue
            with self.subTest(case=case['id']):
                self.assertEqual(match_skills(skills, case['application_id'], case['user_instruction']), [case['skill_id']])
        for app, expected in (
            ('zoom.workplace', ['zoom.breakout_rooms']),
            ('microsoft.teams', ['teams.breakout_classrooms']),
            ('microsoft.outlook', []),
        ):
            with self.subTest(app=app):
                self.assertEqual(match_skills(skills, app, 'Create breakout rooms'), expected)

    def test_every_documented_intent_routes_to_its_skill(self) -> None:
        skills, _ = load_library(ROOT)
        for skill in skills:
            for intent in skill['intents']:
                with self.subTest(skill=skill['id'], intent=intent):
                    self.assertIn(skill['id'], match_skills(skills, skill['application_id'], intent))

    def test_google_meeting_and_calendar_requests_route_by_application(self) -> None:
        skills, cases = load_library(ROOT)
        google_ids = {'meet.presentation_controls', 'meet.host_management',
                      'google_calendar.recurring_events', 'google_calendar.office_hours'}
        for case in cases:
            if case['skill_id'] not in google_ids:
                continue
            with self.subTest(case=case['id']):
                self.assertEqual(match_skills(skills, case['application_id'], case['user_instruction']), [case['skill_id']])
        for app, request in (
            ('google.meet', 'Create a recurring Calendar event'),
            ('google.meet', 'Create office hours with booking limits'),
            ('google.calendar', 'Share a tab and stop presenting'),
            ('google.calendar', 'Grant host controls to Alex'),
        ):
            with self.subTest(app=app, request=request):
                self.assertEqual(match_skills(skills, app, request), [])

    def test_google_workspace_data_requests_keep_applications_distinct(self) -> None:
        skills, cases = load_library(ROOT)
        task_apps = {
            'google_sheets.pivot_analysis': 'google.sheets',
            'google_forms.branching': 'google.forms',
            'gmail.labels_and_filters': 'google.gmail',
            'drive.sharing_permissions': 'google.drive',
        }
        for case in cases:
            if case['skill_id'] not in task_apps:
                continue
            with self.subTest(case=case['id']):
                self.assertEqual(match_skills(skills, case['application_id'], case['user_instruction']), [case['skill_id']])
        for app, request in (
            ('google.sheets', 'Analyze a pivot table'),
            ('google.forms', 'Configure answer based branching'),
            ('google.gmail', 'Apply a label filter'),
            ('google.drive', 'Review sharing permissions'),
        ):
            for other_app in set(task_apps.values()) - {app}:
                with self.subTest(app=other_app, request=request):
                    self.assertEqual(match_skills(skills, other_app, request), [])
        profiles = {p['id']: p for p in load_profiles(ROOT)}
        # Both editors use this host; the existing application picker must resolve it.
        self.assertEqual({p['id'] for p in profiles.values() if 'docs.google.com' in p['domains']}, {'google.sheets', 'google.forms'})
        self.assertEqual(profiles['google.gmail']['domains'], ['mail.google.com'])
        self.assertEqual(profiles['google.drive']['domains'], ['drive.google.com'])

    def test_study_requests_route_with_distinct_mac_surfaces(self) -> None:
        skills, cases = load_library(ROOT)
        task_apps = {'anki.deck_maintenance': ('anki.desktop', 'desktop'),
                     'classroom.rubric_builder': ('google.classroom', 'browser'),
                     'kahoot.assignments_and_reports': ('kahoot.web', 'browser')}
        for case in cases:
            if case['skill_id'] in task_apps:
                with self.subTest(case=case['id']):
                    self.assertEqual(match_skills(skills, case['application_id'], case['user_instruction']), [case['skill_id']])
                    for other_app, _ in set(task_apps.values()) - {task_apps[case['skill_id']]}:
                        self.assertEqual(match_skills(skills, other_app, case['user_instruction']), [])
        profiles = {p['id']: p for p in load_profiles(ROOT)}
        for task in skills:
            if task['id'] in task_apps:
                app, surface = task_apps[task['id']]
                self.assertEqual((task['application_id'], task['platform'], task['surface']), (app, 'macos', surface))
                self.assertEqual(profiles[app]['surface'], surface)
                self.assertEqual(profiles[app]['bundle_ids'], [])
        self.assertEqual(profiles['anki.desktop']['domains'], [])
        self.assertEqual(profiles['google.classroom']['domains'], ['classroom.google.com'])
        # The player join hostname must not identify a host assignment lesson.
        self.assertEqual(profiles['kahoot.web']['domains'], ['create.kahoot.it'])

    def test_matching_keeps_ambiguity_and_checks_application_and_word_boundaries(self) -> None:
        skills, _ = load_library(ROOT)
        sample = deepcopy(skills[0])
        sample['match_groups'] = [['mask'], ['layer', 'image']]
        alternate = deepcopy(sample)
        alternate['id'] = 'other.skill'
        self.assertEqual(match_skills([sample, alternate], sample['application_id'], 'mask the image'), sorted([sample['id'], alternate['id']]))
        self.assertEqual(match_skills([sample], sample['application_id'], 'unmask the image'), [])
        self.assertEqual(match_skills([sample], sample['application_id'], 'mask'), [])
        self.assertEqual(match_skills([sample], 'wrong.app', 'mask image'), [])

    def test_unsupported_verification_and_empty_search_terms_are_rejected(self) -> None:
        skills, _ = load_library(ROOT)
        for field in ('verification', 'match_groups'):
            skill = deepcopy(skills[0])
            if field == 'verification': skill['steps'][0]['verification'] = 'click'
            else: skill['match_groups'] = [['!!!']]
            with self.subTest(field=field), self.assertRaises(ValidationError):
                _skill(skill, 'fixture')

    def test_recovery_coverage_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder in ('skills', 'evaluations/cases'):
                shutil.copytree(ROOT / folder, root / folder)
            path = next((root / 'evaluations/cases').glob('*_recovery.json'))
            path.unlink()
            with self.assertRaisesRegex(ValidationError, 'English, Taglish and recovery'):
                load_library(root)

    def test_no_hands_on_claims_without_recorded_versions(self) -> None:
        skills, cases = load_library(ROOT)
        for item in skills + cases:
            if item['validation']['status'] != 'unverified':
                self.assertTrue(item.get('application_version') or item['validation'].get('tested_versions'))

    def test_audio_outcomes_require_confirmation(self) -> None:
        skills, _ = load_library(ROOT)
        for skill in skills:
            for step in skill['steps']:
                if any(word in step['objective'].lower() for word in ('listen', 'audition', 'against the audio')):
                    self.assertEqual(step['verification'], 'user_confirmation', skill['id'])

if __name__ == '__main__': unittest.main()
