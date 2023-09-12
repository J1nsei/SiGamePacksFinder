# SiGamePacksFinder

## Описание
Простой инструмент для поиска игровых пакетов [SiGame](https://vladimirkhil.com/si/game) на основе оценкок пользователей Вконтакте.

## Установка
1. Установите Python >= 3.7.
2. Установите зависимости:
```python -m pip install -r requirements.txt```

## Использование
1. Поместите Ваш VK API токен в файл token.txt ([Как получить токен?](https://dvmn.org/encyclopedia/qna/63/kak-poluchit-token-polzovatelja-dlja-vkontakte/)) 
2. Запустите программу ``` python SiGamePacksFinder.py --min_likes=5```,
   где параметр **--min_likes** означает минимальное количество лайков на посте с пакетом.
3. Откройте файл **SiGamePackages.csv** с помощью MS Excel (или его альтернативы), выберите нужный пост и нажмите на ячейку "Открыть". В появившемся окне браузера скачайте нужный пакет.
