# Contributing

Thanks for helping improve `/rea-brand`.

## Report a problem

Open an issue with:
- the prompt you ran and the person you ran it on (public creators only),
- the step where it went wrong,
- the error or the wrong output, and the relevant lines from `ledger.txt`.

## Change the skill

1. Edit `skills/rea-brand/SKILL.md`.
2. Run the changed step on a real public creator and check the output.
3. Don't write a dollar sign directly before a digit in `SKILL.md`. Claude Code reads `$0`, `$1`
   and so on as argument placeholders. Write prices as cents (`2¢`) or with `USD`.
4. Keep every endpoint id real: check it with `treg catalog get <id>` before you add it.
5. Add a line to `CHANGELOG.md` under `[Unreleased]`.
6. Open a pull request that says what you changed, why, and what it cost to test.

## Ground rules

Changes must keep the skill inside its rules: public creators and public data only, no logins
or cookies, no contact details, no naming private individuals, and every finding marked SEEN or
INFERRED.
