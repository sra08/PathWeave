import pygame

# ── Palette ────────────────────────────────────────────────────────────────────
BG          = (15,  20,  40)
PANEL       = (22,  30,  55)
ACCENT      = (52,  152, 219)
ACCENT2     = (46,  204, 113)
BTN         = (35,  45,  75)
BTN_HOVER   = (55,  70,  110)
BTN_ACTIVE  = (41,  128, 185)
TEXT_MAIN   = (240, 245, 255)
TEXT_DIM    = (140, 155, 180)
RED         = (231, 76,  60)
GOLD        = (241, 196, 15)
DIVIDER     = (40,  55,  90)

# Legend colors
C_WALL      = (30,  30,  50)
C_START     = (39,  174, 96)
C_END       = (231, 76,  60)
C_VISITED   = (52,  152, 219)
C_FRONTIER  = (133, 193, 233)
C_PATH      = (241, 196, 15)


def draw_rounded_rect(surface, color, rect, radius=8, border=0, border_color=None):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surface, border_color, rect, border, border_radius=radius)


class Visualizer:
    def __init__(self, screen, grid, grid_w, sidebar_w, win_w, win_h):
        self.screen = screen
        self.grid = grid
        self.grid_w = grid_w
        self.sidebar_w = sidebar_w
        self.win_w = win_w
        self.win_h = win_h
        self.sx = grid_w  # sidebar x start

        self.font_title  = pygame.font.SysFont("Segoe UI", 18, bold=True)
        self.font_label  = pygame.font.SysFont("Segoe UI", 14, bold=True)
        self.font_small  = pygame.font.SysFont("Segoe UI", 12)
        self.font_stat   = pygame.font.SysFont("Consolas", 13, bold=True)
        self.font_big    = pygame.font.SysFont("Segoe UI", 22, bold=True)

        self.buttons = {}   # name -> pygame.Rect
        self._build_buttons()

    def _build_buttons(self):
        sx, sw = self.sx + 10, self.sidebar_w - 20
        y = 16

        def btn(name, w, h, x_off=0):
            r = pygame.Rect(sx + x_off, y, w, h)
            self.buttons[name] = r
            return r

        # Title placeholder — no button
        y += 44

        # Algorithm selector
        y += 22
        btn("algo_left",  30, 30, 0)
        btn("algo_right", 30, 30, sw - 30)
        y += 38

        # Speed selector
        y += 22
        btn("speed_left",  30, 30, 0)
        btn("speed_right", 30, 30, sw - 30)
        y += 38

        # Mode buttons row
        y += 18
        hw = (sw - 6) // 2
        btn("set_start", hw, 30, 0)
        btn("set_end",   hw, 30, hw + 6)
        y += 36

        btn("draw",  hw, 30, 0)
        btn("erase", hw, 30, hw + 6)
        y += 46

        # Run / Clear / Reset
        btn("run",        sw, 40, 0);  y += 48
        btn("clear_path", sw, 32, 0);  y += 38
        btn("reset",      sw, 32, 0)

        # Store y for stats section start
        self._stats_y = y + 50

    def get_button_at(self, mx, my):
        for name, rect in self.buttons.items():
            if rect.collidepoint(mx, my):
                return name
        return None

    def _draw_button(self, name, label, color=BTN, text_color=TEXT_MAIN, radius=8, border=None):
        rect = self.buttons[name]
        mx, my = pygame.mouse.get_pos()
        hover = rect.collidepoint(mx, my)
        c = BTN_HOVER if hover else color
        draw_rounded_rect(self.screen, c, rect, radius)
        if border:
            draw_rounded_rect(self.screen, c, rect, radius, 2, border)
        surf = self.font_label.render(label, True, text_color)
        self.screen.blit(surf, surf.get_rect(center=rect.center))

    def _label(self, text, x, y, color=TEXT_DIM, font=None):
        f = font or self.font_small
        surf = f.render(text, True, color)
        self.screen.blit(surf, (x, y))

    def draw(self, algo_name, speed_name, running, path_found, no_path, stats, mode, placing):
        self.screen.fill(BG)
        self.grid.draw(self.screen)

        # ── Sidebar background ──────────────────────────────────────────────────
        sidebar_rect = pygame.Rect(self.sx, 0, self.sidebar_w, self.win_h)
        pygame.draw.rect(self.screen, PANEL, sidebar_rect)
        pygame.draw.line(self.screen, DIVIDER, (self.sx, 0), (self.sx, self.win_h), 2)

        sx = self.sx + 10
        sw = self.sidebar_w - 20

        # ── Title ──────────────────────────────────────────────────────────────
        t = self.font_big.render("AI Pathfinder", True, TEXT_MAIN)
        self.screen.blit(t, (sx, 14))
        pygame.draw.line(self.screen, DIVIDER, (sx, 46), (sx + sw, 46), 1)

        # ── Algorithm selector ─────────────────────────────────────────────────
        y = 56
        self._label("ALGORITHM", sx, y, TEXT_DIM, self.font_small)
        y += 18
        self._draw_button("algo_left",  "<", BTN)
        self._draw_button("algo_right", ">", BTN)
        lbl = self.font_label.render(algo_name, True, ACCENT)
        lbl_r = lbl.get_rect(center=(sx + sw // 2, y + 15))
        self.screen.blit(lbl, lbl_r)

        # ── Speed selector ─────────────────────────────────────────────────────
        y = 114
        self._label("SPEED", sx, y, TEXT_DIM, self.font_small)
        y += 18
        self._draw_button("speed_left",  "<", BTN)
        self._draw_button("speed_right", ">", BTN)
        slbl = self.font_label.render(speed_name, True, ACCENT)
        slbl_r = slbl.get_rect(center=(sx + sw // 2, y + 15))
        self.screen.blit(slbl, slbl_r)

        # ── Mode buttons ───────────────────────────────────────────────────────
        y = 204
        y += 18
        dc = BTN_ACTIVE if mode == "draw"  else BTN
        er = BTN_ACTIVE if mode == "erase" else BTN
        self._draw_button("draw",  "Draw",  dc)
        self._draw_button("erase", "Erase", er)
        
        
        y = 168
        self._label("PLACE NODES", sx, y, TEXT_DIM, self.font_small)
        y += 18
        sc = BTN_ACTIVE if placing == "start" else BTN
        ec = BTN_ACTIVE if placing == "end"   else BTN
        self._draw_button("set_start", "Set Start", sc, C_START if placing == "start" else TEXT_MAIN)
        self._draw_button("set_end",   "Set End",   ec, C_END   if placing == "end"   else TEXT_MAIN)

        

        pygame.draw.line(self.screen, DIVIDER, (sx, 252), (sx + sw, 252), 1)

        # ── Action buttons ────────────────────────────────────────────────────
        run_c = (60, 80, 60) if running else ACCENT2
        run_lbl = "Running..." if running else "RUN"
        self._draw_button("run", run_lbl, run_c, radius=10)
        self._draw_button("clear_path", "Clear Path", BTN)
        self._draw_button("reset", "Reset Grid", (70, 30, 30), RED)

        pygame.draw.line(self.screen, DIVIDER, (sx, self._stats_y - 10), (sx + sw, self._stats_y - 10), 1)

        # ── Stats ─────────────────────────────────────────────────────────────
        sy = self._stats_y
        self._label("STATISTICS", sx, sy, TEXT_DIM, self.font_small)
        sy += 20

        def stat_row(label, val, color=TEXT_MAIN):
            l = self.font_small.render(label, True, TEXT_DIM)
            v = self.font_stat.render(str(val), True, color)
            self.screen.blit(l, (sx, sy))
            self.screen.blit(v, (sx + sw - v.get_width(), sy))

        stat_row("Nodes explored:", stats["nodes"], ACCENT)
        sy += 20
        self.screen.blit(self.font_small.render("Nodes explored:", True, TEXT_DIM), (sx, sy - 20))
        self.screen.blit(self.font_stat.render(str(stats["nodes"]), True, ACCENT), (sx + sw - self.font_stat.size(str(stats["nodes"]))[0], sy - 20))

        self.screen.blit(self.font_small.render("Path length:", True, TEXT_DIM), (sx, sy))
        plen = str(stats["path_len"]) if stats["path_len"] else "-"
        self.screen.blit(self.font_stat.render(plen, True, GOLD), (sx + sw - self.font_stat.size(plen)[0], sy))

        sy += 20
        self.screen.blit(self.font_small.render("Time (s):", True, TEXT_DIM), (sx, sy))
        t_str = f"{stats['time']:.3f}" if stats["time"] else "-"
        self.screen.blit(self.font_stat.render(t_str, True, ACCENT2), (sx + sw - self.font_stat.size(t_str)[0], sy))

        sy += 30

        # Status message
        if path_found:
            msg = self.font_label.render("Path Found!", True, ACCENT2)
            self.screen.blit(msg, msg.get_rect(centerx=sx + sw // 2, y=sy))
        elif no_path:
            msg = self.font_label.render("No Path Exists", True, RED)
            self.screen.blit(msg, msg.get_rect(centerx=sx + sw // 2, y=sy))
        elif running:
            msg = self.font_label.render("Searching...", True, ACCENT)
            self.screen.blit(msg, msg.get_rect(centerx=sx + sw // 2, y=sy))
        elif not self.grid.start or not self.grid.end:
            msg = self.font_small.render("Set Start & End to begin", True, TEXT_DIM)
            self.screen.blit(msg, msg.get_rect(centerx=sx + sw // 2, y=sy))

        # ── Legend ─────────────────────────────────────────────────────────────
        legend_y = self.win_h - 155
        pygame.draw.line(self.screen, DIVIDER, (sx, legend_y - 8), (sx + sw, legend_y - 8), 1)
        self._label("LEGEND", sx, legend_y, TEXT_DIM, self.font_small)
        legend_y += 18
        items = [
            ("Start",    C_START),
            ("End",      C_END),
            ("Wall",     C_WALL),
            ("Visited",  C_VISITED),
            ("Frontier", C_FRONTIER),
            ("Path",     C_PATH),
        ]
        col_w = sw // 2
        for i, (lbl, col) in enumerate(items):
            lx = sx + (i % 2) * col_w
            ly = legend_y + (i // 2) * 22
            pygame.draw.rect(self.screen, col, (lx, ly + 3, 12, 12), border_radius=3)
            self._label(lbl, lx + 16, ly, TEXT_MAIN, self.font_small)

        tip = self.font_small.render("Right-click grid = erase", True, TEXT_DIM)
        self.screen.blit(tip, tip.get_rect(centerx=sx + sw // 2, y=self.win_h - 20))
