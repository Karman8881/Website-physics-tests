document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');

    // Обработка регистрации
    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            registerUser(username, password);
        });
    }

    // Обработка входа
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;
            loginUser(username, password);
        });
    }

    // Проверка токена
    const token = window.localStorage.getItem('token');
    if (token === null && window.location.pathname.endsWith('tests.html')) {
        window.location.href = '/site/index.html'; // Перенаправление на страницу входа, если токена нет
        return;
    }

    // Загрузка тестов, если пользователь авторизован
    if (window.location.pathname.endsWith('tests.html')) {
        fetchTests();

        const submitTestButton = document.getElementById('submitTest');
        if (submitTestButton) {
            submitTestButton.addEventListener('click', function (e) {
                e.preventDefault();
                submitTest();
            });
        }
    }
});

// Функция регистрации пользователя
function registerUser(username, password) {
    fetch('/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка регистрации: Проверьте введенные данные');
            }
            return response.json();
        })
        .then(data => {
            alert('Регистрация прошла успешно!');
            window.location.href = '/site/index.html'; // Перенаправление на страницу входа
        })
        .catch((error) => {
            console.error('Ошибка:', error);
            alert(error.message || 'Ошибка регистрации. Попробуйте снова.');
        });
}

// Функция входа пользователя
function loginUser(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    fetch('/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка входа: Проверьте логин и пароль');
            }
            return response.json();
        })
        .then(data => {
            window.localStorage.setItem('token', data.access_token);
            alert('Вход выполнен успешно!');
            window.location.href = '/site/tests.html'; // Перенаправление на страницу тестов
        })
        .catch((error) => {
            console.error('Ошибка:', error);
            alert(error.message || 'Ошибка входа. Попробуйте снова.');
        });
}

// Функция загрузки тестов
function fetchTests() {
    fetch('/tests/', {
        headers: {
            'Authorization': `Bearer ${window.localStorage.getItem('token')}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Не удалось загрузить тесты');
            }
            return response.json();
        })
        .then(data => {
            const testsContainer = document.getElementById('tests');
            testsContainer.innerHTML = '';
            data.forEach(test => {
                const testElement = document.createElement('div');
                testElement.className = 'test fade-in';
                testElement.innerHTML = `
                    <h2>${test.title}</h2>
                    <p>${test.description}</p>
                    <button onclick="startTest(${test.id})">Начать тест</button>
                `;
                testsContainer.appendChild(testElement);
            });
        })
        .catch((error) => {
            console.error('Ошибка:', error);
            alert(error.message || 'Не удалось загрузить тесты. Попробуйте снова.');
        });
}

// Функция начала теста
function startTest(testId) {
    fetch(`/tests/${testId}/questions/`, {
        headers: {
            'Authorization': `Bearer ${window.localStorage.getItem('token')}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Не удалось загрузить вопросы');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('tests').style.display = 'none';
            document.getElementById('questions').style.display = 'block';
            document.getElementById('testTitle').innerText = `Тест ${testId}`;

            const questionsList = document.getElementById('questionsList');
            questionsList.innerHTML = ''; // Очистка контейнера перед добавлением вопросов

            data.forEach((question, index) => {
                const questionElement = document.createElement('div');
                questionElement.className = 'question fade-in';
                questionElement.innerHTML = `
                    <p><strong>Вопрос ${index + 1}:</strong> ${question.text}</p>
                    <div class="options">
                        ${question.options.map((option, optionIndex) => `
                            <label>
                                <input type="radio" name="question${question.id}" value="${option}">
                                ${option}
                            </label><br>
                        `).join('')}
                    </div>
                `;
                questionsList.appendChild(questionElement);
            });
        })
        .catch((error) => {
            console.error('Ошибка:', error);
            alert(error.message || 'Не удалось загрузить вопросы. Попробуйте снова.');
        });
}

// Функция отправки теста
function submitTest() {
    const questions = document.querySelectorAll('.question');
    let score = 0;
    const results = [];

    questions.forEach(question => {
        const selectedOption = question.querySelector('input[type="radio"]:checked');
        if (selectedOption) {
            const questionId = selectedOption.name.replace('question', '');
            const correctAnswer = Array.from(questions).find(q => q.id === parseInt(questionId)).correct_answer;
            if (selectedOption.value === correctAnswer) {
                score++;
                results.push({ questionId, correct: true });
            } else {
                results.push({ questionId, correct: false });
            }
        }
    });

    // Отображение результатов
    showResults(score, questions.length, results);
}

// Функция отображения результатов
function showResults(score, totalQuestions, results) {
    const questionsList = document.getElementById('questionsList');
    questionsList.innerHTML = ''; // Очистка контейнера перед добавлением результатов

    const resultElement = document.createElement('div');
    resultElement.className = 'result-summary fade-in';
    resultElement.innerHTML = `
        <h2>Результаты теста</h2>
        <p>Вы ответили правильно на <strong>${score}</strong> из <strong>${totalQuestions}</strong> вопросов.</p>
    `;
    questionsList.appendChild(resultElement);

    results.forEach(result => {
        const questionResult = document.createElement('div');
        questionResult.className = `question-result ${result.correct ? 'correct' : 'incorrect'} fade-in`;
        questionResult.innerHTML = `
            <p>Вопрос ${result.questionId}: ${result.correct ? 'Правильно' : 'Неправильно'}</p>
        `;
        questionsList.appendChild(questionResult);
    });

    // Кнопка для возврата к тестам
    const backButton = document.createElement('button');
    backButton.className = 'btn center';
    backButton.innerText = 'Вернуться к тестам';
    backButton.addEventListener('click', () => {
        window.location.href = '/site/tests.html';
    });
    questionsList.appendChild(backButton);
}