String.prototype.format = function () { // форматирует строку. "dsf {0} fds".format('asd') = "dsf asd fds"
    var args = arguments;
    return this.replace(/{(\d+)}/g, function (match, number) {
        return typeof args[number] != 'undefined'
            ? args[number]
            : match
            ;
    });
};

function numToId(num) { // превращает число в буквенный id
    let res = ''
    let letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    num = num.toString()
    for (let i = 0; i < num.length; i++) {
        res += letters[num[i]]
    }
    return res
}

function idToNum(id) { // превращает буквенный id в число
    let res = ''
    let letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    for (let i = 0; i < id.length; i++) {
        res += letters.indexOf(id[i])
    }
    return parseInt(res)
}

function generateUniqueId() { // генерирует уникальный id по текущему времени
    d = Date.now()
    r = Math.floor(Math.random() * 10000)
    return numToId(d * r)
}

/*function getMaxId() {
    let res
    task.forEach(item => {
        if (item.taskType != 'textWithGaps') {
            numid = idToNum(item.id)
            if (numid > res)
                res = numid
        } else {
            item.content.forEach(it => {
                if (typeof(it) == 'object') {
                    numid = idToNum(it.id)
                    if (numid > res)
                        res = numid
                }
            })
        }
    })
}*/

if (task.length == 0) { // при запуске: если ничего нет в task, то делаем task = [{}]
    task = [{}]
}

let taskTemplates = { // шаблоны для заданий
    textWithGaps: "<h1 class=\"task__label\">Вставьте пропуски</h1><div class=\"task__text editable\" contenteditable='true' oninput='textWithGapsInput()'></div>",
    multipleAnswer: "<div class=\"question\"><div class=\"question__content\" id=\"question\"><div class=\"editable\" contenteditable=\"true\" oninput='editQuestion()'>{0}</div></div></div><h3 style=\"font-weight: 500; margin-top: 20px; margin-left: 20px;\">Выберите несколько ответов</h3><div class=\"answers__container\">{1}</div>",
    oneAnswer: "<div class=\"question\"><div class=\"question__content\" id=\"question\"><div class='editable' contenteditable='true' oninput='editQuestion()'>{0}</div></div></div><h3 style=\"font-weight: 500; margin-top: 20px; margin-left: 20px;\">Выберите один из ответов</h3><div class=\"answers__container\">{1}</div>",
    chooseTemplate: "<h2 class=\"textcenter\">Выберите шаблон для задания</h2><div class=\"variants\"><button onclick='chooseTemplate(1)'>Вопрос и выбор из нескольких ответов</button><button onclick='chooseTemplate(2)'>Текстовое поле с пропусками</button><button onclick='chooseTemplate(3)'>Вопрос и выбор из одного ответа</button></div>"

}

function renderTask(task) {  // "Рендер задачи", чтобы потом вставить в DOM, используется при клике на стрелочку вперед или назад
    console.log(task)
    console.log(correctAnswersIds)
    let taskText = "" // html код внутренностей задания
    let taskId = task.id // id задачи
    let res // результат
    if (Object.keys(task).length == 0) { // если задание пустое( {} ), то возвращаем шаблон выбора шаблона
        return taskTemplates.chooseTemplate
    }
    switch (task.taskType) { // обработчики шаблонов
        case "multipleAnswer": // вопрос и несколько ответов
            for (let [index, item] of task.content.answers.entries()) {
                if (correctAnswersIds[taskId].includes(index))
                    taskText += `<button class=\"answer active\" id=\"answer${index}\" oncontextmenu=\"multipleAnswerChoose('answer${index}', '${taskId}')\"><div class="empty"></div><div class="editable" contenteditable="true" oninput="editAnswer('answer${index}')">${item}</div><div class="delete__button" onclick="deleteVariant(${index})"><span class="material-icons-round">delete</span></div></button>`
                else
                    taskText += `<button class=\"answer\" id=\"answer${index}\" oncontextmenu=\"multipleAnswerChoose('answer${index}', '${taskId}')\"><div class="empty"></div><div class="editable" contenteditable="true" oninput="editAnswer('answer${index}')">${item}</div><div class="delete__button" onclick="deleteVariant(${index})"><span class="material-icons-round">delete</span></div></button>`
            }
            taskText += `<button class=\"answer answer-add\" onclick=\"addAnswer()\"><span class="material-icons-round">add_circle_outline</span></button>`
            res = taskTemplates.multipleAnswer.format(task.content.question, taskText)
            return res
            break;
        case "textWithGaps": // текст с пропусками
            return taskTemplates.textWithGaps
            break;
        case "oneAnswer": // вопрос и один ответ
            for (let [index, item] of task.content.answers.entries()) {
                 if (correctAnswersIds[taskId] == index && correctAnswersIds[taskId] !== '')
                     taskText += `<button class="answer active" id="answer${index}" oncontextmenu="oneAnswerChoose('answer${index}', '${taskId}')"><div class="empty"></div><div class="editable" contenteditable="true" oninput="editAnswer('answer${index}')">${item}</div><div class="delete__button" onclick="deleteVariantOneAnswer(${index})"><span class="material-icons-round">delete</span></div></button>`
                 else
                     taskText += `<button class="answer" id="answer${index}" oncontextmenu="oneAnswerChoose('answer${index}', '${taskId}')"><div class="empty"></div><div class="editable" contenteditable="true" oninput="editAnswer('answer${index}')">${item}</div><div class="delete__button" onclick="deleteVariantOneAnswer(${index})"><span class="material-icons-round">delete</span></div></button>`
            }
            taskText += `<button class=\"answer answer-add\" onclick=\"addAnswer()\"><span class="material-icons-round">add_circle_outline</span></button>`
            res = taskTemplates.oneAnswer.format(task.content.question, taskText)
            return res
            break;
    }
}

function textWithGapsInput() {
    task[currentTaskId].content = document.querySelector('.editable').innerText
}

function renderTaskDOM() { // "рендер" задачи в DOM
    content.innerHTML = renderTask(task[currentTaskId])
    if (task[currentTaskId].taskType == 'textWithGaps') {
        document.querySelector('.editable').innerText = task[currentTaskId].content
    }
}

function deleteVariant(index) { // Удаление варианта ответа в multipleAnswer
    task[currentTaskId].content.answers.splice(index, 1)
    let taskId = task[currentTaskId].id
    let indexOfAnswer = correctAnswersIds[taskId].indexOf(index)
    if (indexOfAnswer != -1)
        correctAnswersIds[taskId].splice(correctAnswersIds[taskId].indexOf(index), 1)
    for (i = 0; i <= correctAnswersIds[taskId].length; i++) {
        console.log(correctAnswersIds[taskId][i])
        if (correctAnswersIds[taskId][i] > index) {
            correctAnswersIds[taskId][i] -= 1
        }
    }
    renderTaskDOM()
}

function deleteVariantOneAnswer(index) { // Удаление варианта ответа в oneAnswer
    task[currentTaskId].content.answers.splice(index, 1)
    let taskId = task[currentTaskId].id
    if (correctAnswersIds[taskId] == index) {
        correctAnswersIds[taskId] = null
    } else if (correctAnswersIds[taskId] > index) {
        correctAnswersIds[taskId] -= 1
    }
    renderTaskDOM()
}

function editQuestion() { // Изменение вопроса
    let newQuestion = document.querySelector('#question').innerText
    task[currentTaskId].content.question = newQuestion
}

function editAnswer(id) { // Изменение варианта ответа
    let newans = document.querySelector(`#${id} .editable`).innerText
    let ansId = parseInt(id.replace('answer', ''))
    task[currentTaskId].content.answers[ansId] = newans
}

function oneAnswerChoose(id, taskId) {
    e = window.event
    e.preventDefault()
    id = parseInt(id.replace('answer', ''))
    correctAnswersIds[taskId] = id
    renderTaskDOM()
}

function multipleAnswerChoose(id, taskId) {
    e = window.event
    e.preventDefault()
    let elemId = parseInt(id.replace('answer', ''))
    // let elem = document.querySelector(`#${id}`)
    // if(elem.innerText in correctAnswers[taskId]) {
    //     correctAnswers[taskId].slice(correctAnswers[taskId].indexOf(elem.innerText))
    // } else {
    //     correctAnswers[taskId].push(elem.innerText)
    // }
    if (correctAnswersIds[taskId].includes(elemId)) {
        correctAnswersIds[taskId].splice(correctAnswersIds[taskId].indexOf(elemId), 1)
    } else {
        correctAnswersIds[taskId].push(elemId)
    }
    renderTaskDOM()
}

function chooseTemplate(id) { // выбор шаблона при создании нового задания
    uid = generateUniqueId()
    task[currentTaskId].id = uid
    if (id == 1) {
        task[currentTaskId].taskType = 'multipleAnswer'
        task[currentTaskId].content = {question: "", answers: []}
        correctAnswersIds[uid] = []
    } else if (id == 2) {
        task[currentTaskId].taskType = 'textWithGaps'
        task[currentTaskId].content = ''
        correctAnswersIds[uid] = {}
    } else if (id == 3) {
        task[currentTaskId].taskType = 'oneAnswer'
        task[currentTaskId].content = {question: "", answers: []}
        correctAnswersIds[uid] = null
    }
    renderTaskDOM()
}

function addAnswer() { // добавление ответа в задание
    task[currentTaskId].content.answers.push("")
    renderTaskDOM()
}

let currentTaskId = 0 // id текущей задачи в массиве task
let forwardButton = document.querySelector(".forward") // кнопочки
let backButton = document.querySelector(".back")
let forwardIcon = forwardButton.querySelector('.material-icons-round')
let info = document.querySelector(".info")

info.innerText = `${currentTaskId + 1} из ${task.length}` // информация о текущем задании снизу(1 из 3 и т.д.)

let content = document.querySelector(".content .container")
renderTaskDOM()

if (currentTaskId + 1 == task.length) { // если текущее задание последнее, то на кнопке вперед будет знак плюса
    forwardIcon.innerText = 'add'
}

forwardButton.addEventListener('click', e => { // при нажатии на кнопку вперед
    e.preventDefault()
    if (currentTaskId + 1 == task.length) { // если текущее задание последнее, то создаем новое
        task.push({})
    }
    currentTaskId++
    info.innerText = `${currentTaskId + 1} из ${task.length}` // обновляем info
    if (currentTaskId + 1 == task.length) { // если текущее задание последнее, то на кнопке вперед будет знак плюса
        forwardIcon.innerText = 'add'
    }
    backButton.classList.remove('inactive') // делаем кнопку назад активной(если она была неактивной)
    renderTaskDOM() // "рендерим" контент задачи
})

backButton.addEventListener('click', e => { // кнопка назад
    e.preventDefault()
    if (currentTaskId < 1) {
        return
    }
    currentTaskId--
    if (currentTaskId == 0) {
        backButton.classList.add('inactive')
    }
    forwardIcon.innerText = 'arrow_forward'
    info.innerText = `${currentTaskId + 1} из ${task.length}`
    renderTaskDOM()
})