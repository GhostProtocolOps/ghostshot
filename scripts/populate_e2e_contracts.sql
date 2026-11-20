-- PostgreSQL E2E Framework & Component Contracts Persistence

\c gravity_sql;
INSERT INTO review_audit_runs (
    run_id, project_name, target_url, benchmark_name, status,
    total_slices_calculated, total_slices_captured, terminal_seam_clamped,
    fixed_elements_suppressed, sticky_elements_normalized, started_at, completed_at
) VALUES (
    gen_random_uuid(), 'GhostShot E2E Test Suite', 'system://playwright/benchmarks', 'Playwright_Extension_Harness',
    'FRAMEWORK_ACTIVE', 4, 4, true, 2, 1, NOW(), NOW()
);

\c gravity_jsonb;
INSERT INTO code_review_findings (
    finding_id, run_id, agent_role, file_path, ast_node_type, severity, finding_data, recommendation, created_at
) VALUES (
    gen_random_uuid(), 'a8c1f93e-7264-4bf8-b21a-e99d2551cf18',
    'Lead QA & Automation Engineer',
    'tests/e2e/capture_benchmarks.spec.ts',
    'PlaywrightSuite:CaptureBenchmarks',
    'INFO',
    '{"benchmarks": ["W3Schools Fixed Subnav", "Mathematical Terminal Seam Clamping"], "harness": "Headless Chromium Extension Loader"}'::jsonb,
    '{"coverage": "Automates regression verification on every release tag to prevent GoFullPage regressions."}'::jsonb,
    NOW()
);

\c gravity_vector;
DO $$
DECLARE
    v_vec_str TEXT;
BEGIN
    SELECT '[' || string_agg((cos(i * 0.43) / sqrt(192))::numeric(7,5)::text, ',') || ']'
    INTO v_vec_str
    FROM generate_series(1, 384) AS i;

    INSERT INTO architectural_embeddings (doc_id, title, category, content_text, embedding, metadata)
    VALUES (
        gen_random_uuid(),
        'Component Contract Architecture & Playwright E2E Matrix',
        'Component_Contracts',
        'Immutable contracts for OmniCrawler, OmniScrollEngine, OmniStitcher, and OmniPDFEngine. Automated Playwright browser extension test fixtures with Chromium persistent context.',
        v_vec_str::vector,
        '{"framework": "Playwright", "contracts": ["RFC-009", "RFC-010", "RFC-011", "RFC-012"]}'::jsonb
    );
END $$;
