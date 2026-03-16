#!/usr/bin/env python3
"""
Compatibility exports for HeroAgent scripts.
"""

from __future__ import annotations

from lib.shared_data import ACTION_CONTEXT_HINTS
from lib.shared_data import README_CONTENT
from lib.shared_data import REQUIRED_DIRS
from lib.shared_data import TEMPLATES_DIR
from lib.shared_data import TOP_LEVEL_SKIP_SEGMENTS
from lib.shared_data import WORKFLOW_STATE_CONTENT
from lib.shared_data import WORKSPACE_DIRNAME
from lib.shared_data import WIKI_CORE_FILES
from lib.shared_data import WIKI_STRATEGIES
from lib.workspace import blank_workflow_state
from lib.workspace import fill_named_fields
from lib.workspace import fill_next_step
from lib.workspace import init_workspace
from lib.workspace import load_workflow_state
from lib.workspace import read_template
from lib.workspace import render_blank_focus
from lib.workspace import render_template
from lib.workspace import safe_write
from lib.workspace import save_workflow_state
from lib.workspace import slugify
from lib.workspace import timestamp_now
from lib.workspace import touch_if_missing
from lib.workspace import write_if_missing
from lib.wiki_ops import append_wiki_sync_content
from lib.wiki_ops import assemble_wiki_context
from lib.wiki_ops import build_wiki_registry
from lib.wiki_ops import compact_wiki_content
from lib.wiki_ops import create_wiki_sync_drafts
from lib.wiki_ops import detect_module_target
from lib.wiki_ops import draft_filename_for_target
from lib.wiki_ops import draft_focus_points_for_target
from lib.wiki_ops import draft_target_from_text
from lib.wiki_ops import ensure_wiki_section_path
from lib.wiki_ops import extract_draft_merge_content
from lib.wiki_ops import extract_source_facts
from lib.wiki_ops import is_stale_file
from lib.wiki_ops import load_wiki_registry
from lib.wiki_ops import merge_fact_draft_into_target
from lib.wiki_ops import normalize_module_name
from lib.wiki_ops import parse_draft_mapping
from lib.wiki_ops import parse_maintenance_report
from lib.wiki_ops import refresh_wiki_registry
from lib.wiki_ops import refresh_workflow_wiki_state
from lib.wiki_ops import render_extracted_facts
from lib.wiki_ops import render_wiki_index
from lib.wiki_ops import render_wiki_maintenance_report
from lib.wiki_ops import render_wiki_sync_draft
from lib.wiki_ops import resolve_wiki_strategy
from lib.wiki_ops import score_wiki_document
from lib.wiki_ops import split_path_parts
from lib.wiki_ops import suggest_wiki_targets
from lib.wiki_ops import wiki_doc_kind
from lib.wiki_ops import wiki_doc_status
from lib.wiki_ops import wiki_doc_summary
from lib.wiki_ops import wiki_doc_topic
