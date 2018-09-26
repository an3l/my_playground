def square(x):
    return x*x

def main():
    for i in range(10):
        print("{} squared is {}".format(i, square(i)))
    names= ["Anel", "Melisa"]
    for name in names:
        print(name)

    s= set()
    s.add(1)
    s.add(3)
    s.add(5)
    s.add(3)
    s.add(3) # items in the sets are unique
    print(s)

    # Dictionaries: maps key-value
    ages={"Anel":30, "Melisa": 26}
    ages["Senad"]= 58
    ages["Melisa"]+=1
    print(ages)

if __name__=="__main__":
    main()
