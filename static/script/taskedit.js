String.prototype.format = function () {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function (match, number) {
        return typeof args[number] != 'undefined'
            ? args[number]
            : match
            ;
    });
};

function numToId(num) {
    let res = ''
    let letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    num = num.toString()
    for (let i = 0; i < num.length; i++) {
        res += letters[num[i]]
    }
    return res
}

function idToNum(id) {
    let res = ''
    let letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    for (let i = 0; i < id.length; i++) {
        res += letters.indexOf(id[i])
    }
    return parseInt(res)
}

function generateUniqueId() {
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

if (task.length == 0) {
    task = [{}]
}

let taskTemplates = {
    textWithGaps: "<h1 class=\"task__label\">Вставьте пропуски</h1><div class=\"task__text\">{1}</div>",
    multipleAnswer: "<div class=\"question\"><div class=\"question__content\">{0}</div></div><h3 style=\"font-weight: 500; margin-top: 20px; margin-left: 20px;\">Выберите несколько ответов</h3><div class=\"answers__container\">{1}</div>",
    oneAnswer: "<div class=\"question\"><div class=\"question__content\">{0}</div></div><h3 style=\"font-weight: 500; margin-top: 20px; margin-left: 20px;\">Выберите один из ответов</h3><div class=\"answers__container\">{1}</div>",
    chooseTemplate: "<h2 class=\"textcenter\">Выберите шаблон для задания</h2><div class=\"variants\"><button onclick='chooseTemplate(1)'>Вопрос и выбор из нескольких ответов</button><button onclick='chooseTemplate(2)'>Вопрос и выбор из одного ответа</button><button onclick='chooseTemplate(3)'>Текстовое поле с пропусками</button></div>"

}

function renderTask(task) {  // "Рендер задачи", чтобы потом вставить в DOM, используется при клике на стрелочку вперед или назад
    console.log(task)
    console.log(correctAnswers)
    let taskText = ""
    let taskId = task.id
    let res
    if (Object.keys(task).length == 0) {
        return taskTemplates.chooseTemplate
    }
    switch (task.taskType) {
        case "multipleAnswer":
            for (let [index, item] of task.content.answers.entries()) {
                if (correctAnswers[taskId].includes(item))
                    taskText += `<button class=\"answer active\" id=\"answer${index}\" onclick=\"multipleAnswerChoose('answer${index}', '${taskId}')\"><div class="editable" contenteditable="true">${item}</div></button>`
                else
                    taskText += `<button class=\"answer\" id=\"answer${index}\" onclick=\"multipleAnswerChoose('answer${index}', '${taskId}')\"><div class="editable" contenteditable="true">${item}</div></button>`
            }
            taskText += `<button class=\"answer answer-add\" onclick=\"addAnswer()\"><span class="material-icons-round">add_circle_outline</span></button>`
            res = taskTemplates.multipleAnswer.format(`<div class="editable" contenteditable="true">${task.content.question}</div>`, taskText)
            return res
            break;
        case "textWithGaps":
            task.content.forEach(item => {
                if (typeof(item) == "string") {
                    taskText += item
                } else if(typeof(item) == "object") {
                    if ("content" in item) {
                        taskText += ` <select id='${item.id}' onchange="saveResult('${item.id}', '${taskId}')" value=''><option value="" selected disabled hidden></option>`
                        let alreadyAnswered = correctAnswers[taskId][item.id]
                        item.content.forEach(it => {
                            if (it == alreadyAnswered)
                                taskText += `<option value="${it}" selected>${it}</option>`
                            else
                                taskText += `<option value="${it}">${it}</option>`
                        })
                        taskText += '</select> '
                    } else {
                        let alreadyAnswered = correctAnswers[taskId][item.id]
                        if (alreadyAnswered != "")
                            taskText += ` <input class='task__input' id='${item.id}' oninput="saveResult('${item.id}', '${taskId}')" value='${alreadyAnswered}'> `
                        else
                            taskText += ` <input class='task__input' id='${item.id}' oninput="saveResult('${item.id}', '${taskId}')"> `
                    }
                }
            })
            res = taskTemplates.textWithGaps.format(task.header, taskText)
            return res
            console.log(2)
            break;
        case "oneAnswer":
            for (let [index, item] of task.content.answers.entries()) {
                 if (correctAnswers[taskId] == item)
                     taskText += `<div class="answer active" id="answer${index}" onclick="oneAnswerChoose('answer${index}', '${taskId}')">${item}</div>`
                 else
                     taskText += `<div class="answer" id="answer${index}" onclick="oneAnswerChoose('answer${index}', '${taskId}')">${item}</div>`
            }
            res = taskTemplates.oneAnswer.format(task.content.question, taskText)
            return res
            break;
    }
}

function chooseTemplate(id) {
    task[currentTaskId].id = generateUniqueId()
    if (id == 1) {
        task[currentTaskId].taskType = 'multipleAnswer'
        task[currentTaskId].content = {question: "", answers: []}
    } else if (id == 2) {
        task[currentTaskId].taskType = 'textWithGaps'
        task[currentTaskId].content = []
    } else if (id == 3) {
        task[currentTaskId].taskType = 'oneAnswer'
        task[currentTaskId].content = {question: "", answers: []}
    }
    content.innerHTML = renderTask(task[currentTaskId])
}

function addAnswer() {
    task[currentTaskId].content.answers.push("")
    content.innerHTML = renderTask(task[currentTaskId])
}

let currentTaskId = 0
let forwardButton = document.querySelector(".forward")
let backButton = document.querySelector(".back")
let forwardIcon = forwardButton.querySelector('.material-icons-round')
let info = document.querySelector(".info")

info.innerText = `${currentTaskId + 1} из ${task.length}`

let content = document.querySelector(".content .container")
content.innerHTML = renderTask(task[currentTaskId])

if (currentTaskId + 1 == task.length) {
    forwardIcon.innerText = 'add'
}

forwardButton.addEventListener('click', e => {
    e.preventDefault()
    if (currentTaskId + 1 == task.length) {
        task.push({})
    }
    currentTaskId++
    info.innerText = `${currentTaskId + 1} из ${task.length}`
    if (currentTaskId + 1 == task.length) {
        forwardIcon.innerText = 'add'
    }
    backButton.classList.remove('inactive')
    content.innerHTML = renderTask(task[currentTaskId])
})

backButton.addEventListener('click', e => {
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
    content.innerHTML = renderTask(task[currentTaskId])
})