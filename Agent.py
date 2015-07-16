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
from PIL import Image, ImageChops, ImageMath,ImageOps, ImageStat, ImageFilter
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
    def Solve(self,problem):

        #
        print "problem name: " + problem.name
        # print "problem type: " + problem.problemType
        problem_figures={}

        STRATEGIES=[]

        for figureName in problem.figures:

            figure = problem.figures[figureName]
            image = Image.open(figure.visualFilename).convert('1')

            problem_figures[figureName] = image
        print self.chooseStrategy(problem_figures)
        if self.chooseStrategy(problem_figures)=='row_equals':
           for i in range(1, 9):
               if self.areEqual(problem_figures['H'], problem_figures[str(i)]):
                    return int(i)
        elif self.chooseStrategy(problem_figures)=='one_of_each':
            self.applyOnfOfEachStrategy(problem_figures)

        print ("dunno why?")
        return -1

    @staticmethod
    def areEqual(im1, im2):
        dif = sum(abs(p1-p2) for p1,p2 in zip(im1.getdata(), im2.getdata()))
        ncomponents = im1.size[0] * im1.size[1] * 3
        dist =(dif / 255.0 * 100) / ncomponents
        im1__getcolors = im1.getcolors()
        im2_getcolors = im2.getcolors()
        if  len(im1__getcolors)>1  and  len(im2_getcolors)>1:
            black, white = im1__getcolors
            black1, white1 = im2_getcolors
        else:
            if im1__getcolors[0][1]==255:
                white =im1__getcolors
            else:
                black=im1__getcolors

            if im2_getcolors[0][1]==255:
                white1 =im2_getcolors
            else:
                black1=im2_getcolors


            # print black[0],  black1[0]
            # print white[0], white1[0]
            #
            # print dist
            # print black==black1
            # print white==white1
        return (dist<1.1 and abs(black[0]-black1[0])<100 and abs(white[0]-white1[0]<100))

    def chooseStrategy(self, figures):
        # everyone is the same
        figures_a_ = figures['A']
        figures_b_ = figures['B']
        figures_c_ = figures['C']
        figures_d_ = figures['D']
        figures_e_ = figures['E']
        figures_f_ = figures['F']
        if self.areEqual(figures_a_, figures_b_) and self.areEqual(figures_b_, figures_c_):
            if self.areEqual(figures_d_, figures_e_) and self.areEqual(figures_e_, figures_f_):
                return 'row_equals'
        elif self.areEqual(figures_a_, figures_d_) or self.areEqual(figures_a_, figures_e_) or self.areEqual(figures_a_, figures_f_):
            if self.areEqual(figures_b_, figures_d_) or self.areEqual(figures_b_, figures_e_) or self.areEqual(figures_b_, figures_f_):
                return 'one_of_each'


    def applyOnfOfEachStrategy(self, problem_figures):
        if self.areEqual(problem_figures['A'], problem_figures['G']) or self.areEqual(problem_figures['A'], problem_figures['H']):
            if self.areEqual(problem_figures['B'], problem_figures['G']) or self.areEqual(problem_figures['B'], problem_figures['H']):
                if self.areEqual(problem_figures['C'], problem_figures['G']) or self.areEqual(problem_figures['C'], problem_figures['H']):
                    print  "need to chose another strategy"
                else:
                    print "missing C"
                    missing_figure= problem_figures['C']
            else:
                print "missing B"
                missing_figure= problem_figures['B']
        else:
            missing_figure= problem_figures['A']
            print "missing A"
            print "comp", self.areEqual(problem_figures['A'], problem_figures['1'])
        for i in range(1, 9):
            print 'A &', i
            if self.areEqual(missing_figure, problem_figures[str(i)]):
                print ("found answer", i)
                problem_figures[str(i)].show()
                return int(i)

