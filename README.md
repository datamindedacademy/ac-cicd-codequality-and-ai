# Course name

[![Dataminded Academy](https://raw.githubusercontent.com/datamindedacademy/branding/main/assets/badge.svg)](https://github.com/datamindedacademy)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/datamindedacademy/REPO-NAME)

> **TODO:** replace `REPO-NAME` in the Codespaces badge above with this repository's
> name. The link does not work until you do.

One paragraph on what this course covers and who it is for.

## Getting started in GitHub Codespaces

Click the badge above, or **Code → Codespaces → Create codespace on main** on the
repository page. The devcontainer builds Python 3.14 and `uv`, then runs `uv sync`.
The first build takes a few minutes.

## Getting started locally

You need [uv](https://docs.astral.sh/uv/getting-started/installation/). Then:

```bash
uv sync
```

Run anything through `uv run`.

## The exercises

| Folder | Topic |
| ------ | ----- |
| [`1-first-topic`](1-first-topic/) | What they practice here |

## Reference

- Links to the docs participants will need.

## License

[MIT](LICENSE).

---

## Using this template

1. **Use this template** on GitHub, or `gh repo create datamindedacademy/<name> --template datamindedacademy/academy-template --public`.
2. Replace `REPO-NAME` in the Codespaces badge above with the new repository name.
3. Set the title, the intro paragraph and the exercise table.
4. Set the copyright year and holder in `LICENSE` if they differ.
5. Rename the project in `pyproject.toml` and `.devcontainer/devcontainer.json`.
6. Delete this section.
