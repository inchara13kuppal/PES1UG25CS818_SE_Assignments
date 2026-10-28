# SE Lab 5 - Reflection

**Name:** Inchara K Kuppal | **SRN:** PES1UG25CS818

## 1. Which issues were easiest and hardest to fix?
Flake8 and the unused code were the easiest, since it was just fixing spaces and deleting lines. The hardest was the hidden character in `isOfficer`. It looked normal in the editor, and I only found it because Bandit and Pylint flagged it.

## 2. Were there any false positives?
Mostly no. The hardcoded password warning was only Low severity and the value was just for the demo, so it was partly a false alarm. I still moved it to an environment variable because that is better practice. The other warnings were all real problems.

## 3. How would you use static analysis in a real project?
I would run Pylint, Bandit and Flake8 automatically on every commit or pull request (pre-commit hooks or CI). That way bad code gets caught before it is merged, and we don't have to clean everything up at the end.

## 4. What improved after the fixes?
Pylint went from 5.33 to 10.00, Bandit went from 7 issues (2 High) to 0, and Flake8 went from 30 to 0. The code is safer and easier to read. It also fixed real bugs, like the wrong officer check and `NOTA: 0` printing three times.
