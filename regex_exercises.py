import re

EXERCISES = {
    1:  lambda s: bool(re.fullmatch(r"ab*", s)),
    2:  lambda s: bool(re.fullmatch(r"ab{2,3}", s)),
    3:  lambda s: re.findall(r"[a-z]+(?:_[a-z]+)+", s),
    4:  lambda s: re.findall(r"[A-Z][a-z]+", s),
    5:  lambda s: bool(re.fullmatch(r"a.*b", s)),
    6:  lambda s: re.sub(r"[ ,.]", ":", s),
    7:  lambda s: re.sub(r"_([a-z])", lambda m: m.group(1).upper(), s),
    8:  lambda s: re.split(r"(?=[A-Z])", s),
    9:  lambda s: re.sub(r"(?<=[a-z])(?=[A-Z])", " ", s),
    10: lambda s: re.sub(r"(?<=[a-z])(?=[A-Z])", "_", s).lower(),
}

while True:
    choice = input("\nExercise (1-10, 0 to exit): ").strip()
    if not choice.isdigit() or int(choice) not in range(11):
        print("Enter a number from 0 to 10.")
        continue
    if int(choice) == 0:
        break
    print(EXERCISES[int(choice)](input("Input: ").strip()))
