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
        # print "problem name: " + problem.name
        # print "problem type: " + problem.problemType
        problem_figures={}

        for figureName in problem.figures:

            figure = problem.figures[figureName]
            image = Image.open(figure.visualFilename).convert('1')
            #
            #problem_figures[figureName] = ImageOps.invert(image).filter(ImageFilter.GaussianBlur(2))
            problem_figures[figureName] = image

        #     # problem_figures[figureName].show()
        # print(problem_figures)
        # print("a==b", self.rmsdiff(problem_figures['A'], problem_figures['B']))


        if self.chooseStrategy(problem_figures)=='row equals':
           print self.chooseStrategy(problem_figures)
           for i in range(1, 9):
               print self.areEqual(problem_figures['H'], problem_figures[str(i)])
               if self.areEqual(problem_figures['H'], problem_figures[str(i)]):
                    print "comparing H nad "+ str(i), self.areEqual(problem_figures['H'], problem_figures[str(i)])
                    return int(i)


        return -1

    def areEqual(self, im1, im2):
        dif = sum(abs(p1-p2) for p1,p2 in zip(im1.getdata(), im2.getdata()))
        ncomponents = im1.size[0] * im1.size[1] * 3
        dist =(dif / 255.0 * 100) / ncomponents

        black, white = im1.getcolors()
        black1, white1 = im2.getcolors()
          # print black[0],  black1[0]
          #   print white[0], white1[0]
          #   print im1.histogram(im2)
          #   print im2.histogram(im1)
          #   print im2.histogram()
          #
        # print dist<1.0
        # print black==black1
        # print white==white1
        return (dist<1.0 and black==black1 and white==white1)

    def chooseStrategy(self, figures):
        # everyone is the same
        if self.areEqual(figures['A'], figures['B']) and self.areEqual(figures['B'], figures['C']):
            if self.areEqual(figures['D'], figures['E']) and self.areEqual(figures['E'], figures['F']):
                return 'row equals'





#     from itertools import izip
# import Image
#
# i1 = Image.open("image1.jpg")
# i2 = Image.open("image2.jpg")
# assert i1.mode == i2.mode, "Different kinds of images."
# assert i1.size == i2.size, "Different sizes."
#
#
