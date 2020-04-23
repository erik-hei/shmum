def end_of_number(i, string):
    j = i + 1
    while j + 1 < len(string) and (string[j].isdigit()):
        j += 1
    return j
        
def get_weight(string):
    i = 0
    while i < len(string):
        if string[i].isdigit():
            j = end_of_number(i, string)
            number = int(string[i : j])
            if 90 <= number <= 400:
                return number
            elif any(unit in string[j : j + 10] for unit in {'kg', 'kilo'}):
                return round(number * 2.2)
            else:
                i = j
        else:
            i += 1
    return None

def get_height(string):
    i = 0
    while i < len(string):
        if string[i].isdigit():
            j = end_of_number(i, string)
            feet = int(string[i : j])
            if 4 <= feet <= 6:
                if any(phrase in string[max(0, i - 10) : i] for phrase in {"I am", "I'm", "I’m"}) or any(unit in string[j : j + 10] for unit in {"'", "’", "ft", "feet", "foot"}):
                    k = j
                    fraction_of_inch = 0
                    common_fractions = {'1/2' : 0.5, '3/4' : 0.75, '1/4' : 0.25}
                    for fraction in common_fractions:
                        if fraction in string[j : j + 10]:
                            fraction_of_inch = common_fractions[fraction]
                    while k < min(j + 10, len(string)):
                        if string[k].isdigit():
                            h = end_of_number(k, string)
                            inches = int(string[k : h])
                            if inches <= 12:
                                return {'ft' : feet, 'in' : inches + fraction_of_inch}
                            k = h
                        else:
                            k += 1
                    return {'ft' : feet, 'in' : fraction_of_inch}
            i = j
        else:
            i += 1
    return {'ft' : None, 'in' : None}