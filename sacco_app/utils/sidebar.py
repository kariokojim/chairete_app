SIDEBAR_ITEMS = [
    {
        "label": "Dashboard",
        "icon": "bi-speedometer2",
        "endpoint": "admin.dashboard",
        "roles": ["admin", "staff"]
    },
    {
        "label": "Members",
        "icon": "bi-people",
        "endpoint": "admin.list_members",
        "roles": ["admin", "staff"]
    },
    {
        "label": "Loans",
        "icon": "bi-cash-stack",
        "endpoint": "admin.list_loans",
        "roles": ["admin", "staff"]
    },
    {
        "label": "Reports",
        "icon": "bi-bar-chart",
        "endpoint": "admin.gl_report",
        "roles": ["admin"]
    },
    {
        "label": "User Management",
        "icon": "bi-person-badge",
        "endpoint": "admin.list_users",
        "roles": ["admin"]
    },
    {
        "label": "Audit Logs",
        "icon": "bi-shield-check",
        "endpoint": "admin.audit_logs",
        "roles": ["admin"]
    }

    
]
