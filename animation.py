from manim import *


class AcousticSimulationExplanation(ThreeDScene):
    def construct(self):
        # Source dot and label
        source = Dot([3, 0, 1], 0.1, fill_opacity=1, color=RED)
        source_label = Text("Source", font_size=24).next_to(source, UP)
        self.add(source, source_label)

        # Microphone dots and labels
        mic1 = Dot([-2, 1, 1], 0.1, fill_opacity=1, color=WHITE)
        mic1_label = Text("mic array 1", font_size=16).next_to(mic1, UP)
        mic2 = Dot([-3, -1, 1], 0.1, fill_opacity=1, color=WHITE)
        mic2_label = Text("mic array 2", font_size=16).next_to(mic2, UP)
        mic3 = Dot([-2, -2, 1], 0.1, fill_opacity=1, color=WHITE)
        mic3_label = Text("mic array 3", font_size=16).next_to(mic3, UP)

        self.add(mic1, mic1_label)
        self.add(mic2, mic2_label)
        self.add(mic3, mic3_label)

        num_circles = 4
        max_radius = 70

        animations = []

        for _ in range(num_circles):
            growing_circle = Circle(
                radius=0.1, color=YELLOW, fill_color=BLUE, fill_opacity=0.1
            )
            growing_circle.move_to(source)
            growing_circle.set_stroke(width=2)

            animation = (
                growing_circle.animate.scale(max_radius)
                .set_stroke(opacity=0.001)
                .set_fill(opacity=0.001)
            )
            animations.append(animation)

            self.add(growing_circle)

        self.play(LaggedStart(*animations, lag_ratio=0.5), run_time=14)

        # Draw lines and labels
        self.add_lines_with_labels(source, mic1, "time \(t_1\)")
        self.add_lines_with_labels(source, mic2, "time \(t_2\)")
        self.add_lines_with_labels(source, mic3, "time \(t_3\)")

        self.move_camera(zoom=2.5, frame_center=mic1.get_center(), run_time=2)

        point1_dot = Dot3D(
            [mic1.get_center()[0], mic1.get_center()[1], mic1.get_center()[2] + 1],
            color=RED,
        )
        point1_label = Text("mic 1", font_size=18, color=GREEN).next_to(
            point1_dot, RIGHT
        )
        point2_dot = Dot3D(
            [mic1.get_center()[0], mic1.get_center()[1] + 1, mic1.get_center()[2]],
            color=GREEN,
        )
        point2_label = Text("mic 2", font_size=18, color=GREEN).next_to(
            point2_dot, RIGHT
        )
        point3_dot = Dot3D(
            [mic1.get_center()[0] + 1, mic1.get_center()[1], mic1.get_center()[2]],
            color=BLUE,
        )
        point3_label = Text("mic 3", font_size=18, color=GREEN).next_to(
            point3_dot, RIGHT
        )

        axes = ThreeDAxes()
        axes.move_to(mic1)

        self.remove(mic2, mic2_label, mic3, mic3_label)

        self.add(axes)
        self.play(
            FadeIn(
                point1_dot,
                point2_dot,
                point3_dot,
            )
        )

        self.remove(mic1, mic1_label)
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, run_time=2)
        self.add_fixed_orientation_mobjects(point1_label, point2_label, point3_label)
        self.play(
            FadeIn(
                point1_label,
                point2_label,
                point3_label,
            )
        )
        text3d = Text(
            "Each array can locate the sound source independently & utilizes at least 3 mics.",
            font_size=18,
        )
        self.add_fixed_in_frame_mobjects(text3d)
        text3d.to_edge(DOWN + RIGHT)

        self.wait(2)

    def add_lines_with_labels(self, start_point, end_point, label):
        line = Line(start_point.get_center(), end_point.get_center(), color=YELLOW)
        brace = Brace(line, direction=line.copy().rotate(-PI / 2).get_unit_vector())
        line_text = brace.get_text(label)
        self.play(Create(line), FadeIn(brace))
        self.play(FadeIn(line_text))
        self.wait(1)
        self.remove(line, brace, line_text)
