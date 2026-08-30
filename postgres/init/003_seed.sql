-- ============================================================
-- SentinelOps
-- PostgreSQL Seed Data
-- Phase 4 - Database
-- ============================================================

-- ============================================================
-- 1. Roles
-- ============================================================

INSERT INTO roles (name, description)
VALUES
    (
        'Admin',
        'Full administrative access to SentinelOps'
    ),
    (
        'Security Engineer',
        'Security operations and response management access'
    ),
    (
        'Viewer',
        'Read-only security monitoring access'
    )
ON CONFLICT (name) DO NOTHING;


-- ============================================================
-- 2. Permissions
-- ============================================================

INSERT INTO permissions (code, description)
VALUES
    ('dashboard.read', 'View security dashboard'),
    ('events.read', 'View security events'),
    ('search.read', 'Search security data'),
    ('ip_intelligence.read', 'View IP intelligence'),
    ('block.execute', 'Execute IP blocking operations'),
    ('policy.read', 'View security policies'),
    ('policy.write', 'Create or modify security policies'),
    ('response.read', 'View response history'),
    ('response.execute', 'Execute security response operations'),
    ('audit.read', 'View audit logs'),
    ('backup.read', 'View backup information'),
    ('backup.execute', 'Create database or configuration backups'),
    ('restore.execute', 'Restore system data'),
    ('user.read', 'View user accounts'),
    ('user.write', 'Create or modify user accounts'),
    ('role.read', 'View roles and permissions'),
    ('system.read', 'View system configuration'),
    ('system.write', 'Modify system configuration')
ON CONFLICT (code) DO NOTHING;


-- ============================================================
-- 3. Role Permissions
-- ============================================================

-- ------------------------------------------------------------
-- Admin
-- ------------------------------------------------------------

INSERT INTO role_permissions (role_id, permission_id)
SELECT
    r.id,
    p.id
FROM roles r
CROSS JOIN permissions p
WHERE r.name = 'Admin'
ON CONFLICT DO NOTHING;


-- ------------------------------------------------------------
-- Security Engineer
-- ------------------------------------------------------------

INSERT INTO role_permissions (role_id, permission_id)
SELECT
    r.id,
    p.id
FROM roles r
JOIN permissions p
    ON p.code IN (
        'dashboard.read',
        'events.read',
        'search.read',
        'ip_intelligence.read',
        'block.execute',
        'policy.read',
        'policy.write',
        'response.read',
        'response.execute',
        'audit.read'
    )
WHERE r.name = 'Security Engineer'
ON CONFLICT DO NOTHING;


-- ------------------------------------------------------------
-- Viewer
-- ------------------------------------------------------------

INSERT INTO role_permissions (role_id, permission_id)
SELECT
    r.id,
    p.id
FROM roles r
JOIN permissions p
    ON p.code IN (
        'dashboard.read',
        'events.read',
        'search.read',
        'ip_intelligence.read',
        'policy.read',
        'response.read',
        'audit.read'
    )
WHERE r.name = 'Viewer'
ON CONFLICT DO NOTHING;