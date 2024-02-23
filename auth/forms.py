from re import fullmatch


def validate(name, surname, phone):
    return 'yes' \
        if (fullmatch(r'\+7\d*', phone) and
            fullmatch(r'[A-ZА-Я][a-zа-я]{0,24}', name) and
            fullmatch(r'[A-ZА-Я][a-zа-я]{0,24}', surname)) \
        else 'no'


test_count = int(input())
for i in range(test_count):
    name = input()
    surname = input()
    phone = input()
    print(validate(name, surname, phone))