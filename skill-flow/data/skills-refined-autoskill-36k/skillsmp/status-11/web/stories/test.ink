VAR seen_smoke = false
-> start
=== start ===
Hello from InkJS demo.
#smoke
~ seen_smoke = true
*   Do you want to continue? -> choice_one
*   Or stay here? -> choice_two
=== choice_one ===
You move forward.
-> END
=== choice_two ===
You decide to stay. The smoke clears.
-> END
