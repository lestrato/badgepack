# Static Files and CSS

Path: `/badgepack/login/static/`  

Badgepack makes use of Bootstrap CSS/JS as its base, with some of its style being overwritten by `style.css`. This section details the contents of `style.css`.

## Layout

    login/static/
        bootstrap/  # Bootstrap CSS and JS files.
        style.css   # Custom CSS (overwrites Bootstrap CSS).

## CSS Details

Selector | Description/Notes
--- | ---
`body` | Main body of the pages |
`hr` | Horizontal rule; colour has been modified
`.navbar-default` | Navigation bar
`.navbar-default .navbar-nav > li > a` | Buttons / links in the navigation bar
`.badge-list` | Badge list; not included in Bootstrap
`.badge-list > li` | Members (badges) of the badge list; set to display like a 2- or 3-column table
`.badge-container` | Container for badges; width and height are set here
`.badge-image-container` | Container for the badge image; set to be aligned to the top
`.badge-image` | Contents of `.badge-image-container`; default: an empty 100x100 grey box
`.badge-image > img` | Resizes badges to fit the image container
`.badge-name` | Name/title of the badge
`.badge-description` | Contents of the badge
`.badge-footer` | Bottom row of the badge container; text of the bottom row is handled by `.badge-footer-left` and `.badge-footer-right`
`.badge-footer-left` | Left-most text of the badge footer (i.e. date created/earned)
`.badge-footer-right` | Right-most text of the badge footer (i.e. progress %)