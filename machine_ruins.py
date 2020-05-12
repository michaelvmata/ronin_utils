import textwrap
from typing import List, Dict
import re

from yaml import load_all


possible_act = set(['SENTINEL', 'SCAVENGER', 'ISNPC', 'NICE-THIEF',
    'AGGRESSIVE', 'STAY-ZONE', 'WIMPY', 'SUBDUE', 'RIDE', 'MOUNT', 'FLY',
    'AGGWA', 'AGGTH', 'AGGCL', 'AGGMU', 'MEMORY', 'AGGNI', 'AGGNO', 'AGGPA',
    'AGGAP', 'AGGBA', 'AGGCO', 'AGGEVIL', 'AGGGOOD', 'AGGNEUT', 'AGGLEADER',
    'AGGRANDOM', 'ARM', 'SHIELD', 'OPEN-DOOR', 'NO-TOKEN', 'IGNORE-SPHERE'])

possible_aff = set(['BLIND', 'INVISIBLE', 'DETECT-ALIGNMENT',
    'DETECT-INVISIBLE', 'DETECT-MAGIC', 'SENSE-LIFE', 'HOLD', 'SANCTUARY',
    'CURSE', 'SPHERE', 'POISON', 'PROTECT-EVIL', 'PARALYSIS', 'INFRAVISION',
    'STATUE', 'SLEEP', 'DODGE', 'SNEAK', 'HIDE', 'FLY', 'IMINV', 'INVUL',
    'DUAL', 'FURY', 'PROTECT-GOOD', 'TRIPLE', 'QUAD'])


def to_set(s: str) -> set:
    return set([i.upper() for i in s.split()])


pattern = re.compile(
    r'^(?P<count>[0-9]+)d(?P<sides>[0-9]+)\+(?P<base>[0-9]+)$')


def is_diceroll(s: str) -> bool:
    if not isinstance(s, str):
        return False
    match = re.match(pattern, s)
    return bool(match)


def validate_mobile(mobile: Dict[str, str]):
    assert mobile['id']
    assert mobile['full']
    assert mobile['short']
    assert mobile['keywords']
    assert mobile['level']
    assert mobile['gold']
    assert mobile['exp']
    assert mobile['act']
    assert to_set(mobile['act']).issubset(possible_act)
    assert mobile['aff']
    assert to_set(mobile['aff']).issubset(possible_aff)
    assert 'armor' in mobile
    assert 'align' in mobile
    assert 'hitroll' in mobile
    assert mobile['damage']
    assert is_diceroll(mobile['damage'])
    assert mobile['hp']
    assert is_diceroll(mobile['hp'])
    assert mobile['mana']
    assert is_diceroll(mobile['mana'])


def make_commands(mobile: Dict[str, str], wrap: int = 79) -> List[str]:
    validate_mobile(mobile)
    mobile_id = mobile['id']
    full = textwrap.fill(mobile['full'], wrap)
    return [
        f'create mobile {mobile_id}',
        f'mshort {mobile_id}\n{mobile["short"]}@@',
        f'mlong {mobile_id}\n{mobile["long"]}@@',
        f'mfull {mobile_id}\n{full}\n@@',
        f'mname {mobile_id}\n{mobile["keywords"]}@@',
        f'mlevel {mobile_id} {mobile["level"]}',
        f'mgold {mobile_id} {mobile["gold"]}',
        f'mexp {mobile_id} {mobile["exp"]}',
        f'mact {mobile_id} {mobile["act"]}',
        f'maff {mobile_id} {mobile["aff"]}',
        f'marmor {mobile_id} {mobile["armor"]}',
        f'malign {mobile_id} {mobile["align"]}',
        f'mhitroll {mobile_id} {mobile["hitroll"]}',
        f'mdamage {mobile_id} {mobile["damage"]}',
        f'mhps {mobile_id} {mobile["hp"]}',
        f'mmana {mobile_id} {mobile["mana"]}',
    ]

if __name__ == '__main__':
    with open('machine_ruins.yml', 'r') as f:
        docs = load_all(f.read())

    cmds = []
    for doc in docs:
        try:
            cmds.extend(make_commands(doc))
        except AssertionError:
            print(f'Problem with {doc}')
            raise
    cmds.append('\n')
    raw = '\n'.join(cmds)
    print(raw)
    with open('machine_ruins.cmds', 'w') as f:
        f.write(raw)
