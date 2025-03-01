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
        console.log(token);
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
                throw new Error('Registration failed');
            }
            return response.json();
        })
        .then(data => {
            alert('Registration successful');
            window.location.href = '/site/index.html'; // Перенаправление на страницу входа
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Registration failed. Please try again.');
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
                throw new Error('Login failed');
            }
            return response.json();
        })
        .then(data => {
            window.localStorage.setItem('token', data.access_token);
            alert('Login successful');
            window.location.href = '/site/tests.html'; // Перенаправление на страницу тестов
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Login failed. Please check your credentials.');
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
                throw new Error('Failed to fetch tests');
            }
            return response.json();
        })
        .then(data => {
            const testsContainer = document.getElementById('tests');
            testsContainer.innerHTML = '';
            data.forEach(test => {
                const testElement = document.createElement('div');
                testElement.className = 'test';
                testElement.innerHTML = `
                    <h2>${test.title}</h2>
                    <p>${test.description}</p>
                    <button onclick="startTest(${test.id})">Start Test</button>
                `;
                testsContainer.appendChild(testElement);
            });
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Failed to load tests. Please try again.');
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
                throw new Error('Failed to fetch questions');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('tests').style.display = 'none';
            document.getElementById('questions').style.display = 'block';
            document.getElementById('testTitle').innerText = `Test ${testId}`;
            const questionsList = document.getElementById('questionsList');
            questionsList.innerHTML = ''; // Очистка контейнера перед добавлением вопросов
            data.forEach((question, index) => {
                const questionElement = document.createElement('div');
                questionElement.className = 'question';
                questionElement.innerHTML = `
                    <p>${index + 1}. ${question.text}</p>
                    ${question.options.map(option => `
                        <label>
                            <input type="radio" name="question${question.id}" value="${option}">
                            ${option}
                        </label>
                    `).join('')}
                `;
                questionsList.appendChild(questionElement);
            });
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Failed to load questions. Please try again.');
        });
}

// Функция отправки теста
function submitTest() {
    const questions = document.querySelectorAll('.question');
    let score = 0;
    questions.forEach(question => {
        const selectedOption = question.querySelector('input[type="radio"]:checked');
        if (selectedOption) {
            const questionId = selectedOption.name.replace('question', '');
            const correctAnswer = Array.from(questions).find(q => q.id === parseInt(questionId)).correct_answer;
            if (selectedOption.value === correctAnswer) {
                score++;
            }
        }
    });
    alert(`Your score is ${score}/${questions.length}`);
    // window.location.href = 'tests.html'; // Раскомментируйте, если хотите перенаправить пользователя
}