-- ============================================================
-- SentinelOps
-- PostgreSQL Initial Schema
-- Phase 4 - Database
-- ============================================================

-- ============================================================
-- 1. Roles
-- ============================================================

CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================================
-- 2. Permissions
-- ============================================================

CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================================
-- 3. Users
-- ============================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role_id UUID REFERENCES roles(id),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT users_status_check
        CHECK (status IN ('ACTIVE', 'DISABLED', 'LOCKED'))
);


-- ============================================================
-- 4. Role Permissions
-- ============================================================

CREATE TABLE role_permissions (
    role_id UUID NOT NULL REFERENCES roles(id),
    permission_id UUID NOT NULL REFERENCES permissions(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (role_id, permission_id)
);


-- ============================================================
-- 5. Security Events
-- ============================================================

CREATE TABLE security_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    event_time TIMESTAMPTZ NOT NULL,
    source_ip INET NOT NULL,

    method VARCHAR(20) NOT NULL,
    request_uri TEXT NOT NULL,
    protocol VARCHAR(20),

    status_code SMALLINT,

    user_agent TEXT,
    referer TEXT,

    request_size BIGINT,
    response_size BIGINT,
    response_time_ms INTEGER,

    host VARCHAR(255),
    server_name VARCHAR(255),

    raw_log TEXT,

    event_status VARCHAR(30) NOT NULL DEFAULT 'DETECTED',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT security_events_status_check
        CHECK (
            event_status IN (
                'DETECTED',
                'INVESTIGATING',
                'BLOCKED',
                'RESOLVED',
                'IGNORED'
            )
        )
);


-- ============================================================
-- 6. Detection Results
-- ============================================================

CREATE TABLE detections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    event_id UUID NOT NULL
        REFERENCES security_events(id),

    detection_type VARCHAR(100) NOT NULL,
    rule_name VARCHAR(255),

    severity VARCHAR(20) NOT NULL,

    confidence NUMERIC(5,4),

    evidence JSONB,
    description TEXT,

    detected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT detections_severity_check
        CHECK (
            severity IN (
                'LOW',
                'MEDIUM',
                'HIGH',
                'CRITICAL'
            )
        ),

    CONSTRAINT detections_confidence_check
        CHECK (
            confidence IS NULL
            OR (confidence >= 0 AND confidence <= 1)
        )
);


-- ============================================================
-- 7. Risk Scores
-- ============================================================

CREATE TABLE risk_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    event_id UUID NOT NULL
        REFERENCES security_events(id),

    source_ip INET NOT NULL,

    score INTEGER NOT NULL,

    severity VARCHAR(20) NOT NULL,

    calculation_version VARCHAR(50),

    factors JSONB,

    calculated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT risk_scores_score_check
        CHECK (score >= 0 AND score <= 100),

    CONSTRAINT risk_scores_severity_check
        CHECK (
            severity IN (
                'LOW',
                'MEDIUM',
                'HIGH',
                'CRITICAL'
            )
        )
);


-- ============================================================
-- 8. Policies
-- ============================================================

CREATE TABLE policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name VARCHAR(255) NOT NULL UNIQUE,

    description TEXT,

    enabled BOOLEAN NOT NULL DEFAULT TRUE,

    priority INTEGER NOT NULL DEFAULT 100,

    action VARCHAR(100) NOT NULL,

    duration_seconds INTEGER,

    created_by UUID
        REFERENCES users(id),

    updated_by UUID
        REFERENCES users(id),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT policies_priority_check
        CHECK (priority >= 1),

    CONSTRAINT policies_duration_check
        CHECK (
            duration_seconds IS NULL
            OR duration_seconds >= 0
        )
);


-- ============================================================
-- 9. Policy Rules
-- ============================================================

CREATE TABLE policy_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID NOT NULL
        REFERENCES policies(id)
        ON DELETE CASCADE,

    field VARCHAR(100) NOT NULL,

    operator VARCHAR(50) NOT NULL,

    value TEXT NOT NULL,

    logical_operator VARCHAR(10) DEFAULT 'AND',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT policy_rules_logical_operator_check
        CHECK (
            logical_operator IN ('AND', 'OR')
        )
);


-- ============================================================
-- 10. Policy Evaluations
-- ============================================================

CREATE TABLE policy_evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    event_id UUID NOT NULL
        REFERENCES security_events(id),

    policy_id UUID NOT NULL
        REFERENCES policies(id),

    matched BOOLEAN NOT NULL,

    evaluation_result VARCHAR(100) NOT NULL,

    reason TEXT,

    evaluated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================================
-- 11. IP Lists
-- ============================================================

CREATE TABLE ip_lists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    ip_address INET NOT NULL,

    list_type VARCHAR(20) NOT NULL,

    reason TEXT,

    expires_at TIMESTAMPTZ,

    enabled BOOLEAN NOT NULL DEFAULT TRUE,

    created_by UUID
        REFERENCES users(id),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT ip_lists_type_check
        CHECK (
            list_type IN ('WHITELIST', 'BLACKLIST')
        )
);


-- ============================================================
-- 12. Responses
-- ============================================================

CREATE TABLE responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    event_id UUID
        REFERENCES security_events(id),

    policy_id UUID
        REFERENCES policies(id),

    initiated_by UUID
        REFERENCES users(id),

    response_type VARCHAR(50) NOT NULL,

    target_ip INET,

    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',

    reason TEXT,

    started_at TIMESTAMPTZ,

    completed_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT responses_status_check
        CHECK (
            status IN (
                'PENDING',
                'RUNNING',
                'CONFIG_TEST',
                'APPLY',
                'VERIFY',
                'SUCCESS',
                'FAILED',
                'CANCELLED'
            )
        )
);


-- ============================================================
-- 13. Response Steps
-- ============================================================

CREATE TABLE response_steps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    response_id UUID NOT NULL
        REFERENCES responses(id)
        ON DELETE CASCADE,

    step_order INTEGER NOT NULL,

    step_type VARCHAR(50) NOT NULL,

    status VARCHAR(30) NOT NULL,

    message TEXT,

    metadata JSONB,

    started_at TIMESTAMPTZ,

    completed_at TIMESTAMPTZ,

    CONSTRAINT response_steps_order_check
        CHECK (step_order > 0),

    CONSTRAINT response_steps_status_check
        CHECK (
            status IN (
                'PENDING',
                'RUNNING',
                'SUCCESS',
                'FAILED',
                'SKIPPED'
            )
        ),

    UNIQUE (response_id, step_order)
);


-- ============================================================
-- 14. Incidents
-- ============================================================

CREATE TABLE incidents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    title VARCHAR(255) NOT NULL,

    description TEXT,

    severity VARCHAR(20) NOT NULL,

    status VARCHAR(30) NOT NULL,

    source_ip INET,

    assigned_to UUID
        REFERENCES users(id),

    opened_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    resolved_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT incidents_severity_check
        CHECK (
            severity IN (
                'LOW',
                'MEDIUM',
                'HIGH',
                'CRITICAL'
            )
        )
);


-- ============================================================
-- 15. Incident Events
-- ============================================================

CREATE TABLE incident_events (
    incident_id UUID NOT NULL
        REFERENCES incidents(id)
        ON DELETE CASCADE,

    event_id UUID NOT NULL
        REFERENCES security_events(id),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (incident_id, event_id)
);


-- ============================================================
-- 16. Audit Logs
-- ============================================================

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    actor_user_id UUID
        REFERENCES users(id),

    action VARCHAR(100) NOT NULL,

    target_type VARCHAR(100),

    target_id UUID,

    result VARCHAR(30) NOT NULL,

    reason TEXT,

    source_ip INET,

    before_data JSONB,

    after_data JSONB,

    correlation_id UUID,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================================
-- 17. Config Versions
-- ============================================================

CREATE TABLE config_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    version VARCHAR(100) NOT NULL,

    config_type VARCHAR(100) NOT NULL,

    content_hash VARCHAR(255) NOT NULL,

    storage_path TEXT,

    created_by UUID
        REFERENCES users(id),

    status VARCHAR(30) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================================
-- 18. Backups
-- ============================================================

CREATE TABLE backups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    backup_type VARCHAR(50) NOT NULL,

    version VARCHAR(100) NOT NULL,

    file_path TEXT,

    file_size BIGINT,

    checksum VARCHAR(255),

    status VARCHAR(30) NOT NULL,

    created_by UUID
        REFERENCES users(id),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================================
-- 19. Service Statuses
-- ============================================================

CREATE TABLE service_statuses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    service_name VARCHAR(100) NOT NULL,

    status VARCHAR(30) NOT NULL,

    health_status VARCHAR(30) NOT NULL,

    cpu_percent NUMERIC(5,2),

    memory_percent NUMERIC(5,2),

    disk_percent NUMERIC(5,2),

    last_check_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    details JSONB
);


-- ============================================================
-- 20. System Reports
-- ============================================================

CREATE TABLE system_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    report_type VARCHAR(100) NOT NULL,

    period_start TIMESTAMPTZ,

    period_end TIMESTAMPTZ,

    status VARCHAR(30) NOT NULL,

    file_path TEXT,

    created_by UUID
        REFERENCES users(id),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================================
-- INDEXES
-- ============================================================

-- User / Authorization
CREATE INDEX idx_users_role_id
    ON users(role_id);

CREATE INDEX idx_users_status
    ON users(status);


-- Security Events
CREATE INDEX idx_security_events_event_time
    ON security_events(event_time DESC);

CREATE INDEX idx_security_events_source_ip
    ON security_events(source_ip);

CREATE INDEX idx_security_events_status
    ON security_events(event_status);

CREATE INDEX idx_security_events_status_time
    ON security_events(event_status, event_time DESC);


-- Detection
CREATE INDEX idx_detections_event_id
    ON detections(event_id);

CREATE INDEX idx_detections_type
    ON detections(detection_type);

CREATE INDEX idx_detections_severity
    ON detections(severity);

CREATE INDEX idx_detections_detected_at
    ON detections(detected_at DESC);


-- Risk
CREATE INDEX idx_risk_scores_event_id
    ON risk_scores(event_id);

CREATE INDEX idx_risk_scores_source_ip
    ON risk_scores(source_ip);

CREATE INDEX idx_risk_scores_score
    ON risk_scores(score DESC);

CREATE INDEX idx_risk_scores_calculated_at
    ON risk_scores(calculated_at DESC);


-- Policy
CREATE INDEX idx_policies_enabled_priority
    ON policies(enabled, priority);

CREATE INDEX idx_policy_rules_policy_id
    ON policy_rules(policy_id);

CREATE INDEX idx_policy_evaluations_event_id
    ON policy_evaluations(event_id);

CREATE INDEX idx_policy_evaluations_policy_id
    ON policy_evaluations(policy_id);


-- IP Lists
CREATE INDEX idx_ip_lists_ip_address
    ON ip_lists(ip_address);

CREATE INDEX idx_ip_lists_type_enabled
    ON ip_lists(list_type, enabled);

CREATE INDEX idx_ip_lists_expires_at
    ON ip_lists(expires_at);


-- Responses
CREATE INDEX idx_responses_event_id
    ON responses(event_id);

CREATE INDEX idx_responses_policy_id
    ON responses(policy_id);

CREATE INDEX idx_responses_target_ip
    ON responses(target_ip);

CREATE INDEX idx_responses_status
    ON responses(status);

CREATE INDEX idx_responses_created_at
    ON responses(created_at DESC);


-- Response Steps
CREATE INDEX idx_response_steps_response_id
    ON response_steps(response_id);


-- Incidents
CREATE INDEX idx_incidents_status
    ON incidents(status);

CREATE INDEX idx_incidents_source_ip
    ON incidents(source_ip);

CREATE INDEX idx_incidents_assigned_to
    ON incidents(assigned_to);


-- Audit
CREATE INDEX idx_audit_logs_actor_user_id
    ON audit_logs(actor_user_id);

CREATE INDEX idx_audit_logs_target
    ON audit_logs(target_type, target_id);

CREATE INDEX idx_audit_logs_created_at
    ON audit_logs(created_at DESC);

CREATE INDEX idx_audit_logs_correlation_id
    ON audit_logs(correlation_id);


-- Config
CREATE INDEX idx_config_versions_created_at
    ON config_versions(created_at DESC);

CREATE INDEX idx_config_versions_type_status
    ON config_versions(config_type, status);


-- Backup
CREATE INDEX idx_backups_created_at
    ON backups(created_at DESC);

CREATE INDEX idx_backups_type_status
    ON backups(backup_type, status);


-- Service Status
CREATE INDEX idx_service_statuses_service_name
    ON service_statuses(service_name);

CREATE INDEX idx_service_statuses_last_check
    ON service_statuses(last_check_at DESC);


-- Reports
CREATE INDEX idx_system_reports_created_at
    ON system_reports(created_at DESC);

CREATE INDEX idx_system_reports_type
    ON system_reports(report_type);