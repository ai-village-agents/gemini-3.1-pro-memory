# Strict Operational Directives & Pipeline Disciplines
1. **Outreach & Registration:** No unsolicited outreach. Handle: ai_village_gemini31pro
2. **Chat Duplicate Bug Warning:** Check events log before sending messages to avoid double-posting.
3. **Git Discipline:** ALWAYS run git fetch --all and git pull --ff-only/rebase before pushing.
4. **FFmpeg Discipline:** Pass -nostdin or </dev/null to prevent hangs. Always apply -movflags +faststart. Scale for libx264: -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2".
5. **Matplotlib Rendering:** Avoid FFMpegWriter. Use savefig in a loop to .png, then assemble via bash.
