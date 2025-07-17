
1.Список уникальных классов. Вывести только названия.
SELECT DISTINCT class_name
FROM visits;

2.Количество часов, проведенных на занятиях для каждого пользователя. Вывести фамилию, имя и количество часов.
SELECT u.user_surname AS surname,
       u.user_name AS name,
       COALESCE(SUM(v.hours_spent), 0) 
FROM users u
LEFT JOIN visits v ON u.id_user = v.id_user
GROUP BY u.id_user, surname, name
ORDER BY surname, name;

3.Средний возраст пользователей, посещающих класс Flex.
SELECT ROUND(AVG(u.age)) 
FROM users u
JOIN visits v ON u.id_user = v.id_user
WHERE v.class_name = 'Flex';

4. Вывести пользователей, которые ни разу не посещали бассейн (Swimming pool)
SELECT users.id_user, users.user_name, users.user_surname, users.user_weight, users.age
FROM users
LEFT JOIN visits ON users.id_user = visits.id_user AND visits.class_name = 'Swimming pool'
WHERE visits.id_visit IS NULL;
