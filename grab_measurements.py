import re

def tokenize(string):
    return [x   for y in re.findall("[a-zA-Z]+['’]*[a-zA-Z]*|[0-9]+(?:[0-9\'\"\’\”]*[./][0-9\'\"\’\”]+)*[0-9\'\"\’\”\#]*", string)
                for x in re.findall("[a-zA-Z]+['’]*[a-zA-Z]*|[0-9]+|[./]+|[\'\"\’\”\#]+", y)]

def get_numbers(tokens):
    return [i for i in range(len(tokens)) if tokens[i].isdecimal()]

def foot_feature_map(tokens, i):
    i_am = {"am", "i'm", "i’m"}
    foot = {'foot', 'feet', 'ft', "'", "’"}
    return {
        'i_am' : any(token.lower() in i_am for token in tokens[max(0, i - 3) : i]) and not any(token.isdecimal() for token in tokens[max(0, i - 3) : i]),
        'foot' : any(token in foot for token in tokens[i + 1 : i + 4]),
        'pair_left' : any(token.isdecimal() and int(token) <= 6 for token in tokens[max(0, i - 3) : i]),
        'pair_right' : any(token.isdecimal() and int(token) <= 12 for token in tokens[i + 1 : i + 4])
    }

def inch_feature_map(tokens, i):
    inch = {"''", '"', '”', '’’', 'in', 'inches'}
    return{
        'inch' : any(token in inch for token in tokens[i + 1 : i + 2]),
    }
    

def is_foot(foot_features):
    coefficients = {
        'foot' : 10,
        'i_am' : 5,
        'pair_right' : 5,
        'pair_left' : -5
    }
    return 1 / (1 + 2.7 ** (-1 * sum(coefficients[feature] * (2 * foot_features[feature] - 1) for feature in coefficients)))

def get_height(string):
    tokens = tokenize(string)
    numbers = get_numbers(tokens)
    one_to_five = {str(i + 1) for i in range(5)}
    heights = []
    probabilities = []
    for i, n in enumerate(numbers):
        feet = int(tokens[n])
        p = is_foot(foot_feature_map(tokens, n))
        if 4 <= feet <= 6 and p >= 0.5:
            inches = 0
            if i + 1 < len(numbers) and numbers[i + 1] - n <= 3 and int(tokens[numbers[i + 1]]) <= 12:
                m = numbers[i + 1]
                inches = int(tokens[m])
                if tokens[m] in one_to_five and m + 2 < len(tokens) and tokens[m + 1] == '/' and tokens[m + 2] in one_to_five:
                    inches /= int(tokens[m + 2])
                elif m + 2 < len(tokens) and tokens[m + 1] == '.' and tokens[m + 2].isdecimal():
                    inches += int(tokens[m + 2]) / 10
                elif m + 3 < len(tokens) and tokens[m + 1] in one_to_five and tokens[m + 2] == '/' and tokens[m + 3] in one_to_five:
                    inches += int(tokens[m + 1]) / int(tokens[m + 3])
            heights.append({'ft' : feet, 'in' : inches})
            probabilities.append(p)
    height = None
    p_max = 0
    for i, p in enumerate(probabilities):
        if p > p_max:
            p_max = p
            height = heights[i]
    return height
            

def get_weight(string):
    i_am = {"am", "i'm", "i’m"}
    weigh = {"weigh", "weight"}
    foot = {'foot', 'feet', 'ft', "'", "’"}
    inch = {'in', 'inch', 'inches', '"', "''", '’’', '”'}
    lb = {'lb', 'lbs', 'pounds', '#', '#s', 'pds'}
    kilo = {'kg', 'kgs', 'kilos', 'kilograms'}
    tokens = tokenize(string)
    numbers = get_numbers(tokens)
    for n in numbers:
        weight = int(tokens[n])
        if weight >= 80 and (any(token in i_am | weigh | foot | inch for token in tokens[max(0, n - 10) : n]) or any(token in lb | kg for token in tokens[n + 1 : n + 4])):
            if any(token in kilo for token in tokens[n + 1 : n + 4]):
                return weight * 2.2
            else:
                return weight
    return None

def size_feature_map(string):
    got = {'chose', 'ordered', 'order', 'bought', 'got', 'purchased', 'went', 'sticking'}
    usually = {'usually', 'normally'}
    should = {'if', 'than', 'should'}
    perfect = {'perfect', 'perfectly', 'fit', 'fits', 'works'}
    are = {'is', 'are'}
    size = {'size'}
    exchanged = {'exchanged', 'exchange'}
    