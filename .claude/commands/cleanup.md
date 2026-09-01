End-of-session cleanup. Load Lila and Pam, run documentation and memory updates.

Do the following:

1. **Load profiles**: Read `~/.claude/team/staff/lila.md` and `~/.claude/team/staff/pam.md` to activate both team members for this session.

2. **Pam — Documentation updates**: Review the session and update any relevant project documentation in `Project/`. This includes meeting notes (`Project/meetings/`), changelog entries (`Project/notes/`), and any other docs that need updating. Present proposed updates to Aaron for approval before writing.

3. **Lila — Memory updates**: Review the conversation for any new feedback, project state, user preferences, or reference information that should be saved to the memory system. Check existing memories for anything that needs updating or removing. Present proposed memory changes to Aaron for approval before writing.

4. **Lila — Prepare commits**: Review all uncommitted changes (staged and unstaged). If there are changes to commit:
   - Run `git status` and `git diff --stat`
   - Draft a commit message following the repo's commit style
   - Present the proposed commit to Aaron for approval
   - Do NOT commit or push without Aaron's explicit go-ahead

5. **Report**: Once all steps are complete, Pam gives a brief summary of everything that was updated.
