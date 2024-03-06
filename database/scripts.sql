-- Crear la base de datos "store"
CREATE SCHEMA store;

-- Conectar a la base de datos "store"
USE store;



-- Tablas --------------------------------------------------------------------------------------------------------------------------------------

-- Crear la tabla "users"
CREATE TABLE users (
    id smallint unsigned NOT NULL AUTO_INCREMENT,
    username varchar(20) NOT NULL,
    password char(102) NOT NULL,
    fullname varchar(50),
    usertype tinyint NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Tabla de productos
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    imagen VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL
);





-- Procedimientos -----------------------------------------------------------------------------------------

-- Obtener usuarios
DELIMITER //

CREATE PROCEDURE obtener_usuarios()
BEGIN
    SELECT id, username, password, fullname, usertype FROM users;
END //
DELIMITER ;

-- Obtener usuarios por id
DELIMITER //
CREATE PROCEDURE obtener_usuario_por_id(in usuario_id INT)
BEGIN
    SELECT * FROM users WHERE id = usuario_id;
END //
DELIMITER ;

-- Agregar usuario
DELIMITER //
CREATE PROCEDURE sp_AddUser(IN pUserName VARCHAR(20), IN pPassword VARCHAR(102), IN pFullName VARCHAR(50), IN pUserType tinyint)
BEGIN
    DECLARE hashedPassword VARCHAR(255);
    SET hashedPassword = SHA2(pPassword, 256);
    
    INSERT INTO users (username, password, fullname, usertype)
    VALUES (pUserName, hashedPassword, pFullName, pUserType);
END //
DELIMITER ;


-- Actualizar usuario 
DELIMITER //
CREATE PROCEDURE actualizar_usuario(
    IN usuario_id INT,
    IN username VARCHAR(20),
    IN password VARCHAR(50),
    IN fullname VARCHAR(50),
    IN usertype TINYINT
)
BEGIN
    DECLARE new_hashed_password CHAR(102);

    -- Verifica si se proporciona una nueva contraseña
    IF password IS NOT NULL THEN
        -- Hash de la nueva contraseña
        SET new_hashed_password = SHA2(password, 256);
    ELSE
        -- Mantén la contraseña existente
        SET new_hashed_password = (SELECT password FROM users WHERE id = usuario_id);
    END IF;

    -- Actualiza la información del usuario
    UPDATE users
    SET username = username,
        password = new_hashed_password,
        fullname = fullname,
        usertype = usertype
    WHERE id = usuario_id;
END //
DELIMITER;


-- Eliminar usuarios

DELIMITER //

CREATE PROCEDURE eliminar_usuario(in usuario_id INT)
BEGIN
    DELETE FROM users WHERE id = usuario_id;
END //
DELIMITER ;

-- Obtener productos
DELIMITER //
CREATE PROCEDURE obtener_productos()
BEGIN
    SELECT * FROM productos;
END //
DELIMITER ;

-- Obtener un producto especifico por id
DELIMITER //

CREATE PROCEDURE obtener_producto_por_id(in producto_id INT)
BEGIN
    SELECT * FROM productos WHERE id = producto_id;
END //
DELIMITER ;

-- Agregar producto

DELIMITER //

CREATE PROCEDURE agregar_producto(in nombre VARCHAR(255), in imagen VARCHAR(255), in precio DECIMAL(10, 2))
BEGIN
    INSERT INTO productos (nombre, imagen, precio) VALUES (nombre, imagen, precio);
END //
DELIMITER ;

-- actualizar un producto
DELIMITER //

CREATE PROCEDURE actualizar_producto(in producto_id INT, in nombre VARCHAR(255), in imagen VARCHAR(255), in precio DECIMAL(10, 2))
BEGIN
    UPDATE productos SET nombre = nombre, imagen = imagen, precio = precio WHERE id = producto_id;
END //
DELIMITER ;

-- Eliminar un producto
DELIMITER //

CREATE PROCEDURE eliminar_producto(in producto_id INT)
BEGIN
    DELETE FROM productos WHERE id = producto_id;
END //

DELIMITER ;

-- Procedimiento para veridicar contraseña 
DELIMITER //
CREATE PROCEDURE sp_verifyIdentity(
    IN p_username VARCHAR(20),
    IN p_password VARCHAR(50)
)
BEGIN
    DECLARE hashed_password CHAR(102);

    -- Obtiene la contraseña almacenada para el nombre de usuario proporcionado
    SELECT password INTO hashed_password FROM users WHERE username = p_username;

    -- Compara la contraseña proporcionada con la almacenada
    IF hashed_password IS NOT NULL AND hashed_password = SHA2(p_password, 256) THEN
        -- Si las contraseñas coinciden, devuelve la información del usuario
        SELECT id, username, usertype, fullname FROM users WHERE username = p_username;
    ELSE
        -- Si las contraseñas no coinciden, devuelve NULL
        SELECT NULL;
    END IF;
END //
DELIMITER ;


call sp_AddUser("admin","123","juan perez",1);
call sp_AddUser("user","123","Usuario",2);
call sp_verifyIdentity("admin","123");
