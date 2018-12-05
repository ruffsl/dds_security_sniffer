import sys
import random

def form_group(group_num, n, roles, topics, low, high):
    counts = [0] * len(roles)
    for i in range(n):
        idx = random.randrange(0, len(roles))
        counts[idx] += 1
        subject_name = 'CN=G{}_'.format(group_num) + roles[idx] + str(counts[idx])
        grant_name = 'G{}_'.format(group_num) + roles[idx] + str(counts[idx])
        file_name = grant_name + '.xml'
        rules = generate_rules(topics, low, high)
        if roles[idx] == 'talker':
            write_perm(file_name, grant_name, subject_name, '', rules)
        elif roles[idx] == 'listener':
            write_perm(file_name, grant_name, subject_name, rules, '')

def generate_rules(topics, low, high):
    assert (low <= high)
    idx = random.randint(low, high)
    rule = '            <topic>{}</topic>\n'
    rules = set()
    for i in range(idx):
        topic = random.choice(topics)
        if random.random() < 0.5 and '/' in topic:
            tokens = topic.split('/', random.randint(1, topic.count('/')))
            tokens[-1] = '*'
            topic = '/'.join(tokens)
        rules.add(rule.format(topic))
    return ''.join(rules)

def write_perm(fn, gn, sn, sub_rules, pub_rules):
    perm = '<?xml version="1.0" encoding="utf-8"?>\n<dds>\n  <permissions>\n    <grant name="{}">\n      <subject_name>{}</subject_name>\n      <validity>\n        <not_before>2013-10-26T00:00:00</not_before>\n        <not_after>2023-10-26T22:45:30</not_after>\n      </validity>\n      <allow_rule>\n        <domains>\n          <id>0</id>\n        </domains>\n        <subscribe>\n          <topics>\n{}          </topics>\n        </subscribe>\n        <publish>\n          <topics>\n{}          </topics>\n        </publish>\n      </allow_rule>\n      <default>DENY</default>\n    </grant>\n  </permissions>\n</dds>\n'.format(gn, sn, sub_rules, pub_rules)

    with open(fn, 'w') as f:
        f.write(perm)

if __name__ == "__main__":
    n1 = int(sys.argv[1]) if int(sys.argv[1]) >= 2 else 2
    n2 = int(sys.argv[2]) if int(sys.argv[2]) >= 2 else 2
    low, high = 5, 10
    roles = ['talker', 'listener']
    f1, f2 = 'topics1.txt', 'topics2.txt'
    with open(f1) as f:
        t1 = f.read().splitlines()
    with open(f2) as f:
        t2 = f.read().splitlines()
    form_group(1, n1, roles, t1, low, high)
    form_group(2, n2, roles, t2, low, high)
