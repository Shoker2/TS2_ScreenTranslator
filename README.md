# TS2_ScreenTranslator

## Оглавление
- [Введение](#введение)
- [Как скачать](#как-скачать)
- [Как пользоваться](#как-пользоваться)

## Введение

TS2_ScreenTranslator - программа, которая переводит текст с экрана. Как это происходит:
- Вы выделяете область, текст в которой нужно перевести.
- Программа делает скриншот этой области
- Программа распознаёт текст со скриншота
- Программа переводит полученный текст на выбранный язык
- Программа создаёт окно с переведённым текстом на месте выделения

## Как скачать
- Зайдите в [Releases](https://github.com/Shoker2/TS2_ScreenTranslator/releases)
- Раскройте выпадающий список "Assets"
- Выберите "TS2_ScreenTranslator.exe" или "TS2_ScreenTranslator.zip"

TS2_ScreenTranslator.zip - архив с программой

TS2_ScreenTranslator.exe - саморазархивирующийся архив (Тотже архив, но ему не нужна отдельная программа для разорхивирования)

### Если скачали TS2_ScreenTranslator.zip

Нажмите правой кнопкой мыши по архиву и выберите "Извлечь в текущую папку"

![image](https://user-images.githubusercontent.com/66993983/209824336-316d7c9e-c383-448b-a34f-b1d961510592.png)

Или откройте архив и перетащите папку на рабочий стол

![image](https://user-images.githubusercontent.com/66993983/209824433-f6502641-091e-49e4-9a73-c51108722d92.png)

### Если скачали TS2_ScreenTranslator.exe

Откройте файл и нажмите "Извлечь"

![image](https://user-images.githubusercontent.com/66993983/209824195-5d9068dd-b4bd-4e5b-8fe3-6000c1f2a00e.png)

---

В папке есть файл "main.exe". Откройте его и программа запустится

![image](https://user-images.githubusercontent.com/66993983/209826117-82d5cfa0-ef97-4394-9376-e744de198d43.png)

Вы можете поместить папку на диск C: или любой друго, чтобы она не мешала на рабочем столе. Дальше зайдите в папку и перенесите файл "main.exe" на рабочий стол с помощью правой кнопки мыши, после чего нажмите "Создать ярлык здесь".

![image](https://user-images.githubusercontent.com/66993983/209826495-23eeec84-69e2-43e1-b321-a682d25797d7.png)

Но помните, если вы переместите папку после создания ярлыка, то ярлык перестанет работать и его придётся создавать заново.

[:arrow_up: К оглавлению](#оглавление)

# Как пользоваться

Нажмите сочетание клавиш "Alt+Z"

Нажмите правой кнопкой мыши и в появившимся окно выберите с какого язывка вы хотите переводить текст "From" и на какой "To". Дальше нажмите "Apply"

![image](https://user-images.githubusercontent.com/66993983/212059973-b173f60d-9abc-4ae9-a83e-4366c98d6fc3.png)

Теперь выделите область с текстом для перевода с помощью левой кнопкой мыши. После обработки, создастся окно на месте выделения с переведённым текстом.

Чтобы закрыть это окно нажмите "Esc"

Чтобы повторить прошлое выделение, то нажмите сочетание клавиш "Alt+X"

[:arrow_up: К оглавлению](#оглавление)

## Меню с настройками

Давайте вернёмся к окну, с настройками.

Напомню: Чтобы его окрыть, нужно Нажать сочетание клавиш "Alt+Z", после чего нажать правой кнопкой мыши на экране выделения области. (Выйти нажатием "Esc")

Здесь есть следующие вкладки:
- [General](#general)
- [Font](#font)
- [Shortcuts](#shortcuts)
- [Output](#output)
- [Correction](#correction)

### General

![image](https://user-images.githubusercontent.com/66993983/212059973-b173f60d-9abc-4ae9-a83e-4366c98d6fc3.png)

- From - С какого языка переводить текст
- To - На какой язык переводить текст
- Translator - Переводчик
- Recognizer - Выбор распознователя текста (Чтобы работали другие языки tesseract, нужно [скачать языки отдельно (Assets -> tesseract_langs.zip)](https://github.com/Shoker2/TS2_ScreenTranslator/releases) и переместить все фалы в папку "tesseract" -> "tessdata" внутри папки приложения)
- Apply - Кнопка для применения настроек

### Font

![image](https://user-images.githubusercontent.com/66993983/209829804-3e49082f-08f0-4f05-9ffe-d8cadb0dc52f.png)

- Выпадающий список со шрифтами - выбор шрифта
- Спин-бокс - выбор размера шрифта

Настройки в этой вкладке влияют только на текст в окне с переведённым текстом.

### Shortcuts

![image](https://user-images.githubusercontent.com/66993983/209830697-df3bc328-84b2-4d30-9488-cf6c23a46f94.png)

- Select Area - сочетание клавиш для выбора области перевода текста
- Repeat Area - сочетание клавиш для повторения прошлой бласти

### Output

![image](https://user-images.githubusercontent.com/66993983/210096684-881e1e4a-66cf-4ced-a943-4b799f7ef3e4.png)

![image](https://user-images.githubusercontent.com/66993983/210096640-d16c3bc2-7064-42a3-8558-9eb0bc376317.png)

- Output to the window - Создаст окно с переведённым текстом на месте выделения
- Output to the console - Выведет переведённый текст в консоль
- Output to the clipboard - Скопирует переведённый текст в буфер обмена
- Output original to console - Выведет отсканированный текст в консоль
- Output to the TS2ST_Server - Отправит переведённый текст на [TS2_ScreenTranslator_Server](https://github.com/Shoker2/TS2_ScreenTranslator_Server) (С помощью сокетов). Ниже есть поле ввода для IP [TS2_ScreenTranslator_Server](https://github.com/Shoker2/TS2_ScreenTranslator_Server)

### Correction

![image](https://user-images.githubusercontent.com/66993983/209830709-3def4d19-c3fd-4714-9df2-eb7e447088cd.png)

Тут находится таблица для выполнения замен в тексте (Полезно, если вы стример и хотите не переводить некоторые слова)

- Колонка "Source" - Что должно быть заменено
- Колонка "Changed" - На что должно быть заменено

[:arrow_up: К оглавлению](#оглавление)
