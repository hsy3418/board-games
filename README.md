# Board games

Small two-player browser games. Static site. Game state lives in the URL hash; live rooms relay moves through ntfy.sh pub/sub (random room names, 12h cache).

- `queens/`: Bunny Formation, Star Battle 1★ / Queens-style logic puzzle, 127 generated unique-solution puzzles (6x6..10x10), daily puzzle, zh/en. Generator: `tools_queens_gen.py`.
- `race/`: Bunny Race, dice race with trick cards, live via ntfy.sh, zh/en.
- `burrow/`: Game of the Amazons on a 7x7 board, rabbits vs foxes.
