1.Список уникальных классов. Вывести только названия.
SELECT DISTINCT class_name
FROM visits;

2.Количество часов, проведенных на занятиях для каждого пользователя. Вывести фамилию, имя и количество часов.
SELECT u.user_surname AS surname,
       u.user_name AS name,
       COALESCE(SUM(v.hours_spent), 0) 
FROM users AS u
LEFT JOIN visits AS v ON u.id_user = v.id_user
GROUP BY u.id_user
ORDER BY surname, name;

3.Средний возраст пользователей, посещающих класс Flex.
SELECT ROUND(AVG(u.age)) 
FROM users AS u
LEFT JOIN visits AS v ON u.id_user = v.id_user
WHERE v.class_name = 'Flex';

4. Вывести пользователей, которые ни разу не посещали бассейн (Swimming pool)
SELECT u.id_user, u.user_name, u.user_surname, u.user_weight, u.age
FROM users AS u
LEFT JOIN visits AS v ON u.id_user = v.id_user AND v.class_name = 'Swimming pool'
WHERE v.id_visit IS NULL;

