# Release Notes

Use when the deliverable is a release note, changelog entry or update-feed text. Follow the target project's actual instructions and release sources, not a required `CLAUDE.md` filename or a particular hosting platform.

## Establish the Release

Resolve the last published version and the exact candidate users will receive. Use `HEAD` only when it is that candidate. Include generated or uncommitted changes only when they will actually ship; later commits are not material for an older build.

Read the relevant project conventions and recent release notes for language, structure and tone. Retrieve remote release information through the actual host's available tools; `gh` is an option only for GitHub. Reuse an already identified sibling-project reference when the user requests one; ask only if its identity is unresolved.

Inspect changes within the artifact boundary using commits, diffs and delivery evidence. Do not rely solely on `feat:` or `fix:` prefixes; repositories use different conventions and a user-visible change can appear under any prefix.

## Describe the Result

- Cover distinct user-visible outcomes, required migration steps, compatibility changes and deprecations. Combine changes serving the same result; do not imitate the last release's item count.
- Use project categories when established, otherwise group by the affected user activity or capability. Do not force a desktop application's page names or an internal module taxonomy onto another product.
- Prefer concise statements of what changes for the intended reader. Include mechanism details only when they help that reader configure, migrate, diagnose or decide. Necessary instructions may take more than one sentence.
- Keep language, emoji and punctuation consistent with the user's or project's style. Bilingual output is optional unless requested or required by the target channel; use its established layout and keep meanings aligned.
- Distinguish already available, preview, planned and unreleased changes. Never promise a channel, release date or supported version without evidence.

Check the finished text against the candidate artifact and requested format. Drafting release notes does not authorize publishing, changing versions or sending announcements.
