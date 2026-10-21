# v14 ask_seq
- 65 frames f000..f064, 12 fps (5.4 s), 786x1704 PNG, square corners, no shadow/bezel. Frame i = t*12.
- Source: dev build localhost:5173 (no mock), recorded by rec.mjs (CDP screencast, same as v13). Status bar, time, icons, island, home indicator = visibility:hidden (plain background shows). Keyboard hidden (.kb visibility:hidden) after typing, before Send, so frame 0 is the typed query with no keyboard.
- f000: typed query "I want to find someone to go climbing with me" (input already moved to bottom, send tapped).
- f001: thinking starts ("Reading your notes..." + skeleton cards); "Looking through your people..." ~f016; "Picking the best matches..." ~f024.
- f026: results appear (cards reveal); settled ~f030; f030-f064 hold (~2.9 s).
- Dev build data: Jordan Lee (Founder @ [Startup] - Brooklyn, teal blob avatar, "Climbs Tuesdays, wants a climbing buddy"), Zara Ahmed (Musician - Brooklyn, NY, pink blob avatar, "Just got into bouldering"), white "Draft a message" buttons, "Show all 2 on the mindmap", "Ask me about people" bar at bottom.
