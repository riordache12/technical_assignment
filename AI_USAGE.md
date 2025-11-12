AI_USAGE.md — How I used AI tools in this exercise

Instructions
- Keep this file short (roughly 0.5–1 page). Bullet points are fine.
- Do not paste secrets, company‑internal or proprietary text into AI tools.
- This exercise runs offline; no external API calls are required.

1) Tools used
- Which tool(s) did you use (ChatGPT, Copilot, etc.) and offline/editor integration if any?

2) Prompt(s)
- Copy the key prompts you used (or summarize if many). Keep only what is necessary to understand the interaction.

3) AI output kept vs. modified
- Briefly describe what you kept as‑is and what you changed before committing.
- Add inline markers `# AI-ASSIST:` in code where the AI influenced your changes.

4) Manual correction or improvement (required)
- Provide at least one concrete example where you corrected or improved the AI’s suggestion.
- Explain why the change was needed (correctness, performance, readability, typing, tests, etc.).

5) Reflection
- What went well? What misled you? What would you try differently next time?

---

Example (filled sample — for guidance)

Note: This is an example to illustrate expected content and depth. Replace with your own notes when you complete the exercise.

1) Tools used
- Copilot for programming
- ChatGPT used to understand the problem

2) Prompt(s)
- Prompt 1 (to ChatGPT): "I want to create a small Python script that calculates a daily water balance and a conservative tracer concentration across two linked river reaches. 
                          I have the precipitation, evapotranspiration and recession factor, as well as the tracer upstream value for 7 days in one file and the reach in square km and tracer_init values in another"
- Prompt 2 (to Copilot): "create a class that allows me to write to a csv rows based on the following headers: "date", "reach", "q_m3s", "c_mgL"" (headers in legacy_results.csv)
- Prompt 3 (to Copilot): "create a function that parses a date stored in a csv cell (multiple formats possible) and returns a datetime object"
- Prompt 4 (to Copilot): I asked it to generate tests for the respective files

3) AI output kept vs. modified
- Kept: 
  - on Prompt 2, I've kept the write function and ignored the functions that would add an individual row, as it provided me an entire standalone script
  - on Prompt 3, kept most of the function as seen in the code. I thought it was nicely extendable in case more formats would have to be added.
- Modified:
  - on Prompt 2, I removed the input variables from the init and added them to the write function where I also added a @staticmethod decorator, as I am 
  not expecting to reuse that Writer more than once 
- Marked in code with `# AI-ASSIST:` near the relevant function/test.

4) Manual correction or improvement (required)
- On Prompt 2, AI suggested using the very broad Exception as a handling error. I've modified it to ValueError.

5) Reflection
- Went well: Having no hydrology experience, I used AI to understand the problem and get an explanation of the terms and formulas
- Went well: 
- Misleading: In the parametrization of the test 'test_parse_date_multiple_formats', the AI chose the current date (12/11/2025),
which failed the tests for some of the formats, because the date can still be also a month. I changed the date in order to make the
test pass.
