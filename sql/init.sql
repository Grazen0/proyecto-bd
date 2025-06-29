CREATE TABLE rarities (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  CHECK (LENGTH (name) > 0)
);

CREATE TABLE element_types (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  CHECK (LENGTH (name) > 0)
);

CREATE TABLE expansions (
  id INT PRIMARY KEY,
  name VARCHAR(50) UNIQUE,
  CHECK (LENGTH (name) > 0)
);

CREATE TABLE cards (
  num INT NOT NULL,
  expansion_id INT NOT NULL REFERENCES expansions (id),
  rarity_id INT NOT NULL REFERENCES rarities (id),
  PRIMARY KEY (num, expansion_id)
);

CREATE TABLE pokemon_cards (
  num INT NOT NULL,
  expansion_id INT NOT NULL,
  element_type_id INT NOT NULL REFERENCES element_types (id),
  name VARCHAR(50) NOT NULL,
  description VARCHAR(300) NOT NULL,
  hp INT NOT NULL,
  retreat_cost INT NOT NULL,
  FOREIGN KEY (num, expansion_id) REFERENCES cards (num, expansion_id),
  PRIMARY KEY (num, expansion_id),
  CHECK (
    LENGTH (name) > 0
    AND LENGTH (description) > 0
  )
);

CREATE TABLE pokemon_card_evolves (
  to_num INT NOT NULL,
  to_expansion_id INT NOT NULL,
  from_num INT NOT NULL,
  from_expansion_id INT NOT NULL,
  FOREIGN KEY (to_num, to_expansion_id) REFERENCES pokemon_cards (num, expansion_id),
  FOREIGN KEY (from_num, from_expansion_id) REFERENCES pokemon_cards (num, expansion_id),
  PRIMARY KEY (to_num, to_expansion_id)
);

CREATE TABLE pokemon_card_weaknesses (
  card_num INT NOT NULL,
  card_expansion_id INT NOT NULL,
  element_type_id INT NOT NULL REFERENCEs element_types (id),
  FOREIGN KEY (card_num, card_expansion_id) REFERENCES pokemon_cards (num, expansion_id),
  PRIMARY KEY (card_num, card_expansion_id)
);

CREATE TABLE pokemon_card_resistances (
  card_num INT NOT NULL,
  card_expansion_id INT NOT NULL,
  element_type_id INT NOT NULL REFERENCEs element_types (id),
  value INT NOT NULL,
  FOREIGN KEY (card_num, card_expansion_id) REFERENCES pokemon_cards (num, expansion_id),
  PRIMARY KEY (card_num, card_expansion_id)
);

CREATE TABLE pokemon_powers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50),
  description VARCHAR(300) NOT NULL,
  CHECK (
    LENGTH (name) > 0
    AND LENGTH (description) > 0
  )
);

CREATE TABLE pokemon_card_has_power (
  card_num INT NOT NULL,
  card_expansion_id INT NOT NULL,
  power_id INT NOT NULL REFERENCES pokemon_powers (id),
  FOREIGN KEY (card_num, card_expansion_id) REFERENCES pokemon_cards (num, expansion_id),
  PRIMARY KEY (card_num, card_expansion_id)
);

CREATE TABLE attacks (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(300) NOT NULL,
  damage INT NOT NULL,
  CHECK (
    damage > 0
    AND LENGTH (name) > 0
    AND LENGTH (description) > 0
  )
);

CREATE TABLE attack_costs_element_type (
  attack_id INT NOT NULL REFERENCES attacks (id),
  element_type_id INT NOT NULL REFERENCES element_types (id),
  amount INT NOT NULL,
  CHECK (amount > 0)
);

CREATE TABLE pokemon_card_has_attack (
  card_num INT NOT NULL,
  card_expansion_id INT NOT NULL,
  attack_id INT NOT NULL REFERENCES attacks (id),
  FOREIGN KEY (card_num, card_expansion_id) REFERENCES pokemon_cards (num, expansion_id),
  PRIMARY KEY (card_num, card_expansion_id, attack_id)
);

CREATE TABLE trainer_cards (
  num INT NOT NULL,
  expansion_id INT NOT NULL,
  name VARCHAR(50),
  description VARCHAR(300),
  FOREIGN KEY (num, expansion_id) REFERENCES cards (num, expansion_id),
  PRIMARY KEY (num, expansion_id),
  CHECK (
    LENGTH (name) > 0
    AND LENGTH (description) > 0
  )
);

CREATE TABLE basic_energy_cards (
  num INT NOT NULL,
  expansion_id INT NOT NULL,
  element_type_id INT NOT NULL REFERENCES element_types (id),
  FOREIGN KEY (num, expansion_id) REFERENCES cards (num, expansion_id),
  PRIMARY KEY (num, expansion_id)
);

CREATE TABLE special_energy_cards (
  num INT NOT NULL,
  expansion_id INT NOT NULL,
  name VARCHAR(50),
  description VARCHAR(300),
  FOREIGN KEY (num, expansion_id) REFERENCES cards (num, expansion_id),
  PRIMARY KEY (num, expansion_id),
  CHECK (
    LENGTH (name) > 0
    AND LENGTH (description) > 0
  )
);

CREATE TABLE users (
  id VARCHAR(50) PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  join_date TIMESTAMP NOT NULL DEFAULT NOW (),
  last_drop_date TIMESTAMP
);

CREATE TABLE user_owns_card (
  user_id VARCHAR(50) NOT NULL REFERENCES users (id),
  card_num INT NOT NULL,
  card_expansion_id INT NOT NULL,
  amount INT NOT NULL,
  FOREIGN KEY (card_num, card_expansion_id) REFERENCES cards (num, expansion_id),
  PRIMARY KEY (user_id, card_num, card_expansion_id),
  CHECK (amount > 0)
);

CREATE TABLE user_owns_booster_pack (
  user_id VARCHAR(50) NOT NULL REFERENCES users (id),
  expansion_id INT NOT NULL REFERENCES expansions (id),
  amount INT NOT NULL,
  PRIMARY KEY (user_id, expansion_id),
  CHECK (amount > 0)
);
