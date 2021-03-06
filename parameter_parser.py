from random import shuffle

class Parameters(object):
    def __init__(self):
        self.params = ParameterReader()
        self.test_setups = list()
        for circle_radius in self.params.circle_radius:
            for target_radius in self.params.target_radius:
                self.test_setups.append((circle_radius, target_radius))
        self.__shuffle_setups()

    def __shuffle_setups(self):
        shuffle(self.test_setups)
        self.random_test_setup = iter(self.test_setups)

    def get_screensize(self):
        return self.params.width, self.params.height

    def get_number_of_targets(self):
        return self.params.num_targets

    def get_target_color(self):
        return self.params.target_color

    def get_hilight_color(self):
        return self.params.hilight_color

    def get_test_setup(self):
        try:
            return self.random_test_setup.next()
        except StopIteration:
            self.__shuffle_setups()
            return self.random_test_setup.next()

class ParameterReader(object):
    width, height = 1280, 800
    target_radius = list([50, 40, 30, 20, 10])
    circle_radius = list([350, 300, 250, 200, 150])
    num_targets = 9
    target_color = 244, 238, 224
    hilight_color = 255, 165, 0

    def __init__(self):
        try:
            self.config_file = open("config", "r")
            self.__read_parameters()
            self.config_file.close()
        except IOError:
            print "Could not open the config file. Using defaults."
        except ParameterError as value:
            print "Invalid config file or parameters:\n" + \
                  "%s\nUsing defaults." % value
            self.config_file.close()

    def __read_parameters(self):
        constant_parameters = list()
        circle_diams = list()
        target_diams = list()
        for line in self.config_file:
            if self.__line_is_not_comment(line):
                tokens = self.__tokenize_line(line)
                if len(constant_parameters) < 9:
                    constant_parameters += tokens
                elif len(circle_diams) == 0:
                    circle_diams += tokens
                else:
                    target_diams += tokens
        self.__unlist_parameters(constant_parameters)
        divide_by_two = lambda x: x/2
        self.target_radius = map(divide_by_two, target_diams)
        self.circle_radius = map(divide_by_two, circle_diams)

    def __line_is_not_comment(self, line):
        return not line[0] == '#'

    def __tokenize_line(self, line):
        tokens = list()
        line_params = line.split(' ')
        for token in line_params:
            token = self.__param_to_int(token)
            tokens.append(token)
        return tokens

    def __param_to_int(self, string):
        try:
            integer = int(string)
            if integer < 0:
                raise ParameterError("Negative parameters given. Should be positive.")
            return integer
        except ValueError:
            raise ParameterError("Non-numeric parameters given.")

    def __unlist_parameters(self, parameters):
        self.__check_constant_parameters(parameters)
        self.width, self.height = parameters[0:2]
        self.num_targets = parameters[2]
        self.target_color = parameters[3:6]
        self.hilight_color = parameters[6:9]

    def __check_constant_parameters(self, parameters):
        if parameters[2] % 2 == 0 or parameters[2] == 1:
            raise ParameterError("Number of targets must be an odd number > 1.")
        for param in parameters[3:9]:
            if not (param >= 0 and param <= 255):
                raise ParameterError("%d is not a valid RGB color component value." % param)

class ParameterError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
