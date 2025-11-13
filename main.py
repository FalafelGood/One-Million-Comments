from manim import *
import numpy as np
import os
import json
from scipy.stats import linregress

class ChannelRatings:
    def __init__(self, ratings=None):
        self.ratings = []
        if ratings is not None:
            self.ratings = ratings
        else:
            with os.scandir('channel-ratings') as files:
                for idx, file in enumerate(files):
                    with open(file, 'r') as open_file:
                        data = json.load(open_file)
                        self.ratings.append(data)
        self.num_ratings = len(self.ratings)

    def __str__(self):
        return str(f"ChannelRatings object with {self.num_ratings} ratings")

    def get_names(self):
        names = []
        for channel in self.ratings:
            names.append(channel["channel-name"])
        return names

    def get_comment_counts(self):
        comment_counts = []
        for channel in self.ratings:
            comment_counts.append(channel["num-comments-analyzed"])
        return comment_counts

    def get_formatted_names(self, color):
        """Returns a VGroup of formatted names (with comment count) so we can pretty-print them in our Manim scene"""
        names = self.get_names()
        comment_counts = self.get_comment_counts()
        formatted_names = [Text(name + " (" + str(num_comments) + ")", color=color, font_size=18) for name, num_comments in zip(names, comment_counts)]
        names_group = VGroup(*formatted_names)
        names_group.arrange(DOWN, buff=0.5, aligned_edge=RIGHT)
        names_group.to_edge(RIGHT).shift(UP*1.5)
        return names_group

    def sort_by(self, arg, ascending = True):
        """Sort ratings by the specified argument in ascending or descending order"""
        self.ratings = sorted(self.ratings, key=lambda x: x[arg], reverse=not(ascending))
        return

    def get_channels_by_tag(self, tag):
        """linear scan to find channels with a given tag. Returns a ChannelRatings object"""
        matching_channels = []
        matching_indecies = []
        for idx, channel in enumerate(self.ratings):
            if (tag in channel["tags"]):
                matching_channels.append(channel)
                matching_indecies.append(idx)
        return ChannelRatings(matching_channels), matching_indecies

    def get_coords(self):
        """Returns a list of tuples where the first argument is kindness and the second argument is volatility"""
        return [(channel['kindness'], channel['volatility']) for channel in self.ratings]


#################
# GLOBAL ASSETS #
#################

ratings = ChannelRatings()
ratings.sort_by("kindness")
coords = ratings.get_coords()

ax = Axes(
    x_range=[-0.3, 1, 0.1],
    y_range=[1, 1.5, 0.1],
    axis_config={"include_numbers": True, "numbers_to_exclude": [1]}
)

labels = ax.get_axis_labels(
    Text("Kindness").scale(0.45), Text("Volatility").scale(0.45)
)

# Data points
dots = [Dot(ax.c2p(x,y), radius=0.06, color=BLUE, stroke_width=0, stroke_color=WHITE) for x, y in coords]


###################
# UTILITY SCRIPTS #
###################

def get_dots_and_names_by_tag(tag, color):
    tagged_channels, tagged_indices = ratings.get_channels_by_tag(tag)
    tagged_dots = [dots[idx] for idx in tagged_indices]
    formatted_names = tagged_channels.get_formatted_names(color)
    return tagged_dots, formatted_names

##########
# SCENES #
##########

class APIScene(Scene):
    def construct(self):
        # Start with the acronym "API"
        acronym = Text("A.P.I.", font_size=72, color=BLUE, font="Comic Relief")
        self.play(Write(acronym))
        self.wait(0.5)
        
        # Create the expanded text
        expanded = Text("Application Programming Interface", font_size=48, color=WHITE, font="Comic Relief")
        
        # Transform the acronym into the expanded text
        self.play(ReplacementTransform(acronym, expanded), run_time=1.5)
        self.wait(2)
        
        # Fade out
        self.play(FadeOut(expanded))

class ExplainVader(Scene):
    def construct(self):
        comment_size=24
        font="Comic Relief"
        positive_comment = Text("\"Hey, great video! :-)\"", font_size=comment_size, color=GREEN_C, font=font)
        neutral_comment = Text("\"This video is ok.\"", font_size=comment_size, color=YELLOW_D, font=font)
        negative_comment = Text("\"Bro this sucks\"", font_size=comment_size, color=RED, font=font)
        positive_stats = "{'neg': 0.0, 'neu': 0.23, 'pos': 0.77}"
        neutral_stats = "{'neg': 0.0, 'neu': 0.577, 'pos': 0.423}"
        negative_stats = "{'neg': 0.556, 'neu': 0.444, 'pos': 0.0}"
        
        t0 = Table(
            [[positive_stats],
            [neutral_stats],
            [negative_stats]],
            row_labels=[positive_comment, neutral_comment, negative_comment],
            col_labels=[Text("Vader Score", font="Comic Relief")],
            top_left_entry=Text("Comment", font="Comic Relief"),
            element_to_mobject_config={"font_size": 20, "font": "Ubuntu Mono"})
        self.play(t0.create())
        self.wait(2)

class DefinePNZ(Scene):
    def construct(self):
        # Create separate text objects for each line
        line1 = Tex(r"Define:", font_size=48)
        line2 = Tex(r"$P$ = Average Weighted Positivity", font_size=48, color=GREEN_C)
        line3 = Tex(r"$Z$ = Average Weighted Neturality", font_size=48, color=YELLOW_D)
        line4 = Tex(r"$N$ = Average Weighted Negativity", font_size=48, color=RED)
        
        # Group the lines and arrange them vertically with increased spacing
        text_group = VGroup(line1, line2, line3, line4)
        text_group.arrange(DOWN, buff=0.8)
        text_group.move_to(ORIGIN)
        
        # Animate the text appearing
        self.play(Write(text_group))
        self.wait(2.5)
        
        # Fade out
        self.play(FadeOut(text_group))

class Definitions(Scene):
    def construct(self):
        # Create the math expression with white as default color
        eq1 = MathTex(r"K = \frac{P-N}{P+N}", font_size=72, color=WHITE)
        eq1[0][2].set_color(GREEN)
        eq1[0][6].set_color(GREEN)
        eq1[0][4].set_color(RED)
        eq1[0][8].set_color(RED)
        self.play(Write(eq1))
        self.wait(3)
        
        eq2 = MathTex(r"K = -1", font_size=72, color=WHITE)
        eq2[0][2].set_color(RED)
        eq2[0][3].set_color(RED)
        self.play(ReplacementTransform(eq1, eq2))
        self.wait(1)

        eq3 = MathTex(r"K = 1", font_size=72, color=WHITE)
        eq3[0][2].set_color(GREEN)
        self.play(ReplacementTransform(eq2, eq3))
        self.wait(1)

        eq4 = MathTex(r"K = 0", font_size=72, color=WHITE)
        eq4[0][2].set_color(YELLOW_D)
        self.play(ReplacementTransform(eq3, eq4))
        self.wait(1)

class DefineVolatility(Scene):
    # 1/(Z + abs(P-N))
    def construct(self):
        eq1 = MathTex(r"V = \frac{1}{Z + |P-N|}", font_size=72, color=WHITE)
        eq1[0][4].set_color(YELLOW_D)
        eq1[0][7].set_color(GREEN)
        eq1[0][9].set_color(RED)
        eq2 = MathTex(r"V = \frac{1}{\epsilon}", font_size=72, color=WHITE)
        self.play(Write(eq1))
        self.wait(3)
        self.play(ReplacementTransform(eq1, eq2))
        self.wait(3)
        # For some reason we have to redefine eq1... 
        eq1 = MathTex(r"V = \frac{1}{Z + |P-N|}", font_size=72, color=WHITE)
        eq1[0][4].set_color(YELLOW_D)
        eq1[0][7].set_color(GREEN)
        eq1[0][9].set_color(RED)
        self.play(ReplacementTransform(eq2, eq1))
        self.wait(3)

        eq3 = MathTex(r"V = 1", font_size=72, color=WHITE)
        self.play(ReplacementTransform(eq1, eq3))
        self.wait(3)

        eq4 = MathTex(r"V = \frac{1}{Z + |P-N|} - 1", font_size=72, color=WHITE)
        eq4[0][4].set_color(YELLOW_D)
        eq4[0][7].set_color(GREEN)
        eq4[0][9].set_color(RED)
        self.play(ReplacementTransform(eq3, eq4))
        self.wait(3)

        eq1 = MathTex(r"V = \frac{1}{Z + |P-N|}", font_size=72, color=WHITE)
        eq1[0][4].set_color(YELLOW_D)
        eq1[0][7].set_color(GREEN)
        eq1[0][9].set_color(RED)
        self.play(ReplacementTransform(eq4, eq1))
        self.wait(3)

class ScatterPlot(Scene):
    def construct(self):

        # Draw the axes 
        self.play(Write(ax))
        self.wait()
        self.play(Write(labels))
        self.wait()

        # Draw all dots with a nice little sweep
        self.play(LaggedStart(*[Write(dot) for dot in dots], lag_ratio=.01))
        self.wait()

        # Change the dot ratio and then change it back:
        # self.play(LaggedStart(*[dot.animate.scale(0.5) for dot in dots], lag_ratio=.01))
        # self.play(LaggedStart(*[dot.animate.scale(1/0.5) for dot in dots], lag_ratio=.01))
        # self.wait()

        # Perform linear regression on datapoints
        regression = linregress([c[0] for c in coords], [c[1] for c in coords])
        m = regression.slope
        b = regression.intercept

        # Plot line of best fit
        x1 = -0.2
        x2 = 0.85
        y1 = m*x1 + b
        y2 = m*x2 + b
        start_point = ax.c2p(x1, y1)
        end_point = ax.c2p(x2, y2)
        line = Line(start_point, end_point)
        self.play(Write(line))
        self.wait()

        print("m")

        # Add some text to report on the curve
        tex_m = Tex(fr"m = {round(m, 3)}", font_size=56)
        tex_b = Tex(fr"b = {round(b, 3)}", font_size=56)
        tex_b.shift(DOWN)
        line_info = VGroup(tex_m, tex_b)
        line_info.shift(UP*2)
        line_info.shift(RIGHT*2)
        self.play(AnimationGroup(Write(line_info)))
        self.wait()
        self.play(AnimationGroup(Unwrite(line_info), Unwrite(line)))
        self.wait()

        # Draw ellipse in lower right-hand corner
        # ellipse = Ellipse(width=4.5, height=1).rotate(-60).shift(RIGHT*3).shift(DOWN*2)
        # self.play(Write(ellipse))
        # self.wait()
        # self.play(Unwrite(ellipse))
        # self.wait()


class FirstAnalysis(Scene):
    def animate_dots(self, dots, dot_color, names, unwrite=True):
        self.play(AnimationGroup(*[dot.animate.set_fill(dot_color).scale(1.3) for dot in dots]))
        self.play(Write(names))
        self.wait()
        self.play(Unwrite(names))
        self.wait()
        if unwrite:
            self.play(AnimationGroup(*[dot.animate.set_fill(GRAY_D).scale(1/1.3) for dot in dots]))
        return

    def construct(self):
        # Add (don't draw) the axes and data points
        self.add(ax)
        self.add(labels)
        self.add(Group(*dots))
        self.wait()

        catholic_dots, catholic_names = get_dots_and_names_by_tag("catholic", RED)
        atheist_dots, atheist_names = get_dots_and_names_by_tag("atheist", BLUE)
        protestant_dots, protestant_names = get_dots_and_names_by_tag("protestant", GOLD_B)
        muslim_dots, muslim_names = get_dots_and_names_by_tag("islam", GREEN)
        anime_dots, anime_names = get_dots_and_names_by_tag("anime", WHITE)
        queer_dots, queer_names = get_dots_and_names_by_tag("queer", PINK)

        catholic_names.shift(0.5*DOWN)

        # Wash out dots to gray color
        self.play(LaggedStart(*[dot.animate.set_fill(GRAY_D) for dot in dots], lag_ratio=.01))

        # Catholic channels
        self.animate_dots(catholic_dots, PURE_RED, catholic_names, unwrite=False)
        # self.play(AnimationGroup(*[dot.animate.set_fill(PURE_RED).scale(1.3) for dot in catholic_dots]))
        # self.play(Write(catholic_names))
        # self.wait()
        # self.play(Unwrite(catholic_names))
        # self.wait()

        # Atheist channels
        self.animate_dots(atheist_dots, PURE_BLUE, atheist_names)
        # self.play(AnimationGroup(*[dot.animate.set_fill(BLUE_C).scale(1.3) for dot in atheist_dots]))
        # self.wait()
        # self.play(Write(atheist_names))
        # self.wait()
        # self.play(Unwrite(atheist_names))
        # self.wait()

        ellipse = Ellipse(width=4.5, height=1).rotate(-60).shift(RIGHT*3).shift(DOWN*2)
        self.play(Write(ellipse))
        self.wait()
        self.play(Unwrite(ellipse))
        self.wait()

        self.animate_dots(protestant_dots, GOLD_B, protestant_names)
        self.animate_dots(muslim_dots, GREEN_D, muslim_names)

        # Gay channels
        triangles = [Triangle(color=PINK).scale(0.1).move_to(dot.get_center()) for dot in queer_dots]
        self.play(AnimationGroup(*[Transform(dot, triangle) for dot, triangle in zip(queer_dots, triangles)]))
        self.play(Write(queer_names))
        self.wait()
        self.play(Unwrite(queer_names))
        self.wait()


class SecondAnalysis(Scene):
    def construct(self):
        # Add (don't draw) the axes and data points
        self.add(ax)
        self.add(labels)
        for dot in dots:
            dot.set_fill(GRAY_D)
        self.add(Group(*dots))
        self.wait()

        left_dots, left_names = get_dots_and_names_by_tag("left", BLUE)
        right_dots, right_names = get_dots_and_names_by_tag("right", RED)


        self.play(AnimationGroup(*[dot.animate.set_fill(PURE_RED).scale(1.3) for dot in right_dots]))
        self.play(AnimationGroup(*[dot.animate.set_fill(BLUE).scale(1.3) for dot in left_dots]))
        self.wait(2)

        right_names.shift(LEFT*3.5)
        left_names.shift(DOWN*0.5)
        left_and_right = VGroup(right_names, left_names)
        self.play(Write(left_and_right))
        self.wait()
        self.play(Unwrite(left_and_right))
        self.wait()


class ThirdAnalysis(Scene):
    def construct(self):
        self.add(ax)
        self.add(labels)
        for dot in dots:
            dot.set_fill(GRAY_D)
        self.add(Group(*dots))
        self.wait()

        chess_dots, chess_names = get_dots_and_names_by_tag("chess", WHITE)
        education_dots, education_names = get_dots_and_names_by_tag("education", GREEN)
        popular_dots, popular_names = get_dots_and_names_by_tag("popular", PINK)

        education_names.shift(DOWN*0.5)

        squares = [Square(side_length=0.15).move_to(dot.get_center()) for dot in chess_dots]
        self.play(AnimationGroup(*[Transform(dot, square) for dot, square in zip(chess_dots, squares)]))
        self.play(Write(chess_names))
        self.wait()
        self.play(Unwrite(chess_names))
        self.wait()


        self.play(AnimationGroup(*[dot.animate.set_fill(GREEN_C).scale(1.3) for dot in education_dots]))
        self.play(Write(education_names))
        self.wait()
        self.play(AnimationGroup(*[dot.animate.set_fill(GRAY_D).scale(1/1.3) for dot in education_dots]))
        self.play(Unwrite(education_names))


