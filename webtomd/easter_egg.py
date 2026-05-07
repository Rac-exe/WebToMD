"""Space Galaxy Shooter — hidden easter egg.

Triggered by: webtomd https://play.webtomd.dev
Built with rich.Live (rendering) + pynput (keyboard input).
Cross-platform: Windows, macOS, Linux.
Press q to quit, arrow keys to move, space to shoot.
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass, field

from rich.console import Console
from rich.live import Live
from rich.text import Text


GAME_WIDTH = 50
GAME_HEIGHT = 20
TICK_RATE = 0.08
PLAYER_CHAR = "^"
BULLET_CHAR = "|"
ENEMY_CHARS = ["V", "W", "X", "M"]
STAR_CHAR = "."


@dataclass
class Entity:
    x: int
    y: int
    char: str = ""
    alive: bool = True


@dataclass
class GameState:
    player: Entity = field(default_factory=lambda: Entity(x=GAME_WIDTH // 2, y=GAME_HEIGHT - 2, char=PLAYER_CHAR))
    bullets: list[Entity] = field(default_factory=list)
    enemies: list[Entity] = field(default_factory=list)
    stars: list[Entity] = field(default_factory=list)
    score: int = 0
    lives: int = 3
    wave: int = 1
    running: bool = True
    ticks: int = 0
    move_left: bool = False
    move_right: bool = False
    shooting: bool = False


def launch() -> None:
    """Launch the space galaxy shooter. Press q to quit."""
    console = Console()
    console.clear()
    console.print("[bold cyan]SPACE GALAXY SHOOTER[/bold cyan]", justify="center")
    console.print("[dim]Arrow keys: move | Space: shoot | Q: quit[/dim]\n", justify="center")
    time.sleep(1.2)

    state = GameState()
    _spawn_stars(state)
    _spawn_wave(state)

    try:
        from pynput import keyboard
    except ImportError:
        console.print("[red]pynput is required for the easter egg. Install with: pip install pynput[/red]")
        return

    def on_press(key):
        try:
            if hasattr(key, "char") and key.char == "q":
                state.running = False
                return False
            if hasattr(key, "char") and key.char == " ":
                state.shooting = True
        except AttributeError:
            pass
        if key == keyboard.Key.left:
            state.move_left = True
        elif key == keyboard.Key.right:
            state.move_right = True
        elif key == keyboard.Key.space:
            state.shooting = True

    def on_release(key):
        if key == keyboard.Key.left:
            state.move_left = False
        elif key == keyboard.Key.right:
            state.move_right = False

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    try:
        with Live(console=console, refresh_per_second=12, screen=True) as live:
            while state.running and state.lives > 0:
                _tick(state)
                frame = _render(state)
                live.update(frame)
                time.sleep(TICK_RATE)

            if state.lives <= 0:
                live.update(_game_over_screen(state))
                time.sleep(3)
    finally:
        state.running = False
        listener.stop()

    console.clear()
    console.print(f"\n[bold cyan]Game Over![/bold cyan] Final score: [green]{state.score}[/green]\n")


def _tick(state: GameState) -> None:
    state.ticks += 1

    if state.move_left and state.player.x > 1:
        state.player.x -= 1
    if state.move_right and state.player.x < GAME_WIDTH - 2:
        state.player.x += 1

    if state.shooting:
        state.bullets.append(Entity(x=state.player.x, y=state.player.y - 1, char=BULLET_CHAR))
        state.shooting = False

    for b in state.bullets:
        b.y -= 1
        if b.y < 0:
            b.alive = False

    for e in state.enemies:
        if state.ticks % max(4 - state.wave // 3, 1) == 0:
            e.y += 1
        if e.y >= GAME_HEIGHT - 1:
            e.alive = False
            state.lives -= 1

    for b in state.bullets:
        if not b.alive:
            continue
        for e in state.enemies:
            if not e.alive:
                continue
            if abs(b.x - e.x) <= 1 and abs(b.y - e.y) <= 1:
                b.alive = False
                e.alive = False
                state.score += 10 * state.wave

    state.bullets = [b for b in state.bullets if b.alive]
    state.enemies = [e for e in state.enemies if e.alive]

    for s in state.stars:
        s.y += 1
        if s.y >= GAME_HEIGHT:
            s.y = 0
            s.x = random.randint(0, GAME_WIDTH - 1)

    if not state.enemies:
        state.wave += 1
        _spawn_wave(state)


def _spawn_wave(state: GameState) -> None:
    count = min(5 + state.wave * 2, 20)
    for _ in range(count):
        state.enemies.append(
            Entity(
                x=random.randint(2, GAME_WIDTH - 3),
                y=random.randint(0, 4),
                char=random.choice(ENEMY_CHARS),
            )
        )


def _spawn_stars(state: GameState) -> None:
    for _ in range(15):
        state.stars.append(
            Entity(
                x=random.randint(0, GAME_WIDTH - 1),
                y=random.randint(0, GAME_HEIGHT - 1),
                char=STAR_CHAR,
            )
        )


def _render(state: GameState) -> Text:
    grid = [[" "] * GAME_WIDTH for _ in range(GAME_HEIGHT)]

    for s in state.stars:
        if 0 <= s.y < GAME_HEIGHT and 0 <= s.x < GAME_WIDTH:
            grid[s.y][s.x] = STAR_CHAR

    for e in state.enemies:
        if 0 <= e.y < GAME_HEIGHT and 0 <= e.x < GAME_WIDTH:
            grid[e.y][e.x] = e.char

    for b in state.bullets:
        if 0 <= b.y < GAME_HEIGHT and 0 <= b.x < GAME_WIDTH:
            grid[b.y][b.x] = BULLET_CHAR

    p = state.player
    if 0 <= p.y < GAME_HEIGHT and 0 <= p.x < GAME_WIDTH:
        grid[p.y][p.x] = PLAYER_CHAR

    border_h = "+" + "-" * GAME_WIDTH + "+"
    lines = [f"  Score: {state.score}  Lives: {'<3 ' * state.lives}  Wave: {state.wave}", ""]
    lines.append(border_h)
    for row in grid:
        lines.append("|" + "".join(row) + "|")
    lines.append(border_h)
    lines.append("  [Arrow keys] Move  [Space] Shoot  [Q] Quit")

    text = Text()
    for line in lines:
        text.append(line + "\n")
    return text


def _game_over_screen(state: GameState) -> Text:
    text = Text()
    text.append("\n\n")
    text.append("    GAME OVER\n", style="bold red")
    text.append(f"\n    Final Score: {state.score}\n", style="bold green")
    text.append(f"    Waves Cleared: {state.wave - 1}\n", style="cyan")
    text.append("\n    Thanks for playing!\n", style="dim")
    return text
