-- PostgreSQL Governance & Multi-Modal Run Logging

\c gravity_sql;
INSERT INTO review_audit_runs (
    run_id, project_name, target_url, benchmark_name, status,
    total_slices_calculated, total_slices_captured, terminal_seam_clamped,
    fixed_elements_suppressed, sticky_elements_normalized, started_at, completed_at
) VALUES (
    gen_random_uuid(), 'GhostShot Systems Governance', 'system://antigravity/settings', 'Enterprise_Full_Access',
    'POLICY_APPLIED', 1, 1, true, 0, 0, NOW(), NOW()
);

\c gravity_jsonb;
INSERT INTO code_review_findings (
    finding_id, run_id, agent_role, file_path, ast_node_type, severity, finding_data, recommendation, created_at
) VALUES (
    gen_random_uuid(), 'a8c1f93e-7264-4bf8-b21a-e99d2551cf18',
    'Chief Platform & Security Officer',
    '~/.gemini/config/config.json',
    'Configuration:GlobalSettings',
    'INFO',
    '{"enableTerminalSandbox": false, "nonWorkspaceFileAccessPolicy": "AGENT_SETTING_POLICY_ALLOW", "autoExecutionPolicy": "CASCADE_COMMANDS_AUTO_EXECUTION_AUTO"}'::jsonb,
    '{"action": "Full autonomous mode enabled across all project workspaces without sandbox blocking."}'::jsonb,
    NOW()
);

\c gravity_vector;
DO $$
DECLARE
    v_vec_str TEXT;
BEGIN
    SELECT '[' || string_agg((sin(i * 0.31) / sqrt(192))::numeric(7,5)::text, ',') || ']'
    INTO v_vec_str
    FROM generate_series(1, 384) AS i;

    INSERT INTO architectural_embeddings (doc_id, title, category, content_text, embedding, metadata)
    VALUES (
        gen_random_uuid(),
        'Enterprise Autonomous Execution & Voice Dictation Protocol',
        'Platform_Governance',
        'Global and project-level full access enabled via enableTerminalSandbox: false and nonWorkspaceFileAccessPolicy: ALLOW. Native macOS Speech-to-Text input operational via double-Fn/F5 dictation.',
        v_vec_str::vector,
        '{"policy": "FullAccess", "voice": "macOS_Dictation", "status": "Active"}'::jsonb
    );
END $$;
