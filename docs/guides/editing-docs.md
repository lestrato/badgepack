# Editing the Docs

Documentation for Badgepack is hosted by [Read the Docs](https://readthedocs.org/), and is updated every time changes are pushed to the repository. This page goes over how to update the documentation pages so that we can keep things nice and organized.

## Markdown

All of the documentation for this project is written in Markdown. If you're unfamiliar with it, [here is a good resource for Markdown syntax](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).

## Documentation Structure

The structure of the documentation is recorded in `/badgepack/mkdocs.yml`, and referred to by RTD when building the docs. If you add a new page, you _must_ edit `mkdocs.yml` to reflect these changes. Aside from `mkdocs.yml`, all documentation-related files are kept in the `badgepack/docs/` directory.

## mkdocs.yml

`mkdocs.yml` keeps track of how documentation pages are laid-out, as well as some information such as the name of the project, and the repository URL. Every time you add a new page, you should update `mkdocs.yml` to include the page. In particular, the "pages" section of the file must be updated.

The syntax is relatively straightforward; each item exists on its own line, and is preceded by tabs and hyphens. An example follows:
```
...
pages:
    - Home: index.md
    - Project Status:
        - To-do: status/todo.md
        - Backlog: status/backlog.md
    - Section Name:
        - Subsection Title: path/to-file.md
        - Another Subsection: path/to-another-file.md
        - Yet Another: path/to-another-file-again.md
...
```

## Adding a Page

* Create a new file with a meaningful name (and preferably in the correct subdirectory).
* Add some text to it.
* Update `mkdocs.yml` to include the new page.
* Commit and push your changes.

## Editing a Page

* Find the page you want to edit (refer to `mkdocs.yml` if you're lost).
* Edit the file using whatever text editor you like.
    * Refer to [the Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) if needed.
* Save your changes.
* Commit and push your changes.

## Markdown Notes

* To increase indent level in a list, precede the asterisk with a tab.
* Using tildes for strikethroughs doesn't appear to work properly. Instead, wrap the text in `<del>...</del>` tags.
* You can totally use some HTML tags (e.g. `<ul>`, `<br>`) in Markdown!