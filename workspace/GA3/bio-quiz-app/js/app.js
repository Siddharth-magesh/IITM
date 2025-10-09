const questions = [
    {
        question: "What is known as the powerhouse of the cell?",
        options: ["Nucleus", "Mitochondria", "Ribosome", "Endoplasmic Reticulum"],
        answer: 1
    },
    // Additional questions can be added here
];

let currentQuestionIndex = 0;
let score = 0;

const questionElement = document.getElementById('question');
const optionsElement = document.getElementById('options');
const scoreElement = document.getElementById('score');
const nextButton = document.getElementById('next-button');

function loadQuestion() {
    const currentQuestion = questions[currentQuestionIndex];
    questionElement.textContent = currentQuestion.question;
    optionsElement.innerHTML = '';

    currentQuestion.options.forEach((option, index) => {
        const button = document.createElement('button');
        button.textContent = option;
        button.classList.add('option-button');
        button.addEventListener('click', () => selectOption(index));
        optionsElement.appendChild(button);
    });

    scoreElement.textContent = `Score: ${score}`;
}

function selectOption(index) {
    if (index === questions[currentQuestionIndex].answer) {
        score++;
    }
    nextButton.style.display = 'block';
}

nextButton.addEventListener('click', () => {
    currentQuestionIndex++;
    if (currentQuestionIndex < questions.length) {
        loadQuestion();
        nextButton.style.display = 'none';
    } else {
        questionElement.textContent = `Quiz Over! Your final score is: ${score}`;
        optionsElement.innerHTML = '';
        nextButton.style.display = 'none';
    }
});

// Initial load
loadQuestion();