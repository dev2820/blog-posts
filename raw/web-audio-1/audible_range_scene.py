from manim import *
import numpy as np

BG = "#101827"
TEXT = "#F4F7FB"
MUTED = "#9CAFC4"
CYAN = "#55D6BE"
BLUE = "#58C4DD"
GREEN = "#83C167"
YELLOW = "#FFD166"
ORANGE = "#FF9F43"
MONO = "Noto Sans CJK KR"


def x_for_frequency(freq, left, low_end, high_start, right):
    if freq <= 1000:
        return left + (freq / 1000) * (low_end - left)
    if freq >= 4000:
        return high_start + ((freq - 4000) / 21000) * (right - high_start)
    raise ValueError("1~4 kHz is omitted from the broken axis")


class AudibleRange(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("가청주파수는 얼마나 넓을까?", font=MONO, weight=BOLD,
                     font_size=34, color=TEXT)
        subtitle = Text("빈 구간을 생략한 선형 축에서 비교", font=MONO,
                        font_size=16, color=MUTED)
        title.to_edge(UP, buff=0.45)
        subtitle.next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(title, shift=DOWN * 0.2), FadeIn(subtitle), run_time=1.2)
        self.wait(0.8)

        left, low_end = -1.4, 1.2
        high_start, right = 1.65, 6.1
        axis_y = -2.45
        top_y = 1.72

        def break_wave(y, color, stroke_width=2):
            return ParametricFunction(
                lambda t: np.array([
                    low_end + (high_start - low_end) * t,
                    y + 0.055 * np.sin(4 * np.pi * t),
                    0,
                ]),
                t_range=[0, 1],
                color=color,
                stroke_width=stroke_width,
            )

        name_header = Text("비교 대상", font=MONO, font_size=13, color=MUTED)
        range_header = Text("대표 범위", font=MONO, font_size=13, color=MUTED)
        chart_header = Text("구간별 선형 축  ·  1~4 kHz 생략", font=MONO,
                            font_size=13, color=MUTED)
        name_header.move_to([-5.35, 2.22, 0])
        range_header.move_to([-2.72, 2.22, 0])
        chart_header.move_to([(left + right) / 2, 2.22, 0])

        grid = VGroup()
        ticks = VGroup()
        tick_labels = VGroup()
        tick_specs = [
            (0, "0"), (250, "250"), (500, "500"), (750, "750"), (1000, "1 kHz"),
            (4000, "4 kHz"), (10000, "10 kHz"), (15000, "15 kHz"),
            (20000, "20 kHz"), (25000, "25 kHz"),
        ]
        for freq, label in tick_specs:
            x = x_for_frequency(freq, left, low_end, high_start, right)
            grid.add(DashedLine([x, axis_y, 0], [x, 2.0, 0],
                                dash_length=0.07, color=MUTED,
                                stroke_width=1, stroke_opacity=0.22))
            ticks.add(Line([x, axis_y - 0.1, 0], [x, axis_y + 0.1, 0],
                           color=MUTED, stroke_width=2))
            tick_label = Text(label, font=MONO, font_size=12, color=MUTED)
            label_x = x - 0.1 if freq == 1000 else x + 0.1 if freq == 4000 else x
            tick_label.move_to([label_x, axis_y - 0.33, 0])
            tick_labels.add(tick_label)

        axis = VGroup(
            Line([left, axis_y, 0], [low_end, axis_y, 0], color=MUTED, stroke_width=2),
            break_wave(axis_y, MUTED),
            Line([high_start, axis_y, 0], [right, axis_y, 0], color=MUTED, stroke_width=2),
        )
        self.play(FadeIn(name_header), FadeIn(range_header), FadeIn(chart_header),
                  FadeIn(grid), Create(axis), Create(ticks), FadeIn(tick_labels), run_time=1.2)

        sounds = [
            ("가청주파수", "20 Hz–20 kHz", 20, 20000, CYAN),
            ("피아노 최저음 A0", "27.5 Hz", 27.5, 27.5, BLUE),
            ("전기 제품의 ‘웅—’ 소리", "60 Hz", 60, 60, GREEN),
            ("조율 기준음 A4", "440 Hz", 440, 440, YELLOW),
            ("피아노 최고음 C8", "4.19 kHz", 4186, 4186, ORANGE),
            ("오래된 TV의 ‘삐—’ 소리", "15.7 kHz", 15700, 15700, "#B98CFF"),
            ("개 휘파람", "20–25 kHz", 20000, 25000, "#FF6B9D"),
        ]
        rows = VGroup()
        separators = VGroup()
        row_y = top_y
        for name, value_text, low, high, color in sounds:
            label = Text(name, font=MONO, font_size=13, color=TEXT)
            value = Text(value_text, font=MONO, font_size=11, color=MUTED)
            label.move_to([-5.25, row_y, 0])
            value.move_to([-2.72, row_y, 0])

            start = x_for_frequency(low, left, low_end, high_start, right)
            end = x_for_frequency(high, left, low_end, high_start, right)
            if low == high:
                mark = Dot([start, row_y, 0], radius=0.08, color=color)
            elif low <= 1000 and high >= 4000:
                mark = VGroup(
                    Line([start, row_y, 0], [low_end, row_y, 0], color=color,
                         stroke_width=12, cap_style=CapStyleType.ROUND),
                    break_wave(row_y, color, stroke_width=3),
                    Line([high_start, row_y, 0], [end, row_y, 0], color=color,
                         stroke_width=12, cap_style=CapStyleType.ROUND),
                    Dot([start, row_y, 0], radius=0.055, color=color),
                    Dot([end, row_y, 0], radius=0.055, color=color),
                )
            else:
                mark = VGroup(
                    Line([start, row_y, 0], [end, row_y, 0], color=color,
                         stroke_width=12, cap_style=CapStyleType.ROUND),
                    Dot([start, row_y, 0], radius=0.055, color=color),
                    Dot([end, row_y, 0], radius=0.055, color=color),
                )
            rows.add(VGroup(label, value, mark))
            separators.add(Line([-6.75, row_y - 0.27, 0], [right, row_y - 0.27, 0],
                                color=MUTED, stroke_width=1, stroke_opacity=0.12))
            row_y -= 0.56

        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.08) for row in rows],
                              lag_ratio=0.12), FadeIn(separators), run_time=2.0)
        self.wait(1.0)

        caption = Text("※ 물결 표시는 1~4 kHz 구간의 생략을 뜻하며, 각 구간 안에서는 선형 축입니다.",
                       font=MONO, font_size=11, color=MUTED)
        caption.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(caption), run_time=0.7)
        self.wait(2.0)
