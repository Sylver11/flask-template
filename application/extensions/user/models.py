from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from application.database import db, Base


user_role_assoc = db.Table('na_user_role_assoc',
        db.Column('id', db.Integer(), primary_key=True),
        db.Column('user_uuid', db.ForeignKey('na_user.uuid')),
        db.Column('role_uuid', db.ForeignKey('na_user_role.uuid')))

role_hierachy_assoc = db.Table('na_user_role_hierachy',
        db.Column('id', db.Integer(), primary_key=True),
        db.Column('parent_role_uuid', db.ForeignKey('na_user_role.uuid')),
        db.Column('child_role_uuid', db.ForeignKey('na_user_role.uuid')))

role_ability_assoc = db.Table('na_user_role_ability_assoc',
        db.Column('id', db.Integer(), primary_key=True),
        db.Column('role_uuid', db.ForeignKey('na_user_role.uuid')),
        db.Column('ability_uuid', db.ForeignKey('na_user_role_ability.uuid')))


class Ability(Base):
    __tablename__ = 'na_user_role_ability'
    name:str
    name = db.Column(db.String(120), unique=True)

    def __init__(self, name):
        self.name = name.lower()


class Role(Base):
    __tablename__ = 'na_user_role'
    name:str
    description:str
    abilities:str
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    child_roles = relationship(
            'Hierachy',
            secondary= role_hierachy_assoc,
            primaryjoin='Role.uuid==role_hierachy_assoc.parent_role_uuid',
            secondaryjoin='Role.uuid==role_hierachy_assoc.child_role_uuid',
            backref="parent_roles")
#    abilities = relationship(
#            'Ability',
#            secondary=role_ability_assoc,
#            backref=db.backref('roles', lazy='dynamic'))

    def __init__(self, name):
        self.name = name.lower()

    def add_abilities(self, *abilities):
        for ability in abilities:
            existing_ability = Ability.query.filter_by(
                name=ability).first()
            if not existing_ability:
                existing_ability = Ability(ability)
                db.session.add(existing_ability)
                db.session.commit()
            self.abilities.append(existing_ability)

    def remove_abilities(self, *abilities):
        for ability in abilities:
            existing_ability = Ability.query.filter_by(name=ability).first()
            if existing_ability and existing_ability in self.abilities:
                self.abilities.remove(existing_ability)




class User(Base):
    __tablename__ = 'na_user'

    def __init__(self, roles=None, default_role='user'):
        if roles and isinstance(roles, str):
            roles = [roles]
        if roles and is_sequence(roles):
            self.roles = roles
        elif default_role:
            self.roles = [default_role]

    firstname = db.Column(db.String(255),index=True, nullable=False)
    secondname = db.Column(db.String(255), index=True, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    thirdparty_authenticated = db.Column(db.Boolean, nullable=False,
            default=False)
    thirdparty_name = db.Column(db.String(255))
    authenticated = db.Column(db.Boolean, nullable=False, default=False)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    roles = relationship('Role', secondary=user_role_assoc,
            backref=db.backref('users', lazy='dynamic'))

    def get_id(self):
        return self.uuid

    def is_authenticated(self):
        return self.authenticated

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

#    def has_roles(self, *requirements):
#        for requirement in requirements:
#            if isinstance(requirement, (list, tuple)):
#                tuple_of_role_names = requirement
#                authorised = False
#                for role_name in tuple_of_role_names:
#                    if role_name in self.roles:
#                        authorised = True
#                        break
#                    if not authorised:
#                        return False
#            else:
#                role_name = requirement
#                if not role_name in self.roles:
#                    return False
#        return True

#    def has_ability(self, *abilites):
#        pass

    def add_roles(self, *roles):
        self.roles.extend([role for role in roles if role not in self.roles])

    def remove_roles(self, *roles):
        self.roles = [role for role in self.roles if role not in roles]




