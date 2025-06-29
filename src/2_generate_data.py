import os
import random
import shutil

import psycopg
from faker import Faker

from lib.constants import GENERATED_DIR
from lib.db import select_schema
from lib.generator import EpicDataGenerator

try:
    shutil.rmtree(GENERATED_DIR)
except:
    pass

os.makedirs(GENERATED_DIR)

fake = Faker()


with psycopg.connect() as conn:
    with conn.cursor() as cur:
        select_schema(cur)

        rarity_ids = [
            row[0] for row in cur.execute("SELECT id FROM rarities").fetchall()
        ]
        element_type_ids = [
            row[0] for row in cur.execute("SELECT id FROM element_types").fetchall()
        ]

faker = Faker("es_ES", use_weighting=False)
generator = EpicDataGenerator()

expansions = generator.generate(
    n=1000,
    table_name="expansions",
    spec={"id": lambda i: i, "name": lambda i: f"Expansion #{i}"},
)
expansion_ids = [ex["id"] for ex in expansions]

cards = generator.generate(
    n=2000,
    table_name="cards",
    spec={
        "num": lambda i: i,
        "rarity_id": lambda _: random.choice(rarity_ids),
        "expansion_id": lambda _: random.choice(expansion_ids),
    },
)

pokemon_cards = generator.generate(
    n=1700,
    table_name="pokemon_cards",
    spec={
        "num": lambda i: cards[i]["num"],
        "expansion_id": lambda i: cards[i]["expansion_id"],
        "element_type_id": lambda _: random.choice(element_type_ids),
        "name": lambda _: faker.name(),
        "description": lambda _: faker.sentence(),
        "hp": lambda _: random.randint(100, 1000),
        "retreat_cost": lambda _: random.randint(20, 200),
    },
)

evolutions_len = int(0.9 * len(pokemon_cards))
evolutions = [
    (random.randint(0, i - 1), i)
    for i in random.sample(range(1, len(pokemon_cards)), evolutions_len)
]
generator.generate(
    n=evolutions_len,
    n_strict=True,
    table_name="pokemon_card_evolves",
    spec={
        "to_num": lambda i: pokemon_cards[evolutions[i][1]]["num"],
        "to_expansion_id": lambda i: pokemon_cards[evolutions[i][1]]["expansion_id"],
        "from_num": lambda i: pokemon_cards[evolutions[i][0]]["num"],
        "from_expansion_id": lambda i: pokemon_cards[evolutions[i][0]]["expansion_id"],
    },
)

weaknesses_len = int(0.8 * len(pokemon_cards))
weaknesses = random.sample(range(len(pokemon_cards)), weaknesses_len)
generator.generate(
    n=weaknesses_len,
    n_strict=True,
    table_name="pokemon_card_weaknesses",
    spec={
        "card_num": lambda i: pokemon_cards[weaknesses[i]]["num"],
        "card_expansion_id": lambda i: pokemon_cards[weaknesses[i]]["expansion_id"],
        "element_type_id": lambda _: random.choice(element_type_ids),
    },
)

resistances_len = int(0.8 * len(pokemon_cards))
resistances = random.sample(range(len(pokemon_cards)), weaknesses_len)
generator.generate(
    n=resistances_len,
    n_strict=True,
    table_name="pokemon_card_resistances",
    spec={
        "card_num": lambda i: pokemon_cards[resistances[i]]["num"],
        "card_expansion_id": lambda i: pokemon_cards[resistances[i]]["expansion_id"],
        "element_type_id": lambda _: random.choice(element_type_ids),
        "value": lambda _: 10 * random.randint(1, 4),
    },
)

powered_pokemon_len = int(0.10 * len(pokemon_cards))
powered_pokemon = random.sample(range(len(pokemon_cards)), powered_pokemon_len)
powers_len = int(0.5 * powered_pokemon_len)

powers = generator.generate(
    n=powers_len,
    n_strict=True,
    table_name="pokemon_powers",
    spec={
        "id": lambda i: i,
        "name": lambda _: faker.word(),
        "description": lambda _: faker.sentence(),
    },
)

power_order = list(range(powers_len))
random.shuffle(power_order)

generator.generate(
    n=powered_pokemon_len,
    n_strict=True,
    table_name="pokemon_card_has_power",
    spec={
        "card_num": lambda i: pokemon_cards[powered_pokemon[i]]["num"],
        "card_expansion_id": lambda i: pokemon_cards[powered_pokemon[i]][
            "expansion_id"
        ],
        "power_id": lambda i: powers[power_order[i % powers_len]]["id"],
    },
)

attacks = generator.generate(
    n=1000,
    table_name="attacks",
    spec={
        "id": lambda i: i,
        "name": lambda _: faker.words(2),
        "description": lambda _: faker.sentence(),
        "damage": lambda _: 10 * random.randint(1, 15),
    },
)

attack_costs = []
for a in range(len(attacks)):
    n = random.randint(0, min(4, len(element_type_ids)))
    for t in random.sample(element_type_ids, n):
        attack_costs.append((a, t))

generator.generate(
    n=len(attack_costs),
    n_strict=True,
    table_name="attack_costs_element_type",
    spec={
        "attack_id": lambda i: attacks[attack_costs[i][0]]["id"],
        "element_type_id": lambda i: attack_costs[i][1],
        "amount": lambda _: random.randint(1, 3),
    },
)

pokemon_attacks = []
for a in range(len(attacks)):
    n = random.randint(1, 30)
    for p in random.sample(range(len(pokemon_cards)), n):
        pokemon_attacks.append((p, a))

generator.generate(
    n=len(pokemon_attacks),
    n_strict=True,
    table_name="pokemon_card_has_attack",
    spec={
        "card_num": lambda i: pokemon_cards[pokemon_attacks[i][0]]["num"],
        "card_expansion_id": lambda i: pokemon_cards[pokemon_attacks[i][0]][
            "expansion_id"
        ],
        "attack_id": lambda i: attacks[pokemon_attacks[i][1]]["id"],
    },
)

card_base = len(pokemon_cards)
trainer_cards = generator.generate(
    200,
    "trainer_cards",
    {
        "num": lambda i: cards[card_base + i]["num"],
        "expansion_id": lambda i: cards[card_base + i]["expansion_id"],
        "name": lambda i: faker.words(2),
        "description": lambda _: faker.sentence(),
    },
)

card_base += len(trainer_cards)
basic_energy_cards = generator.generate(
    80,
    "basic_energy_cards",
    {
        "num": lambda i: cards[card_base + i]["num"],
        "expansion_id": lambda i: cards[card_base + i]["expansion_id"],
        "element_type_id": lambda _: random.choice(element_type_ids),
    },
)

card_base += len(basic_energy_cards)
generator.generate(
    20,
    "special_energy_cards",
    {
        "num": lambda i: cards[card_base + i]["num"],
        "expansion_id": lambda i: cards[card_base + i]["expansion_id"],
        "name": lambda _: faker.words(2),
        "description": lambda _: faker.sentence(),
    },
)

users = generator.generate(
    2000,
    "users",
    {
        "id": str,
        "username": lambda i: f"{i}_{faker.user_name()}",
        "join_date": lambda _: faker.date_between("-5y"),
        "last_drop_date": lambda _: faker.date_time_between("-4m"),
    },
)

# Cada usuario tiene 0-50 cartas con cantidad entre 1 y 10
user_cards = []
for u in range(len(users)):
    n = random.randint(0, 50)
    for c in random.sample(range(len(cards)), n):
        user_cards.append((u, c))

generator.generate(
    n=len(user_cards),
    n_strict=True,
    table_name="user_owns_card",
    spec={
        "user_id": lambda i: users[user_cards[i][0]]["id"],
        "card_num": lambda i: cards[user_cards[i][1]]["num"],
        "card_expansion_id": lambda i: cards[user_cards[i][1]]["expansion_id"],
        "amount": lambda _: random.randint(1, 10),
    },
)

# Cada usuario tiene booster packs de 0-3 expansiones con cantidad entre 1 y 5
user_booster_packs = []
for u in range(len(users)):
    n = random.randint(0, min(3, len(expansion_ids)))
    for e in random.sample(expansion_ids, n):
        user_booster_packs.append((u, e))

generator.generate(
    n=len(user_booster_packs),
    n_strict=True,
    table_name="user_owns_booster_pack",
    spec={
        "user_id": lambda i: users[user_booster_packs[i][0]]["id"],
        "expansion_id": lambda i: user_booster_packs[i][1],
        "amount": lambda _: random.randint(1, 5),
    },
)
