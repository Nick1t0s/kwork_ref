-- INSERT INTO Users (id, reg_by, first_name, username, last_name, language_code)
--         VALUES (7, 123, nok, nok, sadf, en);
-- DELETE FROM Users WHERE id = 7
SELECT count(*) FROM Users;
SELECT Users.username FROM Users ORDER BY invited DESC LIMIT 2;
SELECT id FROM Users;
UPDATE Users SET tripvaers = 1 WHERE id = 6080085900;