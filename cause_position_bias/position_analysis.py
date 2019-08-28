import numpy as np
import random


def generate_position_pair():
    with open("../data/clause_keywords_emotion.txt") as f:
        line_list = f.readlines()
        for i in range(len(line_list)):
            if line_list[i].split(",")[5] == "yes" and line_list[i].split(",")[4] == "0":
                print(line_list[i].strip())

    f.close()


if __name__ == "__main__":
    generate_position_pair()