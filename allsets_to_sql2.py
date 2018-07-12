import json
from hashlib import md5
from os import path
from datetime import datetime
from dateutil.parser import parse
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Boolean, MetaData
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()


class Set(Base):
    __tablename__ = 'sets'
    id = Column(String(4), primary_key=True)
    name = Column(String)
    code = Column(String)
    gatherer_code = Column(String)
    old_code = Column(String)
    magiccards_info_code = Column(String)
    release_date = Column(Date)
    border = Column(String)
    type = Column(String)
    block = Column(String)
    online_only = Column(Boolean)
    cards = relationship("Card", order_by="Card.id", backref="set")

    def __repr__(self):
        return "<User(id='%s', name='%s', release_date='%s')>" % (
            self.id, self.name, self.release_date)


class Card(Base):
    __tablename__ = 'cards'
    id = Column(String(40), primary_key=True)
    set_id = Column(String, ForeignKey('sets.id'), nullable=False)
    global_card_id = Column(String(32), ForeignKey('global_cards.id'),
                            nullable=False)
    rarity = Column(String)
    flavor = Column(String)
    artist = Column(String)
    number = Column(String)
    multiverseid = Column(Integer)
    watermark = Column(String)
    border = Column(String)
    timeshifted = Column(String)
    hand = Column(String)
    life = Column(String)
    reserved = Column(String)
    release_date = Column(Date)
    starter = Column(String)
    original_text = Column(String)
    original_type = Column(String)
    source = Column(String)
    mci_number = Column(Integer)
    foreign_names = relationship("ForeignName", backref="card")

    def __repr__(self):
        return "<Card(Name='%s' Set='%s')>" % (self.id, self.set_id)


class GlobalCard(Base):
    __tablename__ = 'global_cards'
    id = Column(String(32), primary_key=True)
    name = Column(String, nullable=False)
    layout = Column(String)
    oracle_text = Column(String)
    card_type = Column(String, nullable=False)
    mana_cost = Column(String)
    cmc = Column(Integer)
    power = Column(String)
    power_number = Column(Integer)
    power_non_integer = Column(Boolean)
    toughness = Column(String)
    toughness_number = Column(Integer)
    toughness_non_integer = Column(Boolean)
    loyalty = Column(String)
    cards = relationship("Card", backref="global_card")
    names = relationship("Name", backref="global_card")
    colors = relationship("Color", backref="global_card")
    supertypes = relationship("Supertype", backref="global_card")
    types = relationship("Type", backref="global_card")
    variations = relationship("Variation", backref="global_card")
    rulings = relationship("Ruling", backref="global_card")
    legalities = relationship("Legality", backref="global_card")
    color_identities = relationship("ColorIdentity", backref="global_card")

    def __repr__(self):
        return "<GlobalCard(Name='%s')>" % self.name


class Name(Base):
    __tablename__ = 'names'
    id = Column(Integer, primary_key=True)
    global_card_id = Column(String(32), ForeignKey('global_cards.id'),
                            nullable=False)
    name = Column(String)

    def __repr__(self):
        return "<Name(global_card_id='%s', name='%s')>" % \
            (self.global_card_id, self.name)


class Color(Base):
    __tablename__ = 'colors'
    id = Column(Integer, primary_key=True)
    global_card_id = Column(String(32), ForeignKey('global_cards.id'),
                            nullable=False)
    color = Column(String)

    def __repr__(self):
        return "<Color(global_card_id='%s', color='%s')>" % \
            (self.global_card_id, self.color)


class Supertype(Base):
    __tablename__ = 'supertypes'
    id = Column(Integer, primary_key=True)
    global_card_id = Column(String(32), ForeignKey('global_cards.id'),
                            nullable=False)
    supertype = Column(String)

    def __repr__(self):
        return "<Supertype(global_card_id='%s', Type='%s')>" % \
            (self.global_card_id, self.type)


class Type(Base):
    __tablename__ = 'types'
    id = Column(Integer, primary_key=True)
    global_card_id = Column(String(32), ForeignKey('global_cards.id'),
                            nullable=False)
    type = Column(String, nullable=False)

    def __repr__(self):
        return "<Type(global_card_id='%s', Type='%s')>" % \
            (self.global_card_id, self.type)


class Variation(Base):
    __tablename__ = 'variations'
    id = Column(Integer, primary_key=True)
    global_card_id = Column(String(32), ForeignKey('global_cards.id'),
                            nullable=False)
    variation_multiverseid = Column(Integer, ForeignKey('cards.multiverseid'),
                                    nullable=False)

    def __repr__(self):
        return "<Variation(global_card_id='%s', Variation='%s')>" % \
            (self.global_card_id, self.variation)


class Ruling(Base):
    __tablename__ = "rulings"
    id = Column(Integer, primary_key=True)
    global_card_id = Column(String(32), ForeignKey('global_cards.id'),
                            nullable=False)
    ruling_date = Column(Date, nullable=False)
    ruling_text = Column(String, nullable=False)

    def __repr__(self):
        return "<Ruling(global_card_id='%s', Date='%s', Text='%s')>" % \
            (self.global_card_id, self.ruling_date, self.ruling_text)


class ForeignName(Base):
    __tablename__ = "foreign_names"
    id = Column(Integer, primary_key=True)
    card_id = Column(String(40), ForeignKey('cards.id'), nullable=False)
    language = Column(String, nullable=False)
    foreign_name = Column(String, nullable=False)
    foreign_multiverseid = Column(Integer)  # ForeignKey('cards.multiverseid'))

    def __repr__(self):
        return "<ForeignName(card_id='%s', Language='%s', Name='%s')>" % \
            (self.card_id, self.language, self.foreign_name)


class Legality(Base):
    __tablename__ = "legalities"
    id = Column(Integer, primary_key=True)
    global_card_id = Column(String(32), ForeignKey('global_cards.id'),
                            nullable=False)
    legality_format = Column(String, nullable=False)
    legality = Column(String, nullable=False)

    def __repr__(self):
        return "<Legality(global_card_id='%s', Format='%s', Legality='%s')>" %\
            (self.global_card_id, self.legality_format, self.legality)


class ColorIdentity(Base):
    __tablename__ = 'color_identities'
    id = Column(Integer, primary_key=True)
    global_card_id = Column(String(32), ForeignKey('global_cards.id'),
                            nullable=False)
    color_identity = Column(String)

    def __repr__(self):
        return "<Color(global_card_id='%s', color='%s')>" % \
            (self.global_card_id, self.color)


###############################################################################
# done with ORM definitions, let's load the data!
basedir = path.abspath(path.dirname(__file__))

engine = create_engine('sqlite:///' + path.join(basedir, 'data-mtg.sqlite'),
                       echo=False)

Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

with open('AllSets-x.json') as file:
    data = json.load(file)

# load up database

count = 0
length = len(data)
for setkey, setitem in data.items():
    count = count + 1
    print('\nprocessing set {0}, {1} of {2}'.format(setkey, count, length))
    # create the set object to add to the database
    set_item = Set(id=setkey)

    set_item.name = setitem['name']
    set_item.code = setitem['code']
    if 'gathererCode' in setitem:
        set_item.gatherer_code = setitem['gathererCode']
    if 'oldCode' in setitem:
        set_item.old_code = setitem['oldCode']
    if 'magicCardsInfoCode' in setitem:
        set_item.magiccards_info_code = setitem['magicCardsInfoCode']
    if 'releaseDate' in setitem:
        set_item.release_date = parse(setitem['releaseDate'])
    set_item.border = setitem['border']
    if 'type' in setitem:
        set_item.type = setitem['type']
    if 'block' in setitem:
        set_item.block = setitem['block']
    if 'onlineOnly' in setitem:
        set_item.online_only = setitem['onlineOnly']

    cards_count = 0
    cards_length = len(setitem["cards"])
    for card in setitem["cards"]:
        cards_count = cards_count + 1
        print(' card {0}/{1}\r'.format(cards_count, cards_length), end='')
        # always expect these values:
        card_id = card["id"]

        global_card_id = md5(card["name"].encode("utf8")).hexdigest()

        card_item = Card(id=card_id)

        card_item.global_card_id = global_card_id

        # check for whether or not the global_card has already been created.
        global_card_item = session.query(GlobalCard).filter_by(
            id=global_card_id).first()

        if not global_card_item:
            global_card_item = GlobalCard(id=global_card_id, name=card["name"])

            global_card_item.layout = card["layout"]

            global_card_item.card_type = card["type"]

            if "manaCost" in card:
                global_card_item.mana_cost = card["manaCost"]

            if "cmc" in card:
                global_card_item.cmc = card["cmc"]

            if "text" in card:
                global_card_item.oracle_text = card["text"]

            if "power" in card:
                global_card_item.power = card["power"]
                # try parsing the value stored in power as an integer
                try:
                    global_card_item.power_number = int(card["power"])
                except ValueError:
                    global_card_item.power_non_integer = True

            if "toughness" in card:
                global_card_item.toughness = card["toughness"]
                # try parsing the value stored in toughness as an integer
                try:
                    global_card_item.toughness_number = int(card["toughness"])
                except ValueError:
                    global_card_item.toughness_non_integer = True

            if "loyalty" in card:
                global_card_item.loyalty = card["loyalty"]

            # save multiple values to their own tables
            if "names" in card:
                for mult_name in card["names"]:
                    name_item = Name(name=mult_name)
                    global_card_item.names.append(name_item)

            if "colors" in card:
                for mult_color in card["colors"]:
                    color_item = Color(color=mult_color)
                    global_card_item.colors.append(color_item)

            if "supertypes" in card:
                for mult_supertype in card["supertypes"]:
                    supertype_item = Supertype(supertype=mult_supertype)
                    global_card_item.supertypes.append(supertype_item)

            if "types" in card:
                for mult_type in card["types"]:
                    type_item = Type(type=mult_type)
                    global_card_item.types.append(type_item)

            if "variations" in card:
                for mult_variation in card["variations"]:
                    variation_item = Variation(
                        variation_multiverseid=mult_variation)
                    global_card_item.variations.append(variation_item)

            if "rulings" in card:
                for mult_ruling in card["rulings"]:
                    ruling_item = Ruling(ruling_date=datetime.strptime(
                        (mult_ruling['date']),
                        "%Y-%m-%d").date(),
                        ruling_text=mult_ruling["text"])
                    global_card_item.rulings.append(ruling_item)

            if "legalities" in card:
                for mult_legality in card["legalities"]:
                    legality_item = Legality(
                        legality_format=mult_legality["format"],
                        legality=mult_legality["legality"])
                    global_card_item.legalities.append(legality_item)

            if "colorIdentity" in card:
                for mult_color_identity in card["colorIdentity"]:
                    color_identity_item = ColorIdentity(
                        color_identity=mult_color_identity)
                    global_card_item.color_identities.append(
                        color_identity_item)

            # add new global card item to the session here since we created it
            session.add(global_card_item)

        # check that the following keys are present before accessing:
        if "rarity" in card:
            card_item.rarity = card["rarity"]

        if "flavor" in card:
            card_item.flavor = card["flavor"]

        if "artist" in card:
            card_item.artist = card["artist"]

        if "number" in card:
            card_item.number = card["number"]

        if "multiverseid" in card:
            card_item.multiverseid = card["multiverseid"]

        if "watermark" in card:
            card_item.watermark = card["watermark"]

        if "border" in card:
            card_item.border = card["border"]

        if "timeshifted" in card:
            card_item.timeshifted = card["timeshifted"]

        if "hand" in card:
            card_item.hand = card["hand"]

        if "life" in card:
            card_item.life = card["life"]

        if "reserved" in card:
            card_item.reserved = card["reserved"]

        if "releaseDate" in card:
            card_item.release_date = parse(card["releaseDate"])

        if "starter" in card:
            card_item.starter = card["starter"]

        if "originalText" in card:
            card_item.original_text = card["originalText"]

        if "originalType" in card:
            card_item.original_type = card["originalType"]

        if "source" in card:
            card_item.source = card["source"]

        if "mciNumber" in card and card["mciNumber"].isdigit():
            card_item.mci_number = card["mciNumber"]

        if "foreignNames" in card:
            for mult_foreign_name in card["foreignNames"]:
                foreign_name_item = ForeignName(
                    language=mult_foreign_name["language"],
                    foreign_name=mult_foreign_name["name"])
                if "multiverseid" in mult_foreign_name:
                    foreign_name_item.foreign_multiverseid = \
                        mult_foreign_name["multiverseid"]
                card_item.foreign_names.append(foreign_name_item)

        set_item.cards.append(card_item)
        global_card_item.cards.append(card_item)
    session.add(set_item)
session.commit()
print('\nDone!')
