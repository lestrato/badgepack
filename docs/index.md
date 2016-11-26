# Badgepack

Created by Mark Clapa, Elaine Huynh, Andrew Petersen, and Steve Engels.

## Project Layout

    mkdocs.yml     # The configuration file.
    docs/
        index.md   # Documentation homepage.
        guides/    # User guides, installation, setup, etc.
        project/   # Code documentation.
        status/    # Project status, sprint details, bugs, backlog, etc.
    login/
        static/
            bootstrap/      # Bootstrap CSS, JS, etc.
            style.css       # Custom CSS to override Bootstrap CSS.
        templates/
            registration/   # Login and registration HTML pages.
            base.html       # Base template included in every HTML page.
            home.html       # Project homepage.
            nav.html        # Navigation bar HTML.
    community/
        templates/
            community.html  # Template for all community pages.
            earner.html     # Community page as seen by regular users.
            moderator.html  # Community page as seen by moderators.
            visitor.html    # Community page as seen by visitors.
    **/migration/   # Django-generated directories.