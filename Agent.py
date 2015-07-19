# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image, ImageChops, ImageMath, ImageOps, ImageStat, ImageFilter
import math, operator
from itertools import izip


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an integer representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These integers
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName() (as Strings).
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(int givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will *not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self, problem):

        # TODO: Implement voting
        print "problem name: " + problem.name
        # print "problem type: " + problem.problemType
        problem_figures = {}

        STRATEGIES = []

        for figureName in problem.figures:
            figure = problem.figures[figureName]
            image = Image.open(figure.visualFilename).convert('1')

            problem_figures[figureName] = image
        print self.chooseStrategy(problem_figures)
        # DEBUG ***********************************************
        if problem.name == 'Basic Problem D-06':  # or problem.name == 'Basic Problem D-04':

            figures_a_ = problem_figures['A']
            figures_b_ = problem_figures['B']
            figures_c_ = problem_figures['C']
            figures_d_ = problem_figures['D']
            figures_e_ = problem_figures['E']
            figures_f_ = problem_figures['F']
            figures_g_ = problem_figures['G']
            figures_h_ = problem_figures['H']


            rowAB= ImageChops.subtract(figures_a_, figures_b_)
            rowCAB= ImageChops.subtract(rowAB, figures_c_)


            rowDE= ImageChops.subtract(figures_d_, figures_e_)
            rowDEF= ImageChops.subtract(rowDE, figures_f_)

            rowCAB.show()
            rowDEF.show()




        #########**************************************
        if self.chooseStrategy(problem_figures) == 'row_equals':
            for i in range(1, 9):
                if self.areEqual(problem_figures['H'], problem_figures[str(i)])[0]:
                    print ("answer", int(i))
                    return int(i)
        elif self.chooseStrategy(problem_figures) == 'one_of_each':
            return self.applyOnfOfEachStrategy(problem_figures)
        elif self.chooseStrategy(problem_figures) == 'one_cancels':

            return self.applyOneCancelsStrategy(problem_figures)

        print ("dunno why?")
        return -1

    @staticmethod
    def areEqual(im1, im2):
        dif = sum(abs(p1 - p2) for p1, p2 in zip(im1.getdata(), im2.getdata()))
        ncomponents = im1.size[0] * im1.size[1] * 3
        dist = (dif / 255.0 * 100) / ncomponents
        im1__getcolors = im1.getcolors()
        im2_getcolors = im2.getcolors()
        black1 = (10000, 0)
        if len(im1__getcolors) > 1:
            black, white = im1__getcolors

        else:
            if im1__getcolors[0][1] == 255:
                white = im1__getcolors
                black = (0, 0)
            else:
                black = im1__getcolors
                white = (0, 255)

        if len(im2_getcolors) > 1:
            black1, white1 = im2_getcolors
        else:
            if im2_getcolors[0][1] == 255:
                white1 = im2_getcolors
                black1 = (0, 0)
            else:
                black1 = im2_getcolors
                white1 = (0, 255)

        stats = {"dist": dist, "blk": abs(black[0] - black1[0]),"white": 0}


        return (dist < 1.1 and abs(black[0] - black1[0]) < 200 and abs(white[0] - white1[0] < 200)), stats

    def chooseStrategy(self, figures):
        # everyone is the same
        figures_a_ = figures['A']
        figures_b_ = figures['B']
        figures_c_ = figures['C']
        figures_d_ = figures['D']
        figures_e_ = figures['E']
        figures_f_ = figures['F']
        figures_g_ = figures['G']

        # overlays
        rowAB = ImageChops.add(figures_a_, figures_b_)
        rowBC = ImageChops.add(figures_b_, figures_c_)
        rowDE = ImageChops.add(figures_d_, figures_e_)
        rowEF = ImageChops.add(figures_e_, figures_f_)

        if self.areEqual(figures_a_, figures_b_)[0] and self.areEqual(figures_b_, figures_c_)[0]:
            if self.areEqual(figures_d_, figures_e_)[0] and self.areEqual(figures_e_, figures_f_)[0]:
                return 'row_equals'
        elif self.areEqual(figures_a_, figures_d_)[0] or self.areEqual(figures_a_, figures_e_)[0] or \
                self.areEqual(figures_a_,
                              figures_f_)[0]:
            if self.areEqual(figures_b_, figures_d_)[0] or self.areEqual(figures_b_, figures_e_) or self.areEqual(
                    figures_b_, figures_f_)[0]:
                return 'one_of_each'
        elif self.areEqual(rowAB, rowBC)[0] and self.areEqual(rowDE, rowEF)[0]:
            return "one_cancels"


    def applyOnfOfEachStrategy(self, problem_figures):
        if self.areEqual(problem_figures['A'], problem_figures['G'])[0] or self.areEqual(problem_figures['A'],
                                                                                         problem_figures['H'])[0]:
            if self.areEqual(problem_figures['B'], problem_figures['G'])[0] or self.areEqual(problem_figures['B'],
                                                                                             problem_figures['H'][0]):
                if self.areEqual(problem_figures['C'], problem_figures['G'])[0] or self.areEqual(problem_figures['C'],
                                                                                                 problem_figures['H'])[
                    0]:
                    print  "need to chose another strategy"
                else:
                    print "missing C"
                    missing_figure = problem_figures['C']
            else:
                print "missing B"
                missing_figure = problem_figures['B']
        else:
            missing_figure = problem_figures['A']

        for i in range(1, 9):
            print 'A &', i
            if self.areEqual(missing_figure, problem_figures[str(i)])[0]:
                print ("found answer", i)

                return int(i)

    def applyOneCancelsStrategy(self, problem_figures):
        rowCF = ImageChops.add(problem_figures["C"], problem_figures["F"])
        rowGH = ImageChops.add(problem_figures["G"], problem_figures["H"])
        rowHF = ImageChops.multiply(problem_figures["H"], problem_figures["F"])
        answers ={}

        for i in range(1, 9):
            print i
            candidate = ImageChops.add(rowCF, problem_figures[str(i)])
            candidate2 = ImageChops.add(rowGH, problem_figures[str(i)])

            if self.areEqual(rowCF, candidate)[0] and self.areEqual(rowGH, candidate2)[0]:
                print ("answer", int(i))
                answers[i]= problem_figures[str(i)]

        print answers, len(answers)
        if len(answers)!=1:
            for i in range(1, 9):
                print "try one more:", i
                if self.areEqual(rowHF, problem_figures[str(i)])[0] :
                    return int(i)
        else:
            return answers.keys()[0]


        return -1;

    def __compareImages(self, img1, img2):
        common = Image.new("1", img1.size, "white")

        delta = Image.new("1", img1.size, "white")
        for x in range(0, common.size[1]):
            for y in range(0, common.size[0]):
                p1 = img1.getpixel((x, y))
                p2 = img2.getpixel((x, y))
                if (p1 == 0 and p2 == 0):
                    common.putpixel((x, y), 0)

                elif p1 == 255 and p2 == 255:
                    common.putpixel((x, y), 255)

                else:

                    delta.putpixel((x, y), 0)

        return common, delta

    def invertGrayScaleImage(self, image):
        inverted = Image.new("1", image.size, "white")
        for x in range(0, image.size[1]):
            for y in range(0, image.size[0]):
                p1 = image.getpixel((x, y))
                if (p1 == 0):
                    inverted.putpixel((x, y), 255)
                else:
                    inverted.putpixel((x, y), 0)

        return inverted


    def paint_edge(im, thickness, value=0):
        new = im.copy()
        x_max, y_max, x_mid, y_mid = new.size[0], new.size[1], new.size[0] // 2, new.size[1] // 2
        count = 0

        ranges = (
            (range(x_mid),        range(y_mid+1)),
            (range(x_mid),        range(y_max-1, y_mid, -1)),
            (range(x_mid, x_max), range(y_mid+1)),
            (range(x_mid, x_max), range(y_max-1, y_mid, -1)),
        )
        for r1, r2 in ranges:
            for x in r1:
                started = False
                for y in r2:
                    pix = new.getpixel((x, y))
                    if pix == 255 and not started:
                        count = 0
                        continue
                    if count < thickness:
                        count += 1
                        new.putpixel((x,y), value)
                        started = True

        for r1, r2 in ranges:
            for y in r1:
                started = False
                for x in r2:
                    pix = new.getpixel((x, y))
                    if pix == 255 and not started:
                        count = 0
                        continue
                    if count < thickness:
                        count += 1
                        new.putpixel((x,y), value)
                        started = True
        return new
