import re
import sympy
from IPython.display import display, Latex
import math

#TODO add constants such as pi, e, and physical constants
#TODO decide whether to substitute constant values or not
#TODO add deg or rad calculation in trigonometry funcs- it is up to the user to modify equation for deg or rad, rad is the default setting
#TODO add inline or multiline substitution
#TODO add calculation or procedure eq
#TODO convert all functions to camel letter


class Units:
    units_dict = {"MPa": "\\text{MPa}",
             "N/mm^2":"\\frac{\\text{N}}{\\text{mm}^2}",
             "N": "\\text{N}",
             "deg": "°",
             "rad": "\\text{rad}",
             "Nm": "\\text{Nm}",
             "kg": "\\text{kg}",
             "m/s^2": "\\frac{\\text{m}}{\\text{s}^2}",
             "m/s": "\\frac{\\text{m}}{\\text{s}}",
             "": "" # no unit
             }
    def __init__(self, unit):
        self.unit = Units.units_dict[unit]
 


class Equation(Units):
    print_latex = False
    print_units = False
    print_description = True
    print_wolframalpha_input = True
    substitute_constant_values = True
    #use_degrees = True
    print_inline = False

    constants = {"pi": [3.14, "\\pi", math.pi, "", ""], # last are unit and description
                 "π": [3.14, "\\pi", math.pi, "", ""],
                 "e": [2.72, "e", math.e, "", ""]}

    def __init__(self, symbol, eq, unit, description, precision, *args):
        if "_" in symbol:
            self.symbol = symbol.split("_")[0] + "_{" + symbol.split("_")[1] + "}"
        else:
            self.symbol = symbol
        super().__init__(unit)
        # self.trigonometry_unit = trigonometry_unit
        self.description = description
        self.precision = precision
        var_sets = args
        self.vars = {}
        for var_set in var_sets:
            self.vars = {**self.vars, **var_set}

        self.eq = eq.replace(" ","")
        self.eq = Equation.change_exponent2(self.eq)
        self.eq = Equation.change_sqrt(self.eq)
        self.eq = Equation.change_division(self.eq)
        self.eq = Equation.change_functions(self.eq)
        self.eq = Equation.change_absolute(self.eq)

        #self.calculate_eq = Equation.change_trigonometry(self.eq)

        self.symbolic_eq, self.value_eq, self.value_unit_eq = Equation.substitute_vars(self.eq, self.vars, Equation.substitute_constant_values)
        self.symbolic_eq = Equation.change_parenthesis(self.symbolic_eq)
        self.value_eq = Equation.change_parenthesis(self.value_eq)
        self.value_unit_eq = Equation.change_parenthesis(self.value_unit_eq)

        self.symbolic_eq = Equation.change_multiplication(self.symbolic_eq)
        self.value_eq = Equation.change_multiplication(self.value_eq)
        self.value_unit_eq = Equation.change_multiplication(self.value_unit_eq)

        self.result, self.wolfram_eq = Equation.calculate_result(eq, self.vars, num_of_decimals=self.precision)

        description_print = self.symbol + "[" + self.unit + "] - " + " \\text{" + self.description + "}"
        symbolic_eq_print = self.symbol + "=" + self.symbolic_eq
        value_eq_print = self.symbol + "=" + self.value_eq
        value_unit_eq_print = self.symbol + "=" + self.value_unit_eq
        result_print = self.symbol + "=" + str(self.result) + self.unit

        if Equation.print_description:
            Equation.output_equation(description_print, Equation.print_latex)
        Equation.output_equation(symbolic_eq_print, Equation.print_latex)
        if Equation.print_units:
            pass
            Equation.output_equation(value_unit_eq_print, Equation.print_latex)
        else:
            pass
            Equation.output_equation(value_eq_print, Equation.print_latex)
        Equation.output_equation(result_print, Equation.print_latex)
        if Equation.print_latex:
            #pass
            display(Latex("$\\newline$"))
        else:
            print()
        if Equation.print_wolframalpha_input:
            print(f"wolfram alpha check:\n{self.wolfram_eq}")

    @staticmethod
    def output_equation(eq, latex):
        if latex:
            #pass
            display_eq = eq
            display_eq = display_eq.replace("\\frac", "\\dfrac")
            display(Latex("$" + display_eq + "\\newline\\\\[10pt]" + "$"))
        else:
            print(eq)

    @staticmethod
    def calculate_result(eq, vars, num_of_decimals=1):
        new_eq = eq
        symbolic_eq = eq
        var_num_match = r"(?![-+*/()x]|frac|abs|Abs|sqrt|ln|log|a?(?:sin|cos|tan)h?)\b\w+\b"
        pattern = re.compile(var_num_match)
        match = pattern.search(new_eq)
        symbol_replacements = []
        symbol_offset = 0
        while match != None:
            if match.group(0) in vars:
                if vars[match.group(0)][1] == "°":
                    value = str(vars[match.group(0)][0]) # * math.pi / 180)
                else:
                    value = str(vars[match.group(0)][0])

                symbol_replacements.append(
                    [symbol_offset + match.start(), symbol_offset + match.end(), value])
                symbol_offset += match.start() + len(value)
            elif match.group(0) in Equation.constants:
                symbol_replacements.append(
                    [symbol_offset + match.start(), symbol_offset + match.end(), str(Equation.constants[match.group(0)][0])])
                symbol_offset += match.start() + len(str(Equation.constants[match.group(0)][0]))
            else:
                symbol_name = match.group(0)
                symbol_offset += match.start() + len(symbol_name)

            new_eq = new_eq[match.end():]
            match = pattern.search(new_eq)
        for i in symbol_replacements:
            symbolic_eq = Equation.replace_string(symbolic_eq, i[2], i[0], i[1])

        """ it will use wolfram_eq for calculation and symbolic_eq for printing. this is needed because once it might use
        degrees for calculating trigonometry and other times it could use radians, the wolfram equation will only have an addition of
        * pi /180 if degrees are used, wolfram_eq also used when substituting constants"""

        wolfram_eq = symbolic_eq
        decimal_match = r"\d+\.?\d*"
        pattern = re.compile(decimal_match)
        result = str(sympy.sympify(symbolic_eq).evalf())
        match = pattern.findall(result)
        chars_before_decimal = 0
        for i in match:
            dissolved_number = i.split(".")
            if len(dissolved_number[0]) > chars_before_decimal:
                chars_before_decimal = len(dissolved_number[0])





        result = sympy.sympify(symbolic_eq).evalf(num_of_decimals + chars_before_decimal)

        if type(result) == type(1.0) or type(result) == type(1):  # not working
            return float(result)
        else:
            result = str(result).replace(" ", "")
            result = result.replace("**", "^")

            result = Equation.change_exponent2(result)
            result = Equation.change_sqrt(result)
            result = Equation.change_division(result)
            result = Equation.change_functions(result)
            result = Equation.change_absolute(result)
            result = Equation.change_parenthesis(result)
            result = Equation.change_multiplication(result)

            var_num_match = r"(?![-+*/()x]|frac|abs|Abs|sqrt|ln|log|e|pi|a?(?:sin|cos|tan)h?)\b\w+\b"
            pattern = re.compile(var_num_match)
            symbols = pattern.finditer(result)
            offset = 0
            result_latex_vars = result
            for symbol_raw in symbols:
                symbol_name_split = symbol_raw.group(0).split("_")
                if len(symbol_name_split) == 2:
                    symbol_name = symbol_name_split[0] + "_{" + symbol_name_split[1] + "}"
                    result_latex_vars = Equation.replace_string(result_latex_vars, symbol_name,
                                                                symbol_raw.start() + offset, symbol_raw.end() + offset)
                    offset += 2
                else:
                    symbol_name = symbol_raw.group(0)
                    result_latex_vars = Equation.replace_string(result_latex_vars, symbol_name,
                                                                symbol_raw.start() + offset, symbol_raw.end() + offset)

            return result_latex_vars, wolfram_eq

    @staticmethod
    def find_parenthesis(eq, index):
        counter = 0
        parenthesis_index = [index, ]
        if (eq[index] == "(") or (eq[index] == ")"):
            left_char = "("
            right_char = ")"
        if (eq[index] == "{") or (eq[index] == "}"):
            left_char = "{"
            right_char = "}"

        if eq[index] == left_char:
            increment = 1
            start_parenthesis = left_char
            find_parenthesis = right_char
        elif eq[index] == right_char:
            increment = -1
            start_parenthesis = right_char
            find_parenthesis = left_char

        while len(parenthesis_index) != 0:
            counter += increment
            if eq[index + counter] == start_parenthesis:
                parenthesis_index.append(index + counter)
            if eq[index + counter] == find_parenthesis:
                parenthesis_index.pop()
        return index + counter

    @staticmethod
    def replace_char(eq, char, index):
        new_eq = eq[:index] + char + eq[(index + 1):]
        return new_eq

    @staticmethod
    def replace_string(eq, string, start_index, end_index):
        new_eq = eq[:start_index] + string + eq[end_index:]
        return new_eq

    @staticmethod
    def insert_string_at_index(eq, chars, index):
        new_eq = eq[:index] + chars + eq[index:]
        return new_eq

    @staticmethod
    def change_sqrt(eq):
        start_search_index = 0
        sqrt_index = eq.find("sqrt", start_search_index)
        new_eq = eq
        while sqrt_index != -1:
            left_parenthesis_index = sqrt_index + len("sqrt")
            right_parenthesis_index = Equation.find_parenthesis(new_eq, left_parenthesis_index)
            new_eq = Equation.replace_char(new_eq, "{", left_parenthesis_index)
            new_eq = Equation.replace_char(new_eq, "}", right_parenthesis_index)
            new_eq = Equation.replace_string(new_eq, "\\sqrt", sqrt_index, sqrt_index + len("sqrt"))
            start_search_index = sqrt_index + 5
            sqrt_index = new_eq.find("sqrt", start_search_index)
        return new_eq



    @staticmethod
    def change_exponent2(eq):
        new_eq = eq
        index_counter = 0
        while index_counter < len(new_eq) - 1:
            if new_eq[index_counter] == "^" and new_eq[index_counter + 1] != "{":
                exponent_members = []
                left_counter = index_counter - 1
                while left_counter >= 0:
                    if new_eq[left_counter] == ")":
                        left_counter = Equation.find_parenthesis(new_eq, left_counter)
                    if left_counter == 0:
                        exponent_begin = left_counter
                        break
                    if new_eq[left_counter - 1] in  ("(", "*", "/", "+", "-"):
                        exponent_begin = left_counter
                        break
                    left_counter -= 1

                exponent_members.append(new_eq[exponent_begin:index_counter])
                right_counter = index_counter + 1
                right_curly_brackets = 1
                right_member_start = index_counter + 1

                while right_counter <= len(new_eq):
                    if new_eq[right_counter] == "(":
                        right_counter = Equation.find_parenthesis(new_eq, right_counter)
                    if right_counter == len(new_eq) - 1:
                        exponent_end = right_counter
                        break
                    if new_eq[right_counter + 1] in (")", "*", "/", "+", "-"):
                        exponent_end = right_counter
                        break
                    if new_eq[right_counter] == "^":
                        right_curly_brackets += 1
                        right_member_end = right_counter
                        exponent_members.append(new_eq[right_member_start:right_member_end])
                        right_member_start = right_counter + 1
                    right_counter += 1
                exponent_members.append(new_eq[right_member_start:exponent_end + 1])
                exponent_latex = exponent_members.pop()
                exponent_members.reverse()

                functions = ["sin", "cos", "tan", "asin", "acos", "atan", "ln", "log"]
                for member in exponent_members:
                    if member[:3] in functions:
                        exponent_latex = "{" + member[:3] + "}^{" + exponent_latex + "}" + member[3:]
                    elif member[:4] in functions:
                        exponent_latex = "{" + member[:4] + "}^{" + exponent_latex + "}" + member[4:]
                    else:
                        exponent_latex = "{" + member + "}^{" + exponent_latex + "}"
                new_eq = Equation.replace_string(new_eq, exponent_latex, exponent_begin, exponent_end + 1)
                #index_counter = exponent_end

            index_counter += 1
        return new_eq

    @staticmethod
    def change_division(eq):
        new_eq = eq
        index_counter = 0
        while index_counter < len(new_eq):
            if new_eq[index_counter] == "/":
                nominator = []
                denominator = []
                left_member_end = index_counter
                left_counter = index_counter - 1
                while left_counter > 0 and new_eq[left_counter - 1] not in ("+", "-", "(", "{"):
                    if (new_eq[left_counter] == ")") or (new_eq[left_counter] == "}"):
                        left_counter = Equation.find_parenthesis(new_eq, left_counter)
                    elif new_eq[left_counter] == "*":
                        left_member_start = left_counter + 1
                        nominator.append(new_eq[left_member_start:left_member_end])
                        left_member_end = left_member_start - 1
                    if left_counter != 0 and new_eq[left_counter - 1] not in ("+", "-", "(", "{"):
                        left_counter -= 1
                if left_counter == 0 and new_eq[left_counter] == ")":
                    left_member_start = left_counter + 1
                else:
                    left_member_start = left_counter
                nominator.append(new_eq[left_member_start:left_member_end])

                nominator.reverse()
                right_member_start = index_counter + 1
                right_counter = index_counter + 1
                current_operator = "/"
                while right_counter != len(new_eq) and new_eq[right_counter] not in ("+", "-", ")", "}"):
                    if (new_eq[right_counter] == "(") or (new_eq[right_counter] == "{"):
                        right_counter = Equation.find_parenthesis(new_eq, right_counter)
                        pass
                    elif new_eq[right_counter] == "*" or new_eq[right_counter] == "/":
                        right_member_end = right_counter
                        if current_operator == "/":
                            denominator.append(new_eq[right_member_start:right_member_end])
                        if current_operator == "*":
                            nominator.append(new_eq[right_member_start:right_member_end])
                        right_member_start = right_counter + 1
                        current_operator = new_eq[right_counter]
                    right_counter += 1
                right_member_end = right_counter
                if current_operator == "/":
                    denominator.append(new_eq[right_member_start:right_member_end])
                if current_operator == "*":
                    nominator.append(new_eq[right_member_start:right_member_end])
                fraction_end = right_member_end
                fraction_start = left_member_start

                # if times or division sign next to parenthesis of the whole fraction then remove parenthesis,
                # if sin, cos tan, abs, etc. in front of parenthesis, DON'T remove them
                # in every other case keep parenthesis

                # check if parenthesis are around
                functions = ["ln", "log", "sin", "cos", "tan", "asin", "acos", "atan", "abs", "Abs"]
                remove_parenthesis = False
                if fraction_start >= 1:
                    if new_eq[fraction_start - 1] == "(":
                        end_parenthesis = Equation.find_parenthesis(new_eq, fraction_start - 1)
                        if end_parenthesis == fraction_end:
                            if fraction_end <= len(new_eq) - 2 and new_eq[fraction_end + 1] == "^":
                                remove_parenthesis = False
                            elif fraction_start >= 2 and new_eq[fraction_start - 2] == "(":  # maybe redundant
                                remove_parenthesis = True
                            elif fraction_start >= 3 and new_eq[fraction_start - 3:fraction_start - 1] in functions:
                                remove_parenthesis = False
                            elif fraction_start >= 4 and new_eq[fraction_start - 4:fraction_start - 1] in functions:
                                remove_parenthesis = False
                            elif fraction_start >= 5 and new_eq[fraction_start - 5:fraction_start - 1] in functions:
                                remove_parenthesis = False
                            elif fraction_end <= len(new_eq) - 2 and new_eq[fraction_end + 1] in ("*", "/"):
                                remove_parenthesis = True
                            elif fraction_start >= 2 and new_eq[fraction_start - 2] in ("*", "/"):
                                remove_parenthesis = True
                            else:
                                remove_parenthesis = False

                # replace gathered nominator and denominator with frac{nominator}{denominator}
                # based on previous check, add or remove parenthesis around frac{}{}
                # if the parenthesis are to be removed, use fraction_start - 1 and fraction_end +1,
                # for replacement, otherwise use only fraction_start and fraction_end
                if remove_parenthesis:
                    nominator_string = "*".join(nominator)
                    denominator_string = "*".join(denominator)
                    new_eq = Equation.replace_string(new_eq,
                                                     "\\frac{" + f"{nominator_string}" + "}{" + f"{denominator_string}" + "}",
                                                     fraction_start - 1, fraction_end + 1)
                else:
                    nominator_string = "*".join(nominator)
                    denominator_string = "*".join(denominator)
                    new_eq = Equation.replace_string(new_eq,
                                                     "\\frac{" + f"{nominator_string}" + "}{" + f"{denominator_string}" + "}",
                                                     fraction_start, fraction_end)
            index_counter += 1
        return new_eq

    @staticmethod
    def change_functions(eq):
        functions = ["ln", "log", "asin", "acos", "atan", "sin", "cos", "tan"]
        new_eq = eq
        for function in functions:
            start_search_index = 0
            func_index = eq.find(function, start_search_index)
            while func_index != -1:
                new_eq = Equation.replace_string(new_eq, f"\\text{{{function}}}", func_index, func_index + len(function))
                start_search_index = func_index + 1 + len(f"\\text{{{function}}}")
                func_index = new_eq.find(function, start_search_index)
        return new_eq

    @staticmethod
    def change_absolute(eq):
        abs_variations = ["abs", "Abs", "ABS"]
        new_eq = eq

        for abs_variant in abs_variations:
            start_search_index = 0
            abs_index = eq.find(abs_variant, start_search_index)
            while abs_index != -1:
                left_parenthesis_index = abs_index + len(abs_variant)
                right_parenthesis_index = Equation.find_parenthesis(new_eq, left_parenthesis_index)
                new_eq = Equation.replace_char(new_eq, "|", left_parenthesis_index)
                new_eq = Equation.replace_char(new_eq, "|", right_parenthesis_index)
                new_eq = Equation.replace_string(new_eq, "", abs_index, abs_index + len(abs_variant))
                start_search_index = abs_index + 1
                abs_index = new_eq.find(abs_variant, start_search_index)
        return new_eq

    @staticmethod
    def substitute_vars(eq, vars, replace_constants):
        new_eq = eq
        symbolic_eq = eq
        value_eq = eq
        value_unit_eq = eq
        var_num_match = r"(?![-+*/()x]|frac|abs|Abs|sqrt|ln|log|a?(?:sin|cos|tan)h?)\b\w+\b"
        pattern = re.compile(var_num_match)
        match = pattern.search(new_eq)
        symbol_replacements = []
        value_replacements = []
        value_unit_replacements = []
        symbol_offset = 0
        value_offset = 0
        value_unit_offset = 0
        while match != None:
            if match.group(0) in vars:
                symbol_name_split = match.group(0).split("_")
                if len(symbol_name_split) == 2 and symbol_name_split[0] != "":
                    symbol_name = symbol_name_split[0] + "_{" + symbol_name_split[1] + "}"
                else:
                    symbol_name = match.group(0)
                symbol_replacements.append([symbol_offset + match.start(), symbol_offset + match.end(), symbol_name])
                value_replacements.append([value_offset + match.start(), value_offset + match.end(), str(vars[match.group(0)][0])])
                value_unit_replacements.append([value_unit_offset + match.start(), value_unit_offset + match.end(), str(vars[match.group(0)][0]) + vars[match.group(0)][1]])
                symbol_offset += match.start() + len(symbol_name)
                value_offset += match.start() + len(str(vars[match.group(0)][0]))
                value_unit_offset += match.start() + len(str(vars[match.group(0)][0]) + vars[match.group(0)][1])

            elif match.group(0) in Equation.constants.keys():
                #print(f"constants matched {match.group(0)}")
                if replace_constants:
                    index = 0
                else:
                    index = 1
                # if "_" in match.group(0):
                #     symbol_name = match.group(0).split("_")[0] + "_{" + match.group(0).split("_")[1] + "}"
                # else:
                #     symbol_name = match.group(0)
                symbol_replacements.append([symbol_offset + match.start(), symbol_offset + match.end(), str(Equation.constants[match.group(0)][1])])
                value_replacements.append(
                    [value_offset + match.start(), value_offset + match.end(), str(Equation.constants[match.group(0)][index])])
                value_unit_replacements.append([value_unit_offset + match.start(), value_unit_offset + match.end(),
                                                str(Equation.constants[match.group(0)][index]) + Equation.constants[match.group(0)][3]])
                symbol_offset += match.start() + len(str(Equation.constants[match.group(0)][1]))
                value_offset += match.start() + len(str(Equation.constants[match.group(0)][index]))
                value_unit_offset += match.start() + len(str(Equation.constants[match.group(0)][index]) + Equation.constants[match.group(0)][3])
            else:
                symbol_name_split = match.group(0).split("_")
                if len(symbol_name_split) == 2 and symbol_name_split[0] != "":
                    symbol_name = symbol_name_split[0] + "_{" + symbol_name_split[1] + "}"
                else:
                    symbol_name = match.group(0)
                symbol_replacements.append(
                    [symbol_offset + match.start(), symbol_offset + match.end(), symbol_name])
                value_replacements.append(
                    [value_offset + match.start(), value_offset + match.end(), symbol_name])
                value_unit_replacements.append([value_unit_offset + match.start(),
                                                value_unit_offset + match.end(),
                                                symbol_name])
                symbol_offset += match.start() + len(symbol_name)
                value_offset += match.start() + len(symbol_name)
                value_unit_offset += match.start() + len(symbol_name)

            new_eq = new_eq[match.end():]
            match = pattern.search(new_eq)
        for i in symbol_replacements:
            symbolic_eq = Equation.replace_string(symbolic_eq, i[2], i[0], i[1])
        for j in value_replacements:
            value_eq = Equation.replace_string(value_eq, j[2], j[0], j[1])
        for k in value_unit_replacements:
            value_unit_eq = Equation.replace_string(value_unit_eq, k[2], k[0], k[1])

        return symbolic_eq, value_eq, value_unit_eq

    @staticmethod
    def change_parenthesis(eq):
        new_eq = ""
        for i in eq:
            if i == "(":
                new_eq += "\\left("
            elif i == ")":
                new_eq += "\\right)"
            else:
                new_eq += i
        return new_eq

    @staticmethod
    def change_multiplication(eq):
        new_eq = ""
        i = 0
        while i < len(eq):
            if eq[i] == "*" and eq[i + 1] != "*":
                new_eq += "\\cdot "
                i += 1
            elif eq[i] == "*" and eq[i + 1] == "*":
                new_eq += "^"
                i += 2
            else:
                new_eq += eq[i]
                i += 1

        return new_eq

    @staticmethod
    def change_trigonometry(eq):
        functions = ["sin", "cos", "tan"]
        inverse_funcs = ["asin", "acos", "atan"]
        new_eq = eq
        for function in functions:
            start_search_index = 0
            func_index = eq.find(function, start_search_index)
            while func_index != -1:
                new_eq = Equation.replace_string(new_eq, f"\\{function}", func_index, func_index + len(function))
                start_search_index = func_index + 1 + len(function)
                func_index = new_eq.find(function, start_search_index)


        for function in inverse_funcs:
            start_search_index = 0
            func_index = eq.find(function, start_search_index)
            while func_index != -1:
                new_eq = Equation.replace_string(new_eq, f"\\{function}", func_index, func_index + len(function))
                start_search_index = func_index + 1 + len(function)
                func_index = new_eq.find(function, start_search_index)
        return new_eq


class Constants(Units):
    constants = {"pi":[math.pi, 3.14, "\\pi"],
                 "e":[math.e, 2.72, "e"]}

class Variables(Units):
    print_latex = True
    print_description = True

    def __init__(self, *args):
        self.variables = {}
        for var in args:
            if "_" in var[0]:
                symbol = var[0].split("_")[0] + "_{" + var[0].split("_")[1] + "}"
            else:
                symbol = var[0]
            string_to_print = symbol + "=" + str(var[1]) + Units.units_dict[var[2]]
            if Variables.print_description:
                string_to_print += "\\text{ - " + var[3] + "}"
            if var[4].lower() == "print":
                Variables.output_equation(string_to_print, Variables.print_latex)
            self.variables[var[0]] = [var[1], Units.units_dict[var[2]], var[3], var[4]]
        if Variables.print_latex:
            #pass
            display(Latex("$\\newline$"))
        else:
            print()

    @staticmethod
    def output_equation(eq, latex):
        if latex:
            #pass

            display_eq = eq
            display_eq = display_eq.replace("\\frac", "\\dfrac")
            display(Latex("$" + display_eq + "\\\\[10pt]" + "$"))
        else:
            print(eq)





Variables.print_latex = False
Equation.print_units = True
Equation.print_latex = True
Equation.print_wolframalpha_input = False
Equation.substitute_constant_values = True

vars = Variables(["μ_steel", 0.1, "", "Steel coefficient of friction", "print"],
                 ["F_n", 100, "N/mm^2", "Normal force", "print"])
print()
friction_eq = Equation("F_fr", # symbol
                       "π+F_n + Abs(e) + ln(5) + pi + F_n^μ_steel * (μ_steel / F_n * (1 /3/2*sqrt(4/5*6))^2) * F_n + μ_steel * F_n", # equation
                       "N", # unit
                       "Friction force", # description
                       4, # number of decimals
                       vars.variables # input variables
                       )
