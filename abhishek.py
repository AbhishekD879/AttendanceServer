import os


def people(name, image):
    people_list = []
    people_dir = 'data/people'

    for person_name in os.listdir(people_dir):
        people_list.append(person_name)

        # print(person_dir)
    if name not in people_list:
        person_dir = os.path.join(people_dir, name)
        print(person_dir)
        os.mkdir(person_dir)


people("praw", "ghdfv")
