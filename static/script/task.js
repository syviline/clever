String.prototype.format = function () {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function (match, number) {
        return typeof args[number] != 'undefined'
            ? args[number]
            : match
            ;
    });
};

let taskTemplates = {
    textWithGaps: "<h1 class=\"task__label\">Вставьте пропуски</h1><div class=\"task__text\">{1}</div>",
    multipleAnswer: "<div class=\"question\"><div class=\"question__content\">{0}</div></div><h3 style=\"font-weight: 500; margin-top: 20px; margin-left: 20px;\">Выберите несколько ответов</h3><div class=\"answers__container\">{1}</div>",
    oneAnswer: "<div class=\"question\"><div class=\"question__content\">{0}</div></div><h3 style=\"font-weight: 500; margin-top: 20px; margin-left: 20px;\">Выберите один из ответов</h3><div class=\"answers__container\">{1}</div>"
}

function save(redirect=false) {
    let xhr = new XMLHttpRequest()
    xhr.open('POST', 'http://127.0.0.1:5000/test/save')
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({
        testid: testid,
        classid: classid,
        answers: answers,
        completed: redirect
    }))
    if (redirect) {
        xhr.onload = () => location = '/panel/tests'
    }
    console.log('Saved!')
}

setInterval(save, 5000)

function renderTask(task) {  // "Рендер задачи", чтобы потом вставить в DOM, используется при клике на стрелочку вперед или назад
    let taskText = ""
    let taskId = task.id
    let res
    switch (task.taskType) {
        case "multipleAnswer":
            for (let [index, item] of task.content.answers.entries()) {
                if (answers[taskId].includes(index))
                    taskText += `<button class=\"answer active\" id=\"answer${index}\" onclick=\"multipleAnswerChoose('answer${index}', '${taskId}')\">${item}</button>`
                else
                    taskText += `<button class=\"answer\" id=\"answer${index}\" onclick=\"multipleAnswerChoose('answer${index}', '${taskId}')\">${item}</button>`
            }
            // task.content.answers.forEach(item => {
            //     if (answers[taskId].includes(item))
            //         taskText += `<div class=\"answer active\" id=\"answer${item}\" onclick=\"multipleAnswerChoose('answer${item}', '${taskId}')\">${item}</div>`
            //     else
            //         taskText += `<div class=\"answer\" id=\"answer${item}\" onclick=\"multipleAnswerChoose('answer${item}', '${taskId}')\">${item}</div>`
            // })
            res = taskTemplates.multipleAnswer.format(task.content.question, taskText)
            return res
            break;
        case "textWithGaps":
            task.content.forEach(item => {
                if (typeof(item) == "string") {
                    taskText += item
                } else if(typeof(item) == "object") {
                    if ("content" in item) {
                        taskText += ` <select id='${item.id}' onchange="saveResult('${item.id}', '${taskId}')" value=''><option value="" selected disabled hidden></option>`
                        let alreadyAnswered = answers[taskId][item.id]
                        item.content.forEach(it => {
                            if (it == alreadyAnswered)
                                taskText += `<option value="${it}" selected>${it}</option>`
                            else
                                taskText += `<option value="${it}">${it}</option>`
                        })
                        taskText += '</select> '
                    } else {
                        let alreadyAnswered = answers[taskId][item.id]
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
                 if (answers[taskId] == index)
                     taskText += `<button class="answer active" id="answer${index}" onclick="oneAnswerChoose('answer${index}', '${taskId}')">${item}</button>`
                 else
                     taskText += `<button class="answer" id="answer${index}" onclick="oneAnswerChoose('answer${index}', '${taskId}')">${item}</button>`
            }
            res = taskTemplates.oneAnswer.format(task.content.question, taskText)
            return res
            break;
    }
}

function multipleAnswerChoose(id, taskId) {
    let elem = document.querySelector(`#${id}`)
    let ansid = parseInt(id.replace('answer', ''))
    if (elem.classList.contains('active')) {
        elem.classList.remove('active')
        answers[taskId].splice(answers[taskId].indexOf(ansid), 1)
    } else {
        elem.classList.add('active')
        answers[taskId].push(ansid)
    }
    console.log(answers[taskId])
}

function oneAnswerChoose(id, taskId) {
    let elem = document.querySelector(`#${id}`)
    let ansid = parseInt(id.replace('answer', ''))
    if (answers[taskId] != null) {
        let lastElem = document.querySelector(`.active`)
        console.log(lastElem)
        lastElem.classList.remove('active')
    }
    elem.classList.add('active')
    answers[taskId] = ansid
    console.log(answers)
}

function saveResult(id, parentId=null) {
    if (parentId == null) {
        answers[id] = document.querySelector(`#${id}`).value
    } else {
        answers[parentId][id] = document.querySelector(`#${id}`).value
    }
    console.log(id)
}

// let task = [
//     {
//         "id": 'a',
//         "taskType": "multipleAnswer",
//         "checkType": "auto",
//         "content": {
//             "question": "Города России",
//             "answers": ["Москва", "Лондон", "2", "2", "2", "2", "2", "2", "2", "2"]
//         }
//     },
//     {
//         "id": 'b',
//         "taskType": "textWithGaps",
//         "checkType": "auto",
//         "content": [
//             "Lorem ipsum", {
//                 "id": 'c'
//             }, "sit", {
//                 "id": 'd', "content": ["amet", "fish", "chicken"]
//             }, "kkqwmkqwek\n"
//         ]
//     },
//     {
//         "id": 'f',
//         "taskType": "oneAnswer",
//         "checkType": "auto",
//         "content": {
//             "question": "Назовите столицу Великобритании",
//             "answers": ["Москва", "Токио", "Лондон"]
//         }
//     }
// ]

if (!answers || Object.keys(answers).length == 0 || answers === 'none') {
    console.log(1)
    task.forEach(item => { // making an answers object
        if (item.taskType == "textWithGaps") {
            answers[item.id] = {}
            item.content.forEach(it => {
                if (typeof (it) == "object") {
                    answers[item.id][it.id] = ""
                }
            })
        } else if (item.taskType == "multipleAnswer") {
            answers[item.id] = []
        } else {
            answers[item.id] = null
        }
    })
}

let currentTaskId = 0

let forwardButton = document.querySelector(".forward")
let backButton = document.querySelector(".back")
let info = document.querySelector(".info")
let forwardIcon = forwardButton.querySelector('.material-icons-round')
// let taskInput

info.innerText = `${currentTaskId + 1} из ${task.length}`

let content = document.querySelector(".content .container")
content.innerHTML = renderTask(task[currentTaskId])
forwardButton.addEventListener('click', e => {
    e.preventDefault()
    if (currentTaskId >= task.length - 1) {
        save(true)
        return
    }
    currentTaskId++
    backButton.classList.remove('inactive')
    if (currentTaskId >= task.length - 1) {
        forwardIcon.innerText = 'done'
        forwardButton.style.backgroundColor = '#6F6'
        // forwardButton.classList.add('inactive')
    }
    content.innerHTML = renderTask(task[currentTaskId])
    info.innerText = `${currentTaskId + 1} из ${task.length}`
})

backButton.addEventListener('click', e => {
    e.preventDefault()
    if (currentTaskId <= 0)
        return
    currentTaskId--
    forwardIcon.innerText = 'arrow_forward'
    forwardButton.style.backgroundColor = '#38bdf8'
    // forwardButton.classList.remove('inactive')
    if (currentTaskId <= 0) {
        backButton.classList.add('inactive')
    }
    content.innerHTML = renderTask(task[currentTaskId])
    info.innerText = `${currentTaskId + 1} из ${task.length}`
})