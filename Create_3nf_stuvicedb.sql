DROP DATABASE IF EXISTS stuvicedb ;

CREATE DATABASE stuvicedb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;

USE stuvicedb;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `firstname` varchar(50) NOT NULL,
  `lastname` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL UNIQUE,
  `password` TEXT NOT NULL,
  `phone` varchar(20) NOT NULL,
  `school` varchar(50) NOT NULL,
  `sex` enum('0','1') not null,
  `date_of_birth` datetime not null,
  `about_me` text,
  `street` varchar(255),
  `city` varchar(100),
  `state` varchar(100),
  `postal_code` varchar(20),
  `status` ENUM('active','inactive') DEFAULT 'active',
  `verified` ENUM('1','0') default '0',
  `picture` blob,
  `overallrate` float default 0.0,
  `fb_token` varchar(250) DEFAULT NULL,
  `fb_id` bigint DEFAULT NULL,
  PRIMARY KEY (`user_id`)
);

CREATE TABLE `service_categories`(
	`category_id` INT NOT NULL AUTO_INCREMENT,
 	`category_name` VARCHAR(100) NOT NULL unique,   
	`category_description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (category_id)
);

CREATE TABLE `user_services` (
  `service_id` int NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  `service_name` varchar(1000) NOT NULL,
  `description` text NOT NULL,
  `point` float default 0,
  `price` float NOT NULL,
  `unit` varchar(200) default NULL,
  `totalrequest` int NOT NULL default '0',
  `totalaccepted` int NOT NULL default '0',
  `totaldeclined` int NOT NULL default '0',
  `acceptrate` float NOT NULL default '0',
  `declinerate` float NOT NULL default '0',
  `averagerate` float NOT NULL DEFAULT '0',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `available` enum('1','0') NOT NULL DEFAULT '1',
  PRIMARY KEY (`service_id`),
  CONSTRAINT `userservice_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `service_category_id_fk` FOREIGN KEY (`category_id`) REFERENCES `service_categories` (`category_id`) ON DELETE CASCADE
);
CREATE TABLE `user_notifications` (
  `notification_id` int NOT NULL AUTO_INCREMENT,
  `recipient_id` int not null,
  `sender_id` int not null,
  `notification_type` enum('friends','service','group') default null,
  `id` int default null,
  `message` text,
  `is_read` boolean default false,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL,
    PRIMARY KEY (`notification_id`),
	CONSTRAINT notification_recepient_id_fk FOREIGN KEY (recipient_id) REFERENCES users (user_id),
    CONSTRAINT notification_sender_id_fk FOREIGN KEY (sender_id) REFERENCES `users` (user_id) ON DELETE CASCADE
);



CREATE TABLE `service_requests` (
  `request_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `to_date` datetime NOT NULL,
  `price` float not NULL,
  `from_date` datetime NOT NULL,
  `created_at` datetime not null default current_timestamp,
  `status` enum('pending', 'accepted', 'declined') NOT NULL DEFAULT 'pending',
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`request_id`,`status`),
  UNIQUE KEY `request_id_status_unique` (`request_id`, `status`),
  KEY `service_id` (`service_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `service_requests_ibfk_1` FOREIGN KEY (`service_id`) REFERENCES `user_services` (`service_id`) ON DELETE CASCADE,
  CONSTRAINT `service_requests_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
);



CREATE TABLE `completed_service_requests` (
  `completed_requests_id` int NOT NULL AUTO_INCREMENT,
  `request_id` int NOT NULL,
  `started_at` datetime NOT NULL,
  `complete_at` DATETIME NOT NULL,
  `settled_price` float NOT NULL,
  `payment_amount` float NOT NULL,
  PRIMARY KEY (`completed_requests_id`),
  CONSTRAINT `completedrequests_request_id_fk` FOREIGN KEY (`completed_requests_id`) REFERENCES `service_requests` (`request_id`) ON DELETE CASCADE
);

CREATE TABLE `service_reviews` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `service_id` int NOT NULL,
  `user_id` int NOT NULL, 
  `rating` float NOT NULL,
  `comment` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`review_id`),
  CONSTRAINT `service_reviews_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `service_reviews_service_fk` FOREIGN KEY (`service_id`) REFERENCES `user_services` (`service_id`) ON DELETE CASCADE
);

CREATE TABLE `wall_posts` (
  `wall_post_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `post_message` text NOT NULL,
  `post_picture` blob,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`wall_post_id`),
  CONSTRAINT `wall_post_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
);

CREATE TABLE `wall_posts_comments` (
  `comment_id` int NOT NULL AUTO_INCREMENT,
  `wall_post_id` int NOT NULL,
  `comment` text NOT NULL,
  `user_id` int NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`comment_id`),
  CONSTRAINT `comments_wall_posts_fk` FOREIGN KEY (`wall_post_id`) REFERENCES `wall_posts` (`wall_post_id`) ON DELETE CASCADE,
  CONSTRAINT `comments_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
);

CREATE TABLE `wall_post_likes` (
  `like_id` int NOT NULL AUTO_INCREMENT,
  `wall_post_id` int NOT NULL,
  `user_id` int NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_id` TIMESTAMP NOT NULL DEFAULT current_timestamp ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`like_id`),
  CONSTRAINT `likes_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (user_id),
  CONSTRAINT `likes_wall_post_fk` FOREIGN KEY (`wall_post_id`) REFERENCES `wall_posts` (`wall_post_id`)
);

CREATE TABLE `friends` (
   `id` int not null auto_increment,
  `user_id` int NOT NULL,
  `friend_id` int NOT NULL,
  `status` ENUM('pending','accepted','declined') NOT NULL DEFAULT 'pending',  
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_id` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  primary key(`id`),
  CONSTRAINT `unique_user_friend_pair` UNIQUE (`user_id`, `friend_id`),
  CONSTRAINT `friends_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `friends_friend_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
);


CREATE TABLE `messages` (
  `message_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `recipient_id` int NOT NULL,
  `message` text NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_read` enum('1','0') NOT NULL DEFAULT '0',
  PRIMARY KEY (`message_id`),
  CONSTRAINT `messages_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `messages_recipient_id` FOREIGN KEY (`recipient_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
);

DROP PROCEDURE IF EXISTS create_user;
DELIMITER $$
CREATE PROCEDURE create_user (
    IN firstname VARCHAR(255), 
    IN lastname VARCHAR(255), 
    IN email VARCHAR(255), 
    IN password VARCHAR(255),
    IN phone VARCHAR(12),
    IN sex ENUM('0', '1'),
    IN school VARCHAR(50),
    IN date_of_birth DATETIME
)
BEGIN
    INSERT INTO users (
        firstname, 
        lastname, 
        email, 
        password,
        phone,
        sex,
        school,
        date_of_birth
    ) VALUES (
        firstname, 
        lastname, 
        email, 
        password,
        phone,
        sex,
        school,
        date_of_birth
    );
END $$
DELIMITER ;

-- GET USER BY ID PROCEDURE
DROP PROCEDURE IF EXISTS get_user_by_id;
DELIMITER $$
CREATE PROCEDURE get_user_by_id (IN user_id INT)
BEGIN
    SELECT * FROM users WHERE users.user_id = user_id;
END $$
DELIMITER ;

-- Update user info
DROP PROCEDURE IF EXISTS update_user;
DELIMITER $$
CREATE PROCEDURE update_user (
    IN p_user_id INT,
    IN p_firstname VARCHAR(2000),
    IN p_lastname VARCHAR(2000),
    IN p_email VARCHAR(2000),
    IN p_phone VARCHAR(12),
    IN p_school VARCHAR(50),
    IN p_sex ENUM('0', '1'),
    IN p_date_of_birth DATETIME,
    IN p_about_me text
)
BEGIN
    UPDATE users
    SET
        firstname = COALESCE(p_firstname, firstname),
        lastname = COALESCE(p_lastname, lastname),
        email = COALESCE(p_email, email),
        phone = COALESCE(p_phone, phone),
        school = COALESCE(p_school, school),
        sex = COALESCE(p_sex, sex),
        date_of_birth = COALESCE(p_date_of_birth, date_of_birth),
        about_me = COALESCE(p_about_me, about_me)
    WHERE
        user_id = p_user_id;
END $$
DELIMITER ;


-- ADD SERVICE TO USER First check if category exists and get id PROCEDURE
DROP PROCEDURE IF EXISTS add_service_to_user;
DELIMITER $$
CREATE PROCEDURE add_service_to_user(
    IN user_id INT,
    IN category_name_in VARCHAR(255),
    IN service_name VARCHAR(255),
    IN price FLOAT,
    IN description TEXT
)
BEGIN
    DECLARE category_id INT;
    
    SELECT sc.category_id INTO category_id FROM service_categories sc WHERE sc.category_name = category_name_in limit 1;
    
    IF category_id IS NULL THEN
        INSERT INTO service_categories (category_name) VALUES (category_name_in);
        SET category_id = LAST_INSERT_ID();
    END IF;
    
    INSERT INTO user_services (user_id, category_id, service_name, price, description)
    VALUES (user_id, category_id, service_name, price, description);
    
END $$
DELIMITER ;

-- UPDATE User service 
DROP PROCEDURE IF EXISTS update_service;
DELIMITER $$
CREATE PROCEDURE update_service(IN service_id INT, IN category_name_in VARCHAR(255), IN service_name VARCHAR(255), IN price FLOAT, IN description TEXT)
BEGIN
    DECLARE category_id INT;
	SELECT sc.category_id INTO category_id FROM service_categories sc WHERE sc.category_name = category_name_in limit 1;
    
    IF category_id IS NULL THEN
        INSERT INTO service_categories (category_name) VALUES (category_name_in);
        SET category_id = LAST_INSERT_ID();
    END IF;
    UPDATE user_services SET category_id = category_id, service_name = service_name, price = price, description = description WHERE service_id = service_id;
END $$
DELIMITER ;


-- SEND SERVICE REQUEST 
DROP PROCEDURE IF EXISTS add_service_request;
DELIMITER $$
CREATE PROCEDURE add_service_request(IN p_service_id INT, IN p_message TEXT, IN p_to_date DATETIME, IN p_from_date DATETIME, IN p_user_id INT, IN p_service_name VARCHAR(100), IN p_price float)
BEGIN
    INSERT INTO service_requests (service_id, message, to_date, from_date, user_id,price)
    VALUES (p_service_id, p_message, p_to_date, p_from_date, p_user_id,p_price);
END $$
DELIMITER ;

-- update service request procedure

DROP PROCEDURE IF EXISTS update_service_request;
DELIMITER $$

CREATE PROCEDURE update_service_request(
    IN p_request_id INT,
    IN p_service_id INT,
    IN p_message TEXT,
    IN p_to_date DATE,
    IN p_from_date DATE,
    IN p_user_id INT
)
BEGIN
    UPDATE service_requests
    SET service_id = p_service_id,
        message = p_message,
        to_date = p_to_date,
        from_date = p_from_date,
        user_id = p_user_id
    WHERE request_id = p_request_id;
END $$

DELIMITER ;

-- cancel service request procedure

DROP PROCEDURE IF EXISTS cancel_service_request;
DELIMITER $$

CREATE PROCEDURE cancel_service_request(
    IN p_request_id INT
)
BEGIN
    UPDATE service_requests
    SET status = 'declined'
    WHERE service_requests.request_id = p_request_id;
END $$

DELIMITER ;

-- update notification procedure

DROP TRIGGER IF EXISTS update_user_notification_trigger1;

DELIMITER $$
CREATE TRIGGER update_user_notification_trigger1
AFTER INSERT ON friends
FOR EACH ROW
BEGIN
  INSERT INTO user_notifications (recipient_id, sender_id, message, created_at, notification_type,id)
  VALUES (NEW.friend_id, NEW.user_id, CONCAT((SELECT CONCAT(firstname, ' ', lastname) FROM users WHERE user_id = NEW.user_id), ' sent you a friend request'), NOW(), 'friends',New.id);
END $$
DELIMITER ;

DROP TRIGGER IF EXISTS update_user_notification_trigger2;

DELIMITER $$
CREATE TRIGGER update_user_notification_trigger2
AFTER UPDATE ON friends
FOR EACH ROW
BEGIN
  IF NEW.status = 'accepted' THEN
    INSERT INTO user_notifications (recipient_id, sender_id, message, created_at, notification_type,id)
    VALUES (NEW.user_id, NEW.friend_id, CONCAT((SELECT CONCAT(firstname, ' ', lastname) FROM users WHERE user_id = NEW.friend_id), ' accepted your friend request'), NOW(), 'friends',New.id);
  ELSEIF NEW.status = 'declined' THEN
    INSERT INTO user_notifications (recipient_id, sender_id, message, created_at, notification_type,id)
    VALUES (NEW.user_id, NEW.friend_id, CONCAT((SELECT CONCAT(firstname, ' ', lastname) FROM users WHERE user_id = NEW.friend_id), ' declined your friend request'), NOW(), 'friends',New.id);
  END IF;
END $$
DELIMITER ;

DROP TRIGGER IF EXISTS update_user_notification_trigger3;

DELIMITER $$
CREATE TRIGGER update_user_notification_trigger3
AFTER INSERT ON service_requests
FOR EACH ROW
BEGIN
   IF NEW.status = 'pending' THEN
    INSERT INTO user_notifications (recipient_id, sender_id, message, created_at, notification_type,id)
    VALUES ((SELECT user_id FROM user_services WHERE service_id = NEW.service_id), NEW.user_id, CONCAT((SELECT CONCAT(firstname, ' ', lastname) FROM users WHERE user_id = NEW.user_id), ' sent you a service request for ', (SELECT service_name FROM user_services WHERE service_id = NEW.service_id)), NOW(), 'service',New.request_id);
  ELSEIF NEW.status = 'accepted' THEN
    INSERT INTO user_notifications (recipient_id, sender_id, message, created_at, notification_type, id)
     VALUES ((SELECT user_id FROM service_requests WHERE request_id = NEW.request_id AND status = 'pending'),
        (SELECT user_id FROM user_services WHERE service_id = NEW.service_id),
        CONCAT((SELECT CONCAT(firstname, ' ', lastname) FROM users WHERE user_id = NEW.user_id), ' accepted your service request for ', (SELECT service_name FROM user_services WHERE service_id = NEW.request_id)),
        NOW(),
        'service',
        NEW.service_id);

  ELSEIF NEW.status = 'declined' THEN
    INSERT INTO user_notifications (recipient_id, sender_id, message, created_at, notification_type,id)
    VALUES ( NEW.user_id,(SELECT user_id FROM user_services WHERE service_id = NEW.service_id), CONCAT('You cancelled your service request for ', (SELECT service_name FROM user_services WHERE service_id = NEW.service_id)), NOW(), 'service',New.request_id);
  END IF;
END $$
DELIMITER ;

DROP TRIGGER IF EXISTS update_user_notification_trigger4;

DELIMITER $$
CREATE TRIGGER update_user_notification_trigger4
AFTER UPDATE ON service_requests
FOR EACH ROW
BEGIN
  IF NEW.status = 'sent' THEN
    INSERT INTO user_notifications (recipient_id, sender_id, message, created_at, notification_type,id)
    VALUES ((SELECT user_id FROM user_services WHERE service_id = NEW.service_id), NEW.user_id, CONCAT((SELECT CONCAT(firstname, ' ', lastname) FROM users WHERE user_id = NEW.user_id), ' sent you a service request for ', (SELECT service_name FROM user_services WHERE service_id = NEW.service_id)), NOW(), 'service',New.request_id);
  ELSEIF NEW.status = 'accepted' THEN
    INSERT INTO user_notifications (recipient_id, sender_id, message, created_at, notification_type,id)
    VALUES (NEW.user_id, (SELECT user_id FROM user_services WHERE service_id = NEW.service_id), CONCAT((SELECT CONCAT(firstname, ' ', lastname) FROM users WHERE user_id = NEW.user_id), ' accepted your service request for ', (SELECT service_name FROM user_services WHERE service_id = NEW.service_id)), NOW(), 'service',New.request_id);
  ELSEIF NEW.status = 'declined' THEN
    INSERT INTO user_notifications (recipient_id, sender_id, message, created_at, notification_type,id)
    VALUES ( NEW.user_id,(SELECT user_id FROM user_services WHERE service_id = NEW.service_id), CONCAT('You cancelled your service request for ', (SELECT service_name FROM user_services WHERE service_id = NEW.service_id)), NOW(), 'service',New.request_id);
  END IF;
END $$
DELIMITER ;

