from sqlalchemy import Column, ForeignKey, Integer, String, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Tabla de relación muchos a muchos para los favoritos
favoritos_planetas = Table('favoritos_planetas', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('planeta_id', Integer, ForeignKey('planetas.id'), primary_key=True)
)

favoritos_personajes = Table('favoritos_personajes', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('personaje_id', Integer, ForeignKey('personajes.id'), primary_key=True)
)

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    fecha_subscripcion = Column(String, nullable=False)

    planetas_favoritos = relationship('Planeta', secondary=favoritos_planetas, back_populates='usuarios')
    personajes_favoritos = relationship('Personaje', secondary=favoritos_personajes, back_populates='usuarios')

class Planeta(Base):
    __tablename__ = 'planetas'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    clima = Column(String)
    terreno = Column(String)
    
    usuarios = relationship('Usuario', secondary=favoritos_planetas, back_populates='planetas_favoritos')

class Personaje(Base):
    __tablename__ = 'personajes'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    especie = Column(String)
    genero = Column(String)
    
    usuarios = relationship('Usuario', secondary=favoritos_personajes, back_populates='personajes_favoritos')

# Tabla de ejemplo para Posts si se desea extender el blog
class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    titulo = Column(String, nullable=False)
    contenido = Column(String, nullable=False)
    
    user = relationship('Usuario', back_populates='posts')
    comentarios = relationship('Comentario', back_populates='post')

class Comentario(Base):
    __tablename__ = 'comentarios'
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    autor_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    comentario_texto = Column(String, nullable=False)
    
    post = relationship('Post', back_populates='comentarios')
    autor = relationship('Usuario', back_populates='comentarios')

# Relación con los posts y comentarios
Usuario.posts = relationship('Post', order_by=Post.id, back_populates='user')
Usuario.comentarios = relationship('Comentario', order_by=Comentario.id, back_populates='autor')
