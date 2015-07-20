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
from ImageUtils import ImageUtils
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
    imageUtils =ImageUtils()
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
        strategy = self.chooseStrategy(problem_figures)
        print strategy
        # DEBUG ***********************************************
        if problem.name == 'Basic Problem D-05':  # or problem.name == 'Basic Problem D-04':

            figures_a_ = problem_figures['A']
            figures_b_ = problem_figures['B']
            figures_c_ = problem_figures['C']
            figures_d_ = problem_figures['D']
            figures_e_ = problem_figures['E']
            figures_f_ = problem_figures['F']
            figures_g_ = problem_figures['G']
            figures_h_ = problem_figures['H']
            figures_1_ = problem_figures['1']
            figures_3_ = problem_figures['3']
            figures_4_ = problem_figures['4']
            figures_8_ = problem_figures['8']
            figures_7_ = problem_figures['7']
            imageUtils =ImageUtils()

            print self.imageUtils.isEqual(figures_g_, figures_4_)
            print self.imageUtils.isEqual(figures_g_, figures_3_)
            print self.imageUtils.isEqual(figures_g_, figures_8_)
            print self.imageUtils.isEqual(figures_g_, figures_7_)



            inverted =self.imageUtils.invertGrayScaleImage(problem_figures['A'])
            sumOfTwo = ImageChops.add(problem_figures['G'], inverted)

            inverted.show()
            sumOfTwo.show()

            # inverted.show()





            # rowAB= ImageChops.multiply(figures_a_, figures_d_)
            # rowCAB= ImageChops.multiply(rowAB, figures_g_)
            #
            #
            # rowDE= ImageChops.multiply(figures_b_, figures_e_)
            # rowDEF= ImageChops.multiply(rowDE, figures_h_)
            #
            # rowCAB.show()
            # rowDEF.show()
            #
            # print self.areEqual(rowCAB, rowDEF)




        #########**************************************
        if strategy == 'row_equals':
            for i in range(1, 9):
                if self.areEqual(problem_figures['H'], problem_figures[str(i)])[0]:
                    print ("answer", int(i))
                    return int(i)
        elif self.chooseStrategy(problem_figures) == 'one_of_each':
            return self.applyOnfOfEachStrategy(problem_figures)
        elif strategy == 'one_cancels':
            return self.applyOneCancelsStrategy(problem_figures)
        elif strategy == 'cancel_out':
            return self.applyCancelOutStrategy(problem_figures)
        else:
            return self.pick_the_one_not_seen(problem_figures)


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



        stats = {"dist": dist, "blk": abs(black[0] - black1[0])}


        return (dist<1.1 and abs(black[0]-black1[0])<100 and abs(white[0]-white1[0]<100)), stats


    def chooseStrategy(self, figures):
        # everyone is the same
        figures_a_ = figures['A']
        figures_b_ = figures['B']
        figures_c_ = figures['C']
        figures_d_ = figures['D']
        figures_e_ = figures['E']
        figures_f_ = figures['F']
        figures_g_ = figures['G']
        figures_h_ = figures['H']

        # overlays
        rowAB = ImageChops.add(figures_a_, figures_b_)
        rowBC = ImageChops.add(figures_b_, figures_c_)
        rowDE = ImageChops.add(figures_d_, figures_e_)
        rowEF = ImageChops.add(figures_e_, figures_f_)


        colAD =ImageChops.multiply(figures_a_, figures_d_)
        colADG= ImageChops.multiply(colAD, figures_g_)

        colBE =ImageChops.multiply(figures_b_, figures_e_)
        colBEH= ImageChops.multiply(colBE, figures_h_)

        if self.areEqual(figures_a_, figures_b_)[0] and self.areEqual(figures_b_, figures_c_)[0]:
            if self.areEqual(figures_d_, figures_e_)[0] and self.areEqual(figures_e_, figures_f_)[0]:
                return 'row_equals'
        elif ((self.areEqual(figures_a_, figures_d_)[0] or self.areEqual(figures_a_, figures_e_)[0] or self.areEqual(figures_a_,figures_f_)[0]) \
                and (self.areEqual(figures_b_, figures_d_)[0] or self.areEqual(figures_b_, figures_e_)[0] or self.areEqual(figures_b_, figures_f_)[0]) \
                and (self.areEqual(figures_c_, figures_d_)[0] or self.areEqual(figures_c_, figures_e_)[0] or self.areEqual(figures_c_, figures_f_)[0])):
            print "I should not be here"
            return 'one_of_each'
        elif self.areEqual(rowAB, rowBC)[0] and self.areEqual(rowDE, rowEF)[0]:
            return "one_cancels"

        elif self.areEqual(colADG, colBEH)[0]:
            return "cancel_out"



    def applyOnfOfEachStrategy(self, problem_figures):
        if self.areEqual(problem_figures['A'], problem_figures['G'])[0] or self.areEqual(problem_figures['A'],problem_figures['H'])[0]:
            if self.areEqual(problem_figures['B'], problem_figures['G'])[0] or self.areEqual(problem_figures['B'],problem_figures['H'][0]):
                if self.areEqual(problem_figures['C'], problem_figures['G'])[0] or self.areEqual(problem_figures['C'],problem_figures['H'])[0]:
                    print  "need to chose another strategy"
                else:
                    miss ="c"
                    print "missing C"
                    missing_figure ='C'
            else:
                print "missing B"
                miss ="b"
                missing_figure ='B'
        else:
            print "missing A"
            miss ="a"
            missing_figure = "A"

        for i in range(1, 9):
            print 'A &', i
            print self.areEqual(problem_figures[missing_figure], problem_figures[str(i)])
            if self.areEqual(problem_figures[missing_figure], problem_figures[str(i)])[0]:
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

                answers[i]= problem_figures[str(i)]

        print answers, len(answers)
        if len(answers)!=1:
            return self.pick_the_one_not_seen(problem_figures)
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



    def pick_the_one_not_seen(self, figures):
        figs =["A","B","C","D","E","F","G", "H"]
        answers=[1,2,3,4,5,6,7,8]
        for fig in figs:
            print fig
            for i in range(1,9):
                print i
                #
                if self.areEqual(figures[fig], figures[str(i)])[0] :
                    print "answer:",answers
                    if i in answers:
                        print ("removing", i)
                        answers.remove(i)

        print(answers)
        if len(answers)>0:
            return answers[0]
        else:
            return -1

    def applyCancelOutStrategy(self,problem_figures):
         figures_a_ = problem_figures['A']
         figures_b_ = problem_figures['B']
         figures_c_ = problem_figures['C']
         figures_d_ = problem_figures['D']
         figures_e_ = problem_figures['E']
         figures_f_ = problem_figures['F']
         figures_g_ = problem_figures['G']

         figures_h_ = problem_figures['H']

         colAD= ImageChops.multiply(figures_a_, figures_d_)
         colADG= ImageChops.multiply(colAD, figures_g_)
         colCF= ImageChops.multiply(figures_c_, figures_f_)

         for i in range(1, 9):
             print i
             candidate = ImageChops.multiply(colCF, problem_figures[str(i)])
             if self.areEqual(candidate,colADG)[0]:
                 return int(i)

         # if len(self.pick_the_one_not_seen(problem_figures))==1:
         #     return self.pick_the_one_not_seen(problem_figures)[0]

         return -1

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
