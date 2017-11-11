with open('./users.txt', 'r') as infile:
    users_set = set([])
    for line in infile.readlines():
        line = line.strip()
        if len(line) != 0:
            users_set.add(line)

with open('./users_1.txt', 'r') as infile:
    for line in infile.readlines():
        line = line.strip()
        if len(line) != 0:
            users_set.add(line)

with open('./do_users.txt', 'w') as outfile:
    for user in users_set:
        outfile.write(user)
        outfile.write('\n')

