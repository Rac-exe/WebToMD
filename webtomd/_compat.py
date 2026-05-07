"""Backward-compatibility shims for legacy terminal environments."""

from __future__ import annotations

import random
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.text import Text

GAME_WIDTH = 50
GAME_HEIGHT = 20
TICK_RATE = 0.08
STAR_COUNT = 18
HIGH_SCORE_PATH = Path.home() / ".webtomd-highscore"

FIRE_COOLDOWN_NORMAL = 2
FIRE_COOLDOWN_RAPID = 1
SHIELD_DURATION = 999
RAPID_DURATION = 80
TRIPLE_DURATION = 60
POWERUP_DROP_CHANCE = 0.20
BOSS_EVERY_N_WAVES = 5
BOSS_HP = 12
BOSS_SHOOT_INTERVAL = 12
TOUGH_HP = 2
EXPLOSION_FRAMES = 3

TITLE_ART = r"""
  ____  ____   __    ___  ____
 / ___)(  _ \ / _\  / __)(  __)
 \___ \ ) __//    \( (__  ) _)
 (____/(__)  \_/\_/ \___)(____)
   ___   __   __     __   _  _  _  _
  / __) / _\ (  )   / _\ ( \/ )( \/ )
 ( (_ \/    \/ (_/\/    \ )  (  )  /
  \___/\_/\_/\____/\_/\_/(_/\_)(__/
  ____  _  _   __    __  ____  ____  ____
 / ___)/ )( \ /  \  /  \(_  _)(  __)(  _ \
 \___ \) __ ((  O )(  O ) )(   ) _)  )   /
 (____/\_)(_/ \__/  \__/ (__) (____)(__\_)
"""


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class Entity:
    x: int
    y: int
    char: str = ""
    alive: bool = True
    hp: int = 1
    pattern: str = "straight"
    spawn_tick: int = 0


@dataclass
class PowerUp:
    x: int
    y: int
    kind: str = "R"
    alive: bool = True


@dataclass
class Explosion:
    x: int
    y: int
    ttl: int = EXPLOSION_FRAMES


@dataclass
class Boss:
    x: int
    y: int
    hp: int = BOSS_HP
    alive: bool = True
    direction: int = 1
    shoot_timer: int = 0


@dataclass
class GameState:
    player: Entity = field(default_factory=lambda: Entity(
        x=GAME_WIDTH // 2, y=GAME_HEIGHT - 2, char="^",
    ))
    bullets: list[Entity] = field(default_factory=list)
    enemies: list[Entity] = field(default_factory=list)
    enemy_bullets: list[Entity] = field(default_factory=list)
    stars: list[Entity] = field(default_factory=list)
    explosions: list[Explosion] = field(default_factory=list)
    powerups: list[PowerUp] = field(default_factory=list)
    boss: Boss | None = None
    score: int = 0
    lives: int = 3
    wave: int = 1
    running: bool = True
    ticks: int = 0
    move_left: bool = False
    move_right: bool = False
    shooting: bool = False
    last_shot_tick: int = -99
    kills: int = 0

    active_powerup: str | None = None
    powerup_remaining: int = 0
    has_shield: bool = False

    high_score: int = 0
    waiting_start: bool = True
    replay_requested: bool = False


# ---------------------------------------------------------------------------
# High score persistence
# ---------------------------------------------------------------------------


def _load_high_score() -> int:
    try:
        return int(HIGH_SCORE_PATH.read_text(encoding="utf-8").strip())
    except Exception:
        return 0


def _save_high_score(score: int) -> None:
    try:
        HIGH_SCORE_PATH.write_text(str(score), encoding="utf-8")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Sound
# ---------------------------------------------------------------------------

def _bell() -> None:
    try:
        sys.stdout.write("\a")
        sys.stdout.flush()
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Box-drawing helpers
# ---------------------------------------------------------------------------

def _supports_unicode() -> bool:
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        "\u2500".encode(encoding)
        return True
    except Exception:
        return False


_USE_UNICODE = None

def _border_chars() -> tuple[str, str, str, str, str, str]:
    global _USE_UNICODE
    if _USE_UNICODE is None:
        _USE_UNICODE = _supports_unicode()
    if _USE_UNICODE:
        return ("\u2500", "\u2502", "\u250c", "\u2510", "\u2514", "\u2518")
    return ("-", "|", "+", "+", "+", "+")


# ---------------------------------------------------------------------------
# Spawning
# ---------------------------------------------------------------------------


def _spawn_stars(state: GameState) -> None:
    for _ in range(STAR_COUNT):
        state.stars.append(Entity(
            x=random.randint(0, GAME_WIDTH - 1),
            y=random.randint(0, GAME_HEIGHT - 1),
            char="." if random.random() > 0.2 else "+",
        ))


def _spawn_wave(state: GameState) -> None:
    is_boss_wave = state.wave % BOSS_EVERY_N_WAVES == 0

    if is_boss_wave:
        state.boss = Boss(x=GAME_WIDTH // 2, y=2, hp=BOSS_HP + state.wave)
        for _ in range(3):
            state.enemies.append(_make_enemy(state, force_pattern="straight"))
        return

    count = min(5 + state.wave * 2, 22)
    for _ in range(count):
        state.enemies.append(_make_enemy(state))


def _make_enemy(state: GameState, force_pattern: str | None = None) -> Entity:
    if force_pattern:
        pattern = force_pattern
    elif state.wave >= 6:
        pattern = random.choice(["straight", "straight", "zigzag", "zigzag", "dive"])
    elif state.wave >= 3:
        pattern = random.choice(["straight", "straight", "straight", "zigzag"])
    else:
        pattern = "straight"

    is_tough = state.wave >= 3 and random.random() < min(0.15 + state.wave * 0.03, 0.45)
    char = "#" if is_tough else random.choice(["V", "W", "X", "M"])
    hp = TOUGH_HP if is_tough else 1

    return Entity(
        x=random.randint(2, GAME_WIDTH - 3),
        y=random.randint(0, 4),
        char=char,
        hp=hp,
        pattern=pattern,
        spawn_tick=state.ticks,
    )


# ---------------------------------------------------------------------------
# Tick / game logic
# ---------------------------------------------------------------------------


def _tick(state: GameState) -> None:
    state.ticks += 1

    if state.move_left and state.player.x > 2:
        state.player.x -= 2
    if state.move_right and state.player.x < GAME_WIDTH - 3:
        state.player.x += 2

    cooldown = FIRE_COOLDOWN_RAPID if state.active_powerup == "R" else FIRE_COOLDOWN_NORMAL
    if state.shooting and (state.ticks - state.last_shot_tick) >= cooldown:
        if state.active_powerup == "T":
            for dx in (-1, 0, 1):
                state.bullets.append(Entity(
                    x=max(1, min(state.player.x + dx, GAME_WIDTH - 2)),
                    y=state.player.y - 1, char="|",
                ))
        else:
            state.bullets.append(Entity(x=state.player.x, y=state.player.y - 1, char="|"))
        state.last_shot_tick = state.ticks
        state.shooting = False

    for b in state.bullets:
        b.y -= 1
        if b.y < 0:
            b.alive = False

    _move_enemies(state)
    _move_boss(state)
    _check_bullet_collisions(state)
    _check_enemy_bullet_collisions(state)
    _check_powerup_collisions(state)

    state.bullets = [b for b in state.bullets if b.alive]
    state.enemies = [e for e in state.enemies if e.alive]
    state.enemy_bullets = [b for b in state.enemy_bullets if b.alive]
    state.powerups = [p for p in state.powerups if p.alive]
    state.explosions = [e for e in state.explosions if e.ttl > 0]

    for s in state.stars:
        s.y += 1
        if s.y >= GAME_HEIGHT:
            s.y = 0
            s.x = random.randint(0, GAME_WIDTH - 1)

    if state.powerup_remaining > 0:
        state.powerup_remaining -= 1
        if state.powerup_remaining <= 0:
            if state.active_powerup == "S":
                state.has_shield = False
            state.active_powerup = None

    no_boss = state.boss is None or not state.boss.alive
    if not state.enemies and no_boss:
        state.wave += 1
        _spawn_wave(state)


def _move_enemies(state: GameState) -> None:
    descent_rate = max(6 - state.wave // 3, 2)
    for e in state.enemies:
        age = state.ticks - e.spawn_tick
        if e.pattern == "zigzag":
            if state.ticks % descent_rate == 0:
                e.y += 1
            if state.ticks % 4 == 0:
                direction = 1 if (age // 10) % 2 == 0 else -1
                e.x = max(1, min(e.x + direction, GAME_WIDTH - 2))
        elif e.pattern == "dive":
            if e.y < GAME_HEIGHT // 2:
                if state.ticks % descent_rate == 0:
                    e.y += 1
            else:
                if state.ticks % 3 == 0:
                    e.y += 1
                    if e.x < state.player.x:
                        e.x += 1
                    elif e.x > state.player.x:
                        e.x -= 1
        else:
            if state.ticks % descent_rate == 0:
                e.y += 1

        if e.y >= GAME_HEIGHT - 1:
            e.alive = False
            state.lives -= 1
            _bell()


def _move_boss(state: GameState) -> None:
    boss = state.boss
    if boss is None or not boss.alive:
        return

    if state.ticks % 2 == 0:
        boss.x += boss.direction
        if boss.x >= GAME_WIDTH - 4:
            boss.direction = -1
        elif boss.x <= 3:
            boss.direction = 1

    boss.shoot_timer += 1
    if boss.shoot_timer >= BOSS_SHOOT_INTERVAL:
        boss.shoot_timer = 0
        state.enemy_bullets.append(Entity(x=boss.x, y=boss.y + 1, char="!"))

    for eb in state.enemy_bullets:
        if state.ticks % 2 == 0:
            eb.y += 1
        if eb.y >= GAME_HEIGHT:
            eb.alive = False


def _check_bullet_collisions(state: GameState) -> None:
    for b in state.bullets:
        if not b.alive:
            continue

        for e in state.enemies:
            if not e.alive:
                continue
            if abs(b.x - e.x) <= 1 and abs(b.y - e.y) <= 1:
                b.alive = False
                e.hp -= 1
                if e.hp <= 0:
                    e.alive = False
                    state.score += 10 * state.wave
                    state.kills += 1
                    state.explosions.append(Explosion(x=e.x, y=e.y))
                    _bell()
                    if random.random() < POWERUP_DROP_CHANCE:
                        state.powerups.append(PowerUp(
                            x=e.x, y=e.y,
                            kind=random.choice(["R", "S", "T"]),
                        ))
                break

        boss = state.boss
        if boss and boss.alive and b.alive:
            if abs(b.x - boss.x) <= 2 and abs(b.y - boss.y) <= 1:
                b.alive = False
                boss.hp -= 1
                if boss.hp <= 0:
                    boss.alive = False
                    state.score += 100 * state.wave
                    state.kills += 1
                    state.explosions.append(Explosion(x=boss.x, y=boss.y))
                    _bell()
                    state.powerups.append(PowerUp(
                        x=boss.x, y=boss.y,
                        kind=random.choice(["R", "S", "T"]),
                    ))


def _check_enemy_bullet_collisions(state: GameState) -> None:
    px, py = state.player.x, state.player.y
    for eb in state.enemy_bullets:
        if not eb.alive:
            continue
        if abs(eb.x - px) <= 1 and eb.y == py:
            eb.alive = False
            if state.has_shield:
                state.has_shield = False
                state.active_powerup = None
                state.powerup_remaining = 0
            else:
                state.lives -= 1
                _bell()


def _check_powerup_collisions(state: GameState) -> None:
    px, py = state.player.x, state.player.y
    for pu in state.powerups:
        if not pu.alive:
            continue
        pu.y += 1 if state.ticks % 3 == 0 else 0
        if pu.y >= GAME_HEIGHT:
            pu.alive = False
            continue
        if abs(pu.x - px) <= 1 and abs(pu.y - py) <= 1:
            pu.alive = False
            _bell()
            state.active_powerup = pu.kind
            if pu.kind == "R":
                state.powerup_remaining = RAPID_DURATION
            elif pu.kind == "T":
                state.powerup_remaining = TRIPLE_DURATION
            elif pu.kind == "S":
                state.powerup_remaining = SHIELD_DURATION
                state.has_shield = True


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

STYLE_MAP = {
    "^": "bold green",
    "|": "yellow",
    "V": "red",
    "W": "magenta",
    "X": "bright_red",
    "M": "bold red",
    "#": "bold yellow",
    ".": "dim white",
    "+": "dim cyan",
    "*": "bold yellow",
    "!": "bright_red",
    "R": "bold cyan",
    "S": "bold green",
    "T": "bold magenta",
    "<": "bold red",
    "O": "bold bright_red",
    ">": "bold red",
}


def _render(state: GameState) -> Text:
    h, v, tl, tr, bl, br = _border_chars()

    grid_chars = [[" "] * GAME_WIDTH for _ in range(GAME_HEIGHT)]
    grid_styles = [[""] * GAME_WIDTH for _ in range(GAME_HEIGHT)]

    for s in state.stars:
        if 0 <= s.y < GAME_HEIGHT and 0 <= s.x < GAME_WIDTH:
            grid_chars[s.y][s.x] = s.char
            grid_styles[s.y][s.x] = STYLE_MAP.get(s.char, "dim white")

    for e in state.enemies:
        if 0 <= e.y < GAME_HEIGHT and 0 <= e.x < GAME_WIDTH:
            ch = e.char
            style = STYLE_MAP.get(ch, "red")
            if ch == "#" and e.hp < TOUGH_HP:
                style = "bold bright_yellow"
            grid_chars[e.y][e.x] = ch
            grid_styles[e.y][e.x] = style

    boss = state.boss
    if boss and boss.alive and 0 <= boss.y < GAME_HEIGHT:
        for dx, ch in [(-1, "<"), (0, "O"), (1, ">")]:
            bx = boss.x + dx
            if 0 <= bx < GAME_WIDTH:
                grid_chars[boss.y][bx] = ch
                grid_styles[boss.y][bx] = STYLE_MAP.get(ch, "bold red")

    for pu in state.powerups:
        if 0 <= pu.y < GAME_HEIGHT and 0 <= pu.x < GAME_WIDTH:
            grid_chars[pu.y][pu.x] = pu.kind
            grid_styles[pu.y][pu.x] = STYLE_MAP.get(pu.kind, "bold white")

    for eb in state.enemy_bullets:
        if 0 <= eb.y < GAME_HEIGHT and 0 <= eb.x < GAME_WIDTH:
            grid_chars[eb.y][eb.x] = "!"
            grid_styles[eb.y][eb.x] = "bright_red"

    for b in state.bullets:
        if 0 <= b.y < GAME_HEIGHT and 0 <= b.x < GAME_WIDTH:
            grid_chars[b.y][b.x] = "|"
            grid_styles[b.y][b.x] = "yellow"

    for ex in state.explosions:
        if 0 <= ex.y < GAME_HEIGHT and 0 <= ex.x < GAME_WIDTH:
            grid_chars[ex.y][ex.x] = "*"
            grid_styles[ex.y][ex.x] = "bold yellow" if ex.ttl > 1 else "dim yellow"
        ex.ttl -= 1

    p = state.player
    if 0 <= p.y < GAME_HEIGHT and 0 <= p.x < GAME_WIDTH:
        if state.has_shield:
            for dx, ch in [(-1, "["), (0, "^"), (1, "]")]:
                sx = p.x + dx
                if 0 <= sx < GAME_WIDTH:
                    grid_chars[p.y][sx] = ch
                    grid_styles[p.y][sx] = "bold cyan" if ch != "^" else "bold green"
        else:
            grid_chars[p.y][p.x] = "^"
            grid_styles[p.y][p.x] = "bold green"

    text = Text()

    lives_display = "".join(["<3 "] * state.lives).strip() or "NONE"
    powerup_display = ""
    if state.active_powerup:
        labels = {"R": "RAPID", "S": "SHIELD", "T": "TRIPLE"}
        powerup_display = f"  PWR: {labels.get(state.active_powerup, '?')}({state.powerup_remaining})"
    boss_display = ""
    if boss and boss.alive:
        boss_display = f"  BOSS HP: {boss.hp}"

    text.append("  ")
    text.append(f"Score: {state.score}", style="bold green")
    text.append("  ")
    text.append(f"Lives: {lives_display}", style="bold red")
    text.append("  ")
    text.append(f"Wave: {state.wave}", style="bold cyan")
    if powerup_display:
        text.append(powerup_display, style="bold magenta")
    if boss_display:
        text.append(boss_display, style="bold bright_red")
    text.append("\n\n")

    border_top = tl + h * GAME_WIDTH + tr
    border_bot = bl + h * GAME_WIDTH + br
    text.append(border_top + "\n", style="dim")

    for row_idx in range(GAME_HEIGHT):
        text.append(v, style="dim")
        for col_idx in range(GAME_WIDTH):
            ch = grid_chars[row_idx][col_idx]
            st = grid_styles[row_idx][col_idx]
            if st:
                text.append(ch, style=st)
            else:
                text.append(ch)
        text.append(v + "\n", style="dim")

    text.append(border_bot + "\n", style="dim")
    text.append("  [Arrows] Move  [Space] Shoot  [Q] Quit\n", style="dim")
    return text


# ---------------------------------------------------------------------------
# Screens
# ---------------------------------------------------------------------------


def _start_screen(high_score: int) -> Text:
    text = Text()
    for line in TITLE_ART.strip().splitlines():
        text.append("  " + line + "\n", style="bold cyan")
    text.append("\n")
    text.append("              SPACE GALAXY SHOOTER\n", style="bold bright_white")
    text.append("\n")
    text.append("     [Arrows] Move   [Space] Shoot   [Q] Quit\n", style="dim")
    text.append("\n")
    if high_score > 0:
        text.append(f"              High Score: {high_score}\n", style="bold yellow")
        text.append("\n")
    text.append("            Press SPACE to start...\n", style="bold green")
    return text


def _countdown_screen(n: int) -> Text:
    text = Text()
    text.append("\n" * (GAME_HEIGHT // 2 - 1))
    text.append(f"                    {n}\n", style="bold bright_white")
    return text


def _game_over_screen(state: GameState) -> Text:
    text = Text()
    text.append("\n\n\n")
    text.append("              GAME OVER\n", style="bold red")
    text.append("\n")
    text.append(f"         Final Score: {state.score}\n", style="bold green")
    text.append(f"         Waves Cleared: {state.wave - 1}\n", style="cyan")
    text.append(f"         Enemies Destroyed: {state.kills}\n", style="yellow")
    text.append("\n")
    if state.score > state.high_score:
        text.append("         ** NEW HIGH SCORE! **\n", style="bold bright_yellow")
        text.append("\n")
    text.append("    Press SPACE to replay, Q to quit\n", style="dim")
    return text


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------


def launch() -> None:
    """Launch the space galaxy shooter. Press q to quit."""
    try:
        from pynput import keyboard
    except ImportError:
        Console().print("[red]pynput is required for the easter egg. Install with: pip install pynput[/red]")
        return

    console = Console()

    while True:
        state = GameState()
        state.high_score = _load_high_score()
        _spawn_stars(state)

        def on_press(key):
            try:
                if hasattr(key, "char") and key.char == "q":
                    state.running = False
                    return False
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
                live.update(_start_screen(state.high_score))
                while state.waiting_start and state.running:
                    if state.shooting:
                        state.shooting = False
                        state.waiting_start = False
                    time.sleep(TICK_RATE)

                if not state.running:
                    break

                for n in (3, 2, 1):
                    live.update(_countdown_screen(n))
                    time.sleep(0.6)

                _spawn_wave(state)

                while state.running and state.lives > 0:
                    _tick(state)
                    frame = _render(state)
                    live.update(frame)
                    time.sleep(TICK_RATE)

                if state.lives <= 0:
                    _bell()
                    if state.score > state.high_score:
                        _save_high_score(state.score)
                    live.update(_game_over_screen(state))

                    state.replay_requested = False
                    state.shooting = False
                    while state.running and not state.replay_requested:
                        if state.shooting:
                            state.replay_requested = True
                            state.shooting = False
                        time.sleep(TICK_RATE)

        finally:
            state.running = False
            listener.stop()

        if not state.replay_requested:
            break

    console.clear()
    console.print(f"\n[bold cyan]Thanks for playing![/bold cyan] Final score: [green]{state.score}[/green]\n")
